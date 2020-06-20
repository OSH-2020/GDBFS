import py2neo
from py2neo import *
from py2neo.ogm import *
from api_extension import api_top
from typing import List
import os


class FileNode(Node):
    RELATES_TO = Relationship.type('RELATES_TO')

    def __init__(self, file_path, keywords=None, labels=None, properties=None, auto_update=False):
        """
        :param file_path: The full path of the file.
        :type file_path: str
        :param keywords: The other keywords needed to be added.
        :type keywords: list(str)
        :param labels: The list of labels for this node. 'File' by default
        :type labels: list
        :param properties: A dict indicating the other properties needed to be specified. None by default
        :type properties: dict
        :param auto_update: Whether update the file's info according to given path
        :type auto_update: bool
        """
        labels = ('File',) if labels is None else set(labels)
        self.keywords = [] if keywords is None else keywords
        self.properties = {} if properties is None else properties
        if auto_update:
            self.update_info()
        super(FileNode, self).__init__(*labels, **self.properties)
        self.file_path = file_path
        self.node_with_keynodes = None
        self.keyword_nodes = None
        self.update_node_with_keynodes()

    def merge_into(self, graph):
        """
        :param graph: The graph which the nodes and relationships to be merged into.
        :type graph: py2neo.database.Graph
        """
        graph.merge(self, 'File', 'path')
        if self.keyword_nodes is not None:
            graph.merge(self.keyword_nodes, 'Keyword', 'name')
        if self.node_with_keynodes is not None:
            graph.merge(self.node_with_keynodes)

    def update_node_with_keynodes(self):
        """
        update node_with_keynodes
        """
        subgraph = self
        if not self.keywords:
            return subgraph
        # Here we always use 'name' to identify the nodes,
        # because it'll be printed by default
        keyword_nodes = [Node('Keyword', name=keyword) for keyword in self.keywords]
        for kw_node in keyword_nodes:
            subgraph |= FileNode.RELATES_TO(self, kw_node)
        self.node_with_keynodes = subgraph
        self.keyword_nodes = Subgraph(keyword_nodes)

    def update_info(self, keys_limit=5, other_keywords=None, other_properties=None, filename_extension_specified=None):
        """
        :param filename_extension_specified: specify the file type
        :type filename_extension_specified: str
        :param keys_limit: limit of keywords
        :type keys_limit: int
        :param other_keywords: Other keywords needed to be added
        :type other_keywords: list
        :param other_properties: A dict indicating the other properties need to be specified. None by default
        :type other_properties: dict
        :return node: The node of the file.
        :rtype node: py2neo.data.Node
        """
        if other_properties is None:
            other_properties = {}
        file_info = api_top.get_keywords_properties(self.file_path, keys_limit, filename_extension_specified)
        self.keywords = list(set(file_info['keywords'])
                             | set(other_keywords if other_keywords is not None else []))
        self.properties.update(file_info['properties'])
        self.properties.update(other_properties)
        super(FileNode, self).__init__(*self.labels, **self.properties)
        self.update_node_with_keynodes()

    @staticmethod
    def from_record(record):
        keys = record['keys']
        node = record.to_subgraph()
        file_node = FileNode(file_path=node['path'],
                             properties=dict(node),
                             keywords=keys)
        file_node.__dict__.update(node.__dict__)
        return file_node


def get_files(graph: Graph, keywords: list, file_properties: dict) -> List[FileNode]:
    """
    :param graph: The Graph from the database
    :param keywords: The associated keywords
    :param file_properties:
    :return files: The list of files' property
    """
    # Deal with time constraints
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
    # print(cypher)
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
