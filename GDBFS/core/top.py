from py2neo import *
from . import neobase
from .api_extension import api_top
from pprint import pprint
import os
from .UsrInputConv import *


@click.command()
@click.argument('yourkey')
@click.option('--atime', default='None', help="access time of your file")
@click.option('--ctime', default='None', help="create time of your file")
@click.option('--mtime', default='None', help="modify time of your file")
def main(yourkey, atime, ctime, mtime):
    # initial the database and put my sample into it for the following tests
    graph = Graph("bolt://localhost:7687")
    # Here is a sample for FileNode
    neo4j_txt = neobase.FileNode(r'sample_files/neo4j.txt')
    neo4j_txt.update_info(other_keywords={'neo4j'})
    neo4j_txt.push_into(graph)
    # Note that this picture processing costs much time.
    '''
    cat_jpeg = neobase.FileNode(r'sample_files/cat.jpg')
    cat_jpeg.update_info()
    cat_jpeg.push_into(graph)
    '''

    # Get usr's input -- Gao
    l_grammared = add_grammar(pos_tag(tree_flatting(ne_chunk(pos_tag(word_tokenize(yourkey))))))
    l_filtered = list_filter(pos_tag(l_grammared))
    atime_period = time_top(atime)
    ctime_period = time_top(ctime)
    mtime_period = time_top(mtime)
    search_key = KeyWord(l_filtered, atime_period, ctime_period, mtime_period)
    print('keywords: ', search_key.keywords)
    print('atime:    ', search_key.atime)
    print('ctime:    ', search_key.ctime)
    print('mtime:    ', search_key.ctime)

    # Get files according to keywords and file_properties -- Wang
    graph = Graph("bolt://localhost:7687")
    neo4jtxt = neobase.get_files(graph,
                                 keywords=search_key.keywords,
                                 file_properties={'cTime': search_key.ctime,
                                                  'aTime': search_key.atime,
                                                  'mTime': search_key.mtime})
    pprint("We've found this for you:")
    if len(neo4jtxt) == 0:
        print("Nothing Found")
    else:
        pprint(neo4jtxt[0].node)


if __name__ == '__main__':
    main()
