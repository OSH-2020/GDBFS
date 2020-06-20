"""
All test codes can be put here.
"""
import neobase
from pprint import pprint
import os
from py2neo import *


def test_create_file_node():
    print("------------------------------------------test_create_file_node()------------------------------------------")
    graph = Graph("bolt://localhost:7687")
    # Here is a sample for FileNode
    neo4j_txt = neobase.FileNode(r'sample_files/neo4j.txt')
    neo4j_txt.update_info(other_keywords=['neo4j'])
    neo4j_txt.merge_into(graph)
    pprint(neo4j_txt)
    print('id: ', str(neo4j_txt.identity))
    # Invoking the picture extractor takes lots of time. So comment it out.
    '''
    cat_jpeg = neobase.FileNode(r'sample_files/cat.jpeg')
    cat_jpeg.update_info()
    cat_jpeg.merge_into(graph)
    pprint(cat_jpeg)
    '''


def test_get_files():
    print("---------------------------------------------test_get_files()---------------------------------------------")
    graph = Graph("bolt://localhost:7687")
    # Get files according to keywords and file_properties
    neo4jtxt = neobase.get_files(graph,
                                 keywords=['graph', 'database', 'neo4j'],
                                 file_properties={'cTime': [('2018-06-10', '2019-06-10'),
                                                            ('2020-06-10', '2021-06-10')]})
    for f in neo4jtxt:
        pprint(f)
        print('id: ', str(f.identity))
    cat_files = neobase.get_files(graph,
                                  keywords=['cat'],
                                  file_properties={'cTime': [('2020-06-10', '2021-06-10')]})
    for f in cat_files:
        pprint(f)
        print('id: ', str(f.identity))


def test_delete_file():
    print("--------------------------------------------test_delete_file()--------------------------------------------")
    graph = Graph("bolt://localhost:7687")
    neobase.delete_file(graph, os.path.realpath('sample_files/neo4j.txt'))


def test_rename_file():
    print("--------------------------------------------test_rename_file()--------------------------------------------")
    graph = Graph("bolt://localhost:7687")
    neobase.rename_file(graph, '/hehe', '/haha')


if __name__ == "__main__":
    # test_create_file_node()
    # test_get_files()
    # test_delete_file()
    test_rename_file()
