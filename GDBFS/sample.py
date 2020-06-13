"""
All test codes can be put here.
"""
import neobase
import logging
import py2neo
from py2neo import *


def test_py2neo():
    # Set log format
    logging.basicConfig(format='%(asctime)s - : %(message)s',
                        level=logging.INFO)
    # Log the version of py2neo
    logging.info('The version of your py2neo is: {}'.format(py2neo.__version__))

    # connect to the database
    g = Graph("bolt://localhost:7687")
    logging.info('Connected to a graph:\n{}'.format(g))

    # Here is a sample for FileNode
    n = neobase.FileNode(r'sample_files/neo4j.txt')
    n.merge_into(g)

    # Get files according to keywords and file_properties
    neobase.get_files(g, keywords=['graph', 'database', 'neo4j'], file_properties={'cTime': [('2020-06-10', '2021-06-10')]})


if __name__ == "__main__":
    test_py2neo()
