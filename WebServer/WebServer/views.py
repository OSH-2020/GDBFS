from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django import forms
from django.forms import fields, widgets
import json
from py2neo import *
from . import neobase
from . import UsrInputConv


# Create your views here. 
def index(request):
    return render(request, 'index.html')


def add(request):
    a = request.GET.get('a', 0)
    b = request.GET.get('b', 0)
    c = int(a) + int(b)
    return HttpResponse(str(c))


def ajax_list(request):
    a = list(range(10))
    # return HttpResponse(json.dump(a), content_type='application/json')
    return JsonResponse(a, safe=False)


def find_files(request):
    print(request.POST.get("description").__class__)
    description = request.POST.get("description")
    ctime = request.POST.get("ctime")
    atime = request.POST.get("atime")
    mtime = request.POST.get("mtime")
    print("description", description)
    print("acmtime", atime, ctime, mtime)
    # Get usr's input -- Gao
    l_grammared = UsrInputConv.add_grammar(
        UsrInputConv.pos_tag(
            UsrInputConv.tree_flatting(
                UsrInputConv.ne_chunk(
                    UsrInputConv.pos_tag(
                        UsrInputConv.word_tokenize(description))))))
    l_filtered = UsrInputConv.list_filter(UsrInputConv.pos_tag(l_grammared))
    atime_period = UsrInputConv.time_top(atime)
    ctime_period = UsrInputConv.time_top(ctime)
    mtime_period = UsrInputConv.time_top(mtime)
    search_key = UsrInputConv.KeyWord(l_filtered, atime_period, ctime_period, mtime_period)
    print('keywords: ', search_key.keywords)
    print('atime:    ', search_key.atime)
    print('ctime:    ', search_key.ctime)
    print('mtime:    ', search_key.ctime)

    # Get files according to keywords and file_properties -- Wang
    graph = Graph("bolt://localhost:7687")
    result = neobase.get_files(graph,
                               keywords=search_key.keywords,
                               file_properties={'cTime': search_key.ctime,
                                                'aTime': search_key.atime,
                                                'mTime': search_key.mtime})
    if len(result) == 0:
        return JsonResponse({"nodes": [], "edges": []})

    print(result[0].node)
    print(result[0].keywords)

    nodes = []
    node_indexes = {}
    edges = []
    node_count = 0
    for file_node in result:
        nodes.append({'name': file_node.node['name'], 'label': 'File'})
        node_indexes[file_node.node['path']] = node_count
        node_count += 1
        for keyword in file_node.keywords:
            if keyword not in nodes:
                nodes.append({'name': keyword, 'label': 'Keyword'})
                node_indexes[keyword] = node_count
                node_count += 1
            edges.append({'source': node_indexes[file_node.node['path']],
                          'target': node_indexes[keyword],
                          'relation': 'TO',
                          'value': 1})

    name_dict = {"nodes": nodes, "edges": edges}
    return JsonResponse(name_dict)
