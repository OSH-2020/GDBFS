from django.conf.urls import url
from django.urls import path
from WebServer import views

urlpatterns = [
    url(r'^home$', views.home),
    url(r'^gdbfs$', views.gdbfs),
    path('rename/', views.rename, name='rename'),
    path('gdbfs/', views.return_gdbfs, name='return_gdbfs'),
    url(r'^find_files$', views.find_files, name='find_files'),
    url(r'^find_files_by_name$', views.find_files_by_name, name='find_files_by_name'),
    url(r'^open_file$', views.open_file, name='open_file'),
    url(r'^add_files$', views.add_files, name='add_files'),
    url(r'^rm_file$', views.rm_file, name='rm_file'),
    url(r'^choose_dir$', views.choose_dir, name='choose_dir'),
    url(r'^umount$', views.umount, name='umount'),
    url(r'^add_folder$', views.add_folder, name='add_folder'),
]
