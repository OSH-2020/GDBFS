import py2neo
from py2neo import *
from py2neo.ogm import *
import os
import time
from api_extension import api_top


class FileNode:
    RELATES_TO = Relationship.type('RELATES_TO')

    def __init__(self, file_path, label="File", other_keywords=None, other_properties=None):
        """
        :param file_path: The full path of the file.
        :type file_path: str
        :param other_keywords: The other keywords needed to be added.
        :type other_keywords: list(str)
        :param label: The label for this node. 'File' by default
        :type label: str
        :param other_properties: A dict indicating the other properties needed to be specified. None by default
        :type other_properties: dict
        """
        self.file_path = file_path
        file_info = api_top.get_keywords_properties(file_path, 5)
        self.keywords = list(set(file_info['keywords']) | set(other_keywords if other_keywords is not None else []))
        self.node = self.file_to_node(file_path, label, other_properties=file_info['properties'])
        self.subgraph, self.keyword_nodes = self.get_subgraph

    def merge_into(self, graph):
        """
        :param graph: The graph which the nodes and relationships to be merged into.
        :type graph: py2neo.database.Graph
        """
        print(self.node)
        graph.merge(self.node, 'File', 'name')
        graph.merge(self.keyword_nodes, 'Keyword', 'name')
        graph.merge(self.subgraph)

    @property
    def get_subgraph(self):
        """
        :return subgraph: The subgraph of keywords nodes, file node and the corresponding relationships
        :rtype subgraph: py2neo.data.Subgraph
        :return Subgraph(keyword_nodes): The keyword_nodes as the class 'Subgraph'
        :rtype Subgraph(keyword_nodes): py2neo.data.Subgraph
        """
        subgraph = self.node
        if not self.keywords:
            return subgraph
        # Here we always use 'name' to identify the nodes,
        # because it'll be printed by default
        keyword_nodes = [Node('Keyword', name=keyword) for keyword in self.keywords]
        for kw_node in keyword_nodes:
            subgraph |= FileNode.RELATES_TO(self.node, kw_node)
        return subgraph, Subgraph(keyword_nodes)

    @staticmethod
    def file_to_node(file_path, label='File', other_properties=None):
        """
        :param file_path: The full path of the file.
        :type file_path: str
        :param label: The label for this node. 'File' by default
        :type label: str
        :param other_properties: A dict indicating the other properties need to be specified. None by default
        :type other_properties: dict
        :return node: The node of the file.
        :rtype node: py2neo.data.Node
        """
        if other_properties is None:
            other_properties = {}
        properties = {}
        # properties = FileNode.get_property(file_path)
        properties.update(other_properties)
        node = Node(label, **properties)
        return node

def get_files(graph: Graph, keywords: list, file_properties: dict) -> list:
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
RETURN DISTINCT f""".format(keywords=cypher_repr(keywords),
                            other_constraint=constraint_cypher)
    print(cypher)
    files = graph.run(cypher)
    import pprint
    pprint.pprint(files.data())
    return files
