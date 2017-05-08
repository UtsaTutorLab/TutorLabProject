# -*- coding: utf-8 -*-

from django.conf.urls import url
from . import views

app_name='messenger'
urlpatterns = [
    #url(r'^(?P<label>[\w-]{,50})/$', views.chat_room , name="msg"),
    
    url(r'^(?P<label>[A-z]{3}[0-9]{3})/$', views.gen_token , name="msg"),
    url(r'^(?P<token>[\w\-:]+)/$', views.chat_room, name="room"),
]
