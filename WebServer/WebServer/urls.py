from django.conf.urls import url
from django.urls import path
from WebServer import views

urlpatterns = [
    url(r'^index$', views.index),
    url(r'^find_files$', views.find_files, name='find_files'),
]
