from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView


urlpatterns = patterns('',

    url(r'^$', 'inbox.views.inbox', name='inbox'),
    url(r'^sent$', 'inbox.views.outbox', name='outbox'),
    url(r'^inquiries$', 'inbox.views.inquiries', name='inquiries'),
    url(r'^sent_inquiries$', 'inbox.views.sent_inquiries', name='sent_inquiries'),
    url(r'^quotations$', 'inbox.views.quotations', name='quotations'),
    url(r'^sent_quotations$', 'inbox.views.sent_quotations', name='sent_quotations'),
    url(r'^messages$', 'inbox.views.messages', name='messages'),
    url(r'^sent_messages$', 'inbox.views.sent_messages', name='sent_messages'),

    # url(r'^edit/(?P<id>[^/]+)/$', 'forum.views.edit_ques', name='edit_ques'),
)
