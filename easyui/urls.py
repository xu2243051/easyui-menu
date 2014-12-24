#!/usr/bin/python
#coding:utf-8
from django.conf.urls import patterns, url

from .views import logout_view, LoginView, HomeView, get_url, success

urlpatterns = patterns('',
    url(r'^home/$', HomeView.as_view(), name='home'),
    url(r'^success/$', success, name='success'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', logout_view, name='logout'),
    url(r'(?i)get_url/$', get_url, name='get_url'),
)
from easyui.utils import register_views
urlpatterns = register_views('easyui.views', 'views', urlpatterns)
