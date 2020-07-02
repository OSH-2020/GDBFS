from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django import forms
from django.forms import fields, widgets
import json
from py2neo import *
from . import neobase


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


def submit(request):
    print(request.POST.get("description"))
    graph = Graph("bolt://localhost:7687")
    result = neobase.get_files(graph,
                                 keywords=[request.POST.get("description")])
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
