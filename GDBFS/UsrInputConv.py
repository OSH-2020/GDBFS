import nltk
from nltk import *
import click
import time
import calendar
import datetime
from datetime import datetime,timedelta

'''
TODO: "weekend","last Sunday","last September"
TODO: size 
TODO: last year/month yesterday in case first day
'''


class KeyWord:
    def __init__(self, keywords, atime,ctime,mtime):
        self.keywords = keywords
        self.atime = atime
        self.ctime = ctime
        self.mtime = mtime


@click.command()
@click.argument('yourkey')
@click.option('--atime', default='None', help="access time of your file")
@click.option('--ctime', default='None', help="create time of your file")
@click.option('--mtime', default='None', help="modify time of your file")
def main(yourkey,atime,ctime,mtime):
    tree = ne_chunk(pos_tag(word_tokenize(yourkey)))
    l_grammared = add_grammar(pos_tag(tree_flatting(tree)))
    l_filtered = list_filter(pos_tag(l_grammared))
    atime_period = time_top(atime)
    ctime_period = time_top(ctime)
    mtime_period = time_top(mtime)
    searchkey = KeyWord(l_filtered, atime_period, ctime_period, mtime_period)
    #print('keywords: ',searchkey.keywords)
    #print('atime:    ',searchkey.atime)
    #print('ctime:    ',searchkey.ctime)
    #print('mtime:    ',searchkey.mtime)
    return searchkey

def time_top(str):
    if(str != 'None'):
        time_list = pos_tag(word_tokenize(str))
    else:
        time_list = ['None']
    time_tu = time_process(time_list)

    l = []
    for i in range(0, len(time_tu[0])):
        newrange = datetime.strftime(time_tu[0][i], '%Y-%m-%dT%H:%M:%S') + ' - ' 
        newrange += datetime.strftime(time_tu[1][i], '%Y-%m-%dT%H:%M:%S')
        l.append(newrange)
    return l


def tree_flatting(tree):
    """
    :param tree: Tree builded by some defined grammar
    :return: A list whose elements are tree's leaves(without tag)
    """
    l = []
    for i in range(0, len(tree)):
        if type(tree[i]) == tuple:
            l.append(tree[i][0])
        else:
            s = ''
            for j in range(0, len(tree[i])):
                s += tree[i][j][0]
                s += ' '
            s = s[0:len(s)-1]
            l.append(s)
    return l


def add_grammar(l):
    """
    :param l: a list with tag but just chunked by ne_chunk (a classifier to identify named entities)
    :return: a list with more customized grammar (without tag)
    """
    grammar = r'''
        NP: {<JJ>+<NN>}     # add this for case "big eye"
            {<NN>{2,}}      # add this for case "operating system"
        '''
    chunkParser = nltk.RegexpParser(grammar)
    tree = chunkParser.parse(l)
    newlist = tree_flatting(tree)
    return newlist


def list_filter(l):
    """
    :param l: a well-chunked (maybe) list with tag
    :return: a list filted some stopwords and attributes, plural nouns will
             be converted into the corresponding singular
    """
    grammar = r'''
        VBN: <NNS | NN>{<VBN>} #case: remove 'taken' in "photo taken in ..."
        IN:  {<IN>}            #remove preposition or subordinating conjunction
        DT:  {<DT>}            #remove deteminer
        CC:  {<CC>}
        '''
    chunkParser = nltk.RegexpParser(grammar)
    tree = chunkParser.parse(l)
    wnl = WordNetLemmatizer()
    # we change NNS into correspnding NN
    filtered_list = []
    for i in range(0,len(tree)):
        if type(tree[i]) == tuple:
            if(tree[i][1] == 'NNS'):
                filtered_list.append(wnl.lemmatize(tree[i][0]))
            else:
                filtered_list.append(tree[i][0])
    return filtered_list


def ismonth(str):
    if str in calendar.month_name[1:13]:
        return list(calendar.month_name).index(str)
    else:
        return 0


