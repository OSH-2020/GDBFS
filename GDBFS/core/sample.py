"""
All test codes can be put here.
"""
from . import neobase
from pprint import pprint
import os
from py2neo import *


def test_create_file_node():
    print("------------------------------------------test_create_file_node()------------------------------------------")
    graph = Graph("bolt://localhost:7687")
    # Here is a sample for FileNode
    neo4j_txt = neobase.FileNode(r'sample_files/neo4j.txt')
    neo4j_txt.update_info(other_keywords=['neo4j'])
    neo4j_txt.push_into(graph)
    pprint(neo4j_txt.node)
    pprint(neo4j_txt.keywords)
    pprint(neo4j_txt.keyword_nodes)
    pprint(neo4j_txt.relationships)
    print('id: ', str(neo4j_txt.node.identity))
    # Invoking the picture extractor takes lots of time. So comment it out.

    cat_jpeg = neobase.FileNode(r'sample_files/cat.jpg')
    cat_jpeg.update_info()
    cat_jpeg.push_into(graph)
    pprint(cat_jpeg)



def test_get_files():
    print("---------------------------------------------test_get_files()---------------------------------------------")
    graph = Graph("bolt://localhost:7687")
    # Get files according to keywords and file_properties
    neo4jtxt = neobase.get_files(graph,
                                 keywords=['graph', 'database', 'neo4j'],
                                 file_properties={'cTime': [('2018-06-10', '2019-06-10'),
                                                            ('2020-06-10', '2021-06-10')]})
    for f in neo4jtxt:
        pprint(f.node)
        print('id: ', f.node.identity)
    cat_files = neobase.get_files(graph,
                                  keywords=['cat'],
                                  file_properties={'cTime': [('2020-06-10', '2021-06-10')]})
    for f in cat_files:
        pprint(f.node)
        print('id: ', f.node.identity)

    # You can also modify the properties just by [], like this,
    neo4jtxt[0].node['path'] = os.path.realpath('sample_files/neo4j.txt')
    neo4jtxt[0].keywords.discard('neo4j')
    print(neo4jtxt[0].node)
    neo4jtxt[0].push_into(graph, update_key=True)

    cat_files[0].node['name'] = 'I am cat!'
    cat_files[0].keywords.add('mao mi')
    cat_files[0].update_relationships()
    cat_files[0].push_into(graph, update_key=True)
    print(cat_files[0].node)


def test_delete_file():
    print("--------------------------------------------test_delete_file()--------------------------------------------")
    graph = Graph("bolt://localhost:7687")
    neobase.delete_file(graph, os.path.realpath('sample_files/neo4j.txt'))


def test_rename_file():
    print("--------------------------------------------test_rename_file()--------------------------------------------")
    graph = Graph("bolt://localhost:7687")
    neobase.rename_file(graph, os.path.realpath('sample_files/neo4j.txt'),
                        os.path.realpath('sample_files/neo4j2.txt'))


if __name__ == "__main__":
    test_create_file_node()
    # test_get_files()
    # test_delete_file()
    # test_rename_file()
    pass
