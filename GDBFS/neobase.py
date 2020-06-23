import py2neo
from py2neo import *
from py2neo.ogm import *
from api_extension import api_top
from typing import *
import os
from pprint import pprint
import logging

class FileNode:
    RELATES_TO = Relationship.type('RELATES_TO')
    property_keys = {'name', 'path', 'cTime', 'mTime', 'aTime', 'size'}

    def __init__(self, file_path=None, node=None, properties=None, keywords=None, labels=None, auto_update=False):
        """
        :param properties: A dict indicating the other properties needed to be specified. None by default
        :type properties: dict
        :param keywords: The other keywords needed to be added.
        :type keywords: set[str]
        :param labels: The list of labels for this node. 'File' by default
        :type labels: List[str]
        :param auto_update: Whether update the file's info according to given path
        :type auto_update: bool
        """
        # ====================Set Basic Variables of FileNode====================
        labels = ('File',) if labels is None else list(labels)
        # FileNode.node
        if node:
            self.node = node
        else:
            self.node = Node(*labels)
        self.node.update(properties)
        if file_path:
            self.node.update({'path': file_path})
        # The keywords as set
        self.keywords = set() if keywords is None else set(keywords)
        # The keyword nodes
        self.keyword_nodes = None
        # The subgraph depicting the relationships
        self.relationships = None
        # ====================Update Variables====================
        # Update self.keywords, keywords_nodes and relationships according to API
        if auto_update:
            self.update_info()

    def update_properties(self, properties=None):
        if properties is None:
            properties = api_top.get_keywords_properties(self.node['path'], PM_code=2)['properties']
        properties = {key: properties[key] for key in properties.keys() if key in FileNode.property_keys}
        self.node.update(properties)

    def update_keywords(self, keywords=None, keys_limit=5, filename_extension_specified=None):
        """
        :param filename_extension_specified: specify the file type
        :type filename_extension_specified: str
        :param keys_limit: limit of keywords
        :type keys_limit: int
        :param keywords: keywords needed to be added, if None, use api.
        :type keywords: set
        :return node: The node of the file.
        :rtype node: py2neo.data.Node
        """
        if not keywords:
            keywords = api_top.get_keywords_properties(self.node['path'], keys_limit,
                                                       filename_extension_specified, PM_code=1)['keywords']
        self.keywords |= set(keywords)
        self.update_keyword_nodes()

    def update_keyword_nodes(self):
        keyword_nodes = []
        for keyword in self.keywords:
            keyword_nodes.append(Node('Keyword', name=keyword))
        self.keyword_nodes = Subgraph(keyword_nodes) if keyword_nodes != [] else None

    def update_relationships(self):
        self.update_keyword_nodes()
        relationships = self.node
        if type(self.keyword_nodes) is not Subgraph:
            return
        for keyword_node in self.keyword_nodes.nodes:
            relationships |= FileNode.RELATES_TO(self.node, keyword_node)
        self.relationships = relationships

    def update_info(self, other_properties=None, other_keywords=None, keys_limit=5, filename_extension_specified=None):
        # update with api
        self.update_keywords()
        self.update_properties()
        # update with given values
        if other_properties:
            self.update_properties(properties=other_properties)
        if other_keywords:
            self.update_keywords(keywords=set(other_keywords))
        # update subgraphs
        self.update_relationships()

    def merge_into(self, graph):
        """
        :param graph: The graph which the nodes and relationships to be merged into.
        :type graph: py2neo.database.Graph
        """
        logging.warning(" The merge_into() is obsolete! Use push_into() instead!"
                        " You can samply replace all merge_into() with push_into().")
        if self.node:
            graph.merge(self.node, 'File', 'path')
        if self.relationships:
            graph.merge(self.relationships, 'Keyword', 'name')

    def push_into(self, graph, update_key=False, delete_node=False):
        """
        Use push_into! Because, you can
            1. specify whether delete the obsolete keys;
            2. specify whether to delete the node with a same path. This is important in editor's saving operation.
        :param graph: The graph which the nodes and relationships to be merged into.
        :param update_key: if True, delete the node's keys which are not in self.keywords
        :param delete_node: if True, delete the node with same path
        """
        # remove the same path's node
        if delete_node:
            delete_file(graph, self.node['path'])

        # delete the original keyword nodes
        if update_key:
            cypher = """
MATCH (f:File)-[r]->(k:Keyword)
WHERE ID(f) = {id}
    WITH r, k
        WHERE NOT k.name IN {keywords}
            DELETE r
            WITH k
                WHERE NOT EXISTS((k) < --())
                    DELETE k""".format(id=self.node.identity, keywords=cypher_repr(list(self.keywords)))
            graph.run(cypher)
            self.merge_into(graph)

        if self.node:
            graph.merge(self.node, 'File', 'path')
        if self.relationships:
            graph.merge(self.relationships, 'Keyword', 'name')

    @staticmethod
    def from_record(record):
        keys = record['keys']
        node = record['f']
        file_node = FileNode(node=node, keywords=set(keys))
        return file_node


