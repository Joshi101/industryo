from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView


urlpatterns = patterns('',

    url(r'^$', 'inbox.views.inbox', name='inbox'),
    url(r'^inquiries$', 'inbox.views.inquiries', name='inquiries'),
    url(r'^quotations$', 'inbox.views.quotations', name='quotations'),
    url(r'^messages$', 'inbox.views.messages', name='messages'),

    # url(r'^edit/(?P<id>[^/]+)/$', 'forum.views.edit_ques', name='edit_ques'),
)
