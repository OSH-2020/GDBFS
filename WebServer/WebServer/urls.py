from django.conf.urls import url
from django.urls import path
from WebServer import views

urlpatterns = [
    url(r'^home$', views.home),
    url(r'^gdbfs$', views.gdbfs),
    url(r'^find_files$', views.find_files, name='find_files'),
    url(r'^open_file$', views.open_file, name='open_file'),
    url(r'^choose_dir$', views.choose_dir, name='choose_dir'),
    url(r'^umount$', views.umount, name='umount'),
]
