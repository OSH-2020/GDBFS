from django.http import JsonResponse
from django.shortcuts import render
from py2neo import *
from core import neobase, UsrInputConv
import os
import tkinter as tk
from tkinter import filedialog
from . import settings


def home(request):
    return render(request, 'home.html')


def gdbfs(request):
    if request.POST.get('path') is None or request.POST.get('path') == '':
        return render(request, 'gdbfs.html', {'mount_path': settings.fuse_process.fuse_obj.mount_point})
    try:
        if type(settings.fuse_process) == settings.FuseProcess:
            settings.fuse_process.terminate()
            print("\n\numounting {}\n\n".format(settings.fuse_process.mount_path))
            os.system("umount {}".format(settings.fuse_process.mount_path))
    except AttributeError:
        pass
    settings.fuse_process = settings.FuseProcess(request.POST.get('path'))
    settings.fuse_process.start()
    return render(request, 'gdbfs.html', {'mount_path': settings.fuse_process.fuse_obj.mount_point})


def rename(request):
    return render(request, 'rename.html')


def return_gdbfs(request):
    return render(request, 'gdbfs.html')


def find_files(request):
    description = request.POST.get("description")
    ctime = request.POST.get("ctime")
    atime = request.POST.get("atime")
    mtime = request.POST.get("mtime")
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
    print("acmtime", search_key.atime, search_key.ctime, search_key.mtime, sep=', ')

    # Get files according to keywords and file_properties -- Wang
    graph = Graph("bolt://localhost:7687")
    result = neobase.get_files(graph,
                               keywords=search_key.keywords,
                               file_properties={'cTime': search_key.ctime,
                                                'aTime': search_key.atime,
                                                'mTime': search_key.mtime})
    if len(result) == 0:
        return JsonResponse({"nodes": [], "edges": []})

    name_dict = neobase.file_nodes_to_d3(result)
    return JsonResponse(name_dict)


def find_files_by_name(request):
    name = request.POST.get('name')
    graph = Graph("bolt://localhost:7687")
    result = neobase.get_files_by_name(graph, name)
    name_dict = neobase.file_nodes_to_d3(result)
    return JsonResponse(name_dict)


def open_file(request):
    path = request.POST.get('path')
    path = neobase.convert_path(path,
                                settings.fuse_process.fuse_obj.root,
                                settings.fuse_process.fuse_obj.mount_point)
    ok = True
    if not os.access(path, os.F_OK):
        ok = False
    os.system("nohup xdg-open {}".format(path))
    return JsonResponse({'ok': ok})


def rm_file(request):
    path = request.POST.get('path')
    path = neobase.convert_path(path,
                                settings.fuse_process.fuse_obj.root,
                                settings.fuse_process.fuse_obj.mount_point)
    os.system("rm {}".format(path))
    return find_files(request)


def rm_node(request):
    path = request.POST.get('path')
    graph = Graph("bolt://localhost:7687")
    ok = True
    if not neobase.delete_file(graph, path):
        ok = False
    return JsonResponse({'ok': ok})


def choose_dir(request):
    root = tk.Tk()
    root.withdraw()
    path = filedialog.askdirectory()
    root.destroy()
    print(path)
    return JsonResponse({'path': path})


def add_files(request):
    root = tk.Tk()
    root.withdraw()
    paths = filedialog.askopenfilenames()
    root.destroy()
    for path in paths:
        full_path = os.path.realpath(settings.fuse_process.fuse_obj.mount_point + '/' + os.path.realpath(path))
        print('\n\n', full_path, '\n\n')
        os.makedirs(os.path.dirname(full_path))
        os.system('cp {} {}'.format(path, full_path))

    return JsonResponse({'paths': paths})


def umount(request):
    print(umount)
    try:
        if type(settings.fuse_process) == settings.FuseProcess:
            settings.fuse_process.terminate()
            os.system("umount {}".format(settings.fuse_process.mount_path))
    except AttributeError:
        pass
    return render(request, 'home.html')


def add_folder(request):
    root = tk.Tk()
    root.withdraw()
    path = filedialog.askdirectory()
    root.destroy()
    os.system('cp -r {} {}'.format(path, settings.fuse_process.fuse_obj.mount_point))
    return JsonResponse({'paths': path})
