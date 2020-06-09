import nltk
from nltk import *
from textblob import TextBlob
"""
I use the following string for test, you can try something more

1. input : photos taken in USTC in September 2019
   output: ['photo', 'USTC','September', '2019']
2. input : a movie directed by Tom Steven
   output: ['movie','Tom Steven']
3. input : big eye cat
   output: ['big eye','cat']
4. input : lab1 of operating system
   output: ['lab1','operating system']
"""
def tree_flatting(tree):
    """
    :param tree: Tree builded by some defined grammar
    :return: A list whose elements are tree's leaves(without tag)
    """
    l = []
    for i in range(0,len(tree)):
        if type(tree[i]) == tuple:
            l.append(tree[i][0])
        else:
            s = ''
            for j in range(0,len(tree[i])):
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
    # I'm not sure "September 2019" should be translated into one or two keywords
    chunkParser  = nltk.RegexpParser(grammar)
    tree = chunkParser.parse(l)
    newlist = tree_flatting(tree)
    return newlist

def list_filter(l):
    """
    :param l: a well-chunked (maybe) list with tag
    :return: a list filted some stopwords and attributes, plural nouns will be 
             converted into the corresponding singular
    """
    grammar = r'''
        VBN: <NNS | NN>{<VBN>}    #case: remove 'taken' in "photo taken in ..."
        IN:  {<IN>}               #remove preposition or subordinating conjunction
        DT:  {<DT>}               #remove deteminer
        '''              
    chunkParser  = nltk.RegexpParser(grammar)
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

def main():
    str = input()
    tree = ne_chunk(pos_tag(word_tokenize(str)))
    l_grammared = add_grammar(pos_tag(tree_flatting(tree)))
    l_filtered = list_filter(pos_tag(l_grammared))
    print(l_filtered)
   

if __name__ == "__main__":
    main()