def time_process(timelist):
    num = 0
    month_num = 0   # default flag
    rela_flag = 0   # relatively time flag 
    endtime = []
    begintime = []
    endtime.append(datetime.now())
    nt = endtime[0]
    if(timelist[0] == 'None'):
        begintime.append(datetime(nt.date().year - 3, nt.date().month, 
                                  nt.date().day, 0, 0, 0))
    else:
        for i in range(0, len(timelist)):
            # means month
            if(timelist[i][1] == 'NNP'):  
                month_num = ismonth(timelist[i][0])
                if(month_num  == 0):
                    print("TimeTypeError:time will be set as default")
                    begintime.append(datetime(nt.date().year - 3, nt.date().month, 
                                              nt.date().day, 0, 0, 0))
                    break
            # means 'this'
            elif(timelist[i][1] == 'DT'):    
                if(timelist[i + 1][0] == 'year'):
                    rela_flag = 1
                elif(timelist[i + 1][0] == 'month'):
                    rela_flag = 2
                else:
                    print("TimeTypeError:time will be set as default")
                    begintime.append(datetime(nt.date().year - 3, nt.date().month, 
                                              nt.date().day, 0, 0, 0))
                    break
            # means 'last'
            elif(timelist[i][1] == 'JJ'):    
                if(timelist[i + 1][0] == 'year'):
                    rela_flag = 3
                elif(timelist[i + 1][0] == 'month'):
                    rela_flag = 4
                else:
                    print("TimeTypeError:time will be set as default")
                    begintime.append(datetime(nt.date().year - 3, nt.date().month, 
                                              nt.date().day, 0, 0, 0))
                    break
            # 'yesterday'?
            elif(timelist[i][1] == 'NN'):
                if(timelist[i][0] == 'yesterday'):
                    begintime.append(datetime(nt.date().year, nt.date().month, 
                                              nt.date().day - 1, 0, 0, 0))
                    endtime.pop(0)
                    endtime.append(datetime(nt.date().year, nt.date().month, 
                                              nt.date().day - 1, 23, 59, 59))
                elif(timelist[i][0] == 'year' or timelist[i][0] == 'month'):
                    pass
                else:
                    print("TimeTypeError:time will be set as default")
                    begintime.append(datetime(nt.date().year - 3, nt.date().month, 
                                              nt.date().day, 0, 0, 0))
                    break
            else:
                continue
    # Now process the list
    if(rela_flag == 1):
        begintime.append(datetime(nt.date().year, 1, 1, 0, 0, 0))
    elif(rela_flag == 2):
        begintime.append(datetime(nt.date().year, nt.date().month, 1, 0, 0, 0))
    elif(rela_flag == 3):
        begintime.append(datetime(nt.date().year - 1, 1, 1, 0, 0, 0))
        endtime.pop(0)
        endtime.append(datetime(nt.date().year - 1, 12, 31, 23, 59, 59))
    elif(rela_flag == 4):
        begintime.append(datetime(nt.date().year, nt.date().month - 1, 1, 0, 0, 0))
        endtime.pop(0)
        endtime.append(datetime(nt.date().year, nt.date().month - 1,
                                calendar.monthrange(nt.date().year, 
                                                    nt.date().month - 1)[1],
                                23, 59, 59))
    elif(len(begintime) == 0):
        begintime.append(datetime(nt.date().year - 3, nt.date().month, 
                                  nt.date().day, 0, 0, 0))
    # Now process specific month
    if(month_num != 0):
        bt_month = datetime(begintime[0].date().year, month_num, 1, 0, 0, 0)
        endyear = endtime[0].date().year
        begintime.pop(0)
        endtime.pop(0)
        for i in range(bt_month.date().year, endyear + 1):
            begintime.append(datetime(i, month_num, 1, 0, 0, 0))
            endtime.append(datetime(i, month_num, 
                                    calendar.monthrange(bt_month.date().year, 
                                               bt_month.date().month)[1],
                                    23, 59, 59))
    return (begintime,endtime)


if __name__ == "__main__":
    main()
