#!/usr/bin/python
#coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

from django.conf.urls import patterns, url

from polls import views
urlpatterns = patterns('',
    # ex: /polls/
    url(r'^$', views.index, name='index'),
    # ex: /polls/5/
    # the 'name' value as called by the {% url %} template tag  
    # "{% url 'detail' question.id  %}"
    url(r'^(?P<question_id>\d+)/$', views.detail, name='detail'),
    # ex: /polls/5/results/
    url(r'^(?P<question_id>\d+)/results/$', views.results, name='results'),
    # ex: /polls/5/vote/
    url(r'^(?P<question_id>\d+)/vote/$', views.vote, name='vote'),
)