def get_files(graph: Graph, keywords=None, file_properties=None) -> List[FileNode]:
    """
    :param graph: The Graph from the database
    :param keywords: The associated keywords
    :param file_properties:
    :return files: The list of files' property
    """
    # Deal with time constraints
    if not keywords:
        keywords = []
    if not file_properties:
        file_properties = {}

    def time_cypher_repr(span):
        begin = 'DATETIME(f.cTime) >= DATETIME("{}")'.format(span[0]) if span[0] is not None else 'TRUE'
        end = 'DATETIME(f.cTime) <= DATETIME("{}")'.format(span[1]) if span[1] is not None else 'TRUE'
        return begin + ' AND ' + end

    cTime_constraint = [time_cypher_repr(span) for span in file_properties['cTime']] \
        if 'cTime' in file_properties else []
    cTime_constraint_cypher = (' AND ' + '({})'.format(' OR '.join(cTime_constraint))) \
        if cTime_constraint != [] else ''
    aTime_constraint = [time_cypher_repr(span) for span in file_properties['aTime']] \
        if 'aTime' in file_properties else []
    aTime_constraint_cypher = (' AND ' + '({})'.format(' OR '.join(aTime_constraint))) \
        if aTime_constraint != [] else ''
    mTime_constraint = [time_cypher_repr(span) for span in file_properties['mTime']] \
        if 'mTime' in file_properties else []
    mTime_constraint_cypher = (' AND ' + '({})'.format(' OR '.join(mTime_constraint))) \
        if mTime_constraint != [] else ''
    constraint_cypher = cTime_constraint_cypher + aTime_constraint_cypher + mTime_constraint_cypher

    # Deal with name constraint
    constraint_cypher += (' AND ' + 'f.name = "{}"'.format(file_properties['name'])) \
        if 'name' in file_properties else ''

    # TODO: size constraint seems to be useless, so I didn't add it

    cypher = """
MATCH (f:File)-->(kw:Keyword)
WHERE kw.name in {keywords} {other_constraint}
    WITH DISTINCT f
        MATCH (f)-->(keys)
        RETURN f, ID(f) AS id, COLLECT(keys.name) AS keys""".format(keywords=cypher_repr(keywords),
                                                                    other_constraint=constraint_cypher)
    result = graph.run(cypher)
    file_nodes = []
    for record in result:
        file_nodes.append(FileNode.from_record(record))
    return file_nodes


def delete_file(graph: Graph, path: str):
    """
    :param graph: The Graph from the database
    :param path: The path of the file to delete
    """
    cypher = """
MATCH (f: File {properties})
    OPTIONAL MATCH (f)-[r: RELATES_TO]->(k:Keyword)
        DELETE r, f
        WITH k
            WHERE NOT EXISTS((k) < --())
                DELETE k""".format(properties=cypher_repr({'path': path}))
    graph.run(cypher)


def rename_file(graph: Graph, old: str, new: str):
    """
    :param graph: The Graph from the database
    :param old: The old path(must be full path)
    :param new: The new path(must be full path)
    """
    if old[0] != '/' or new[0] != '/':
        print('not real path')
        return
    # Remove the original one
    cypher = """
OPTIONAL MATCH (new:File {{path:{new_path}}})
OPTIONAL MATCH (new)-[r: RELATES_TO]->(k:Keyword)
    WITH new, r, k
        DELETE new, r
        WITH k
            WHERE NOT EXISTS((k) < --())
                DELETE k""".format(old_path=cypher_repr(old),
                                   new_name=cypher_repr(os.path.split(new)[1]),
                                   new_path=cypher_repr(new))
    graph.run(cypher)
    delete_file(graph, old)
    # Update
    file_node = FileNode(old)
    file_node.update_info(filename_extension_specified=os.path.splitext(new)[1][1:],
                          other_properties={'path': new,
                                            'name': os.path.split(new)[1]})
    file_node.merge_into(graph)
