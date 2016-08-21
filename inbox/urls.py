from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
from . import views, unified


urlpatterns = [

    url(r'^$', views.inbox, name='inbox'),
    url(r'^sent/$', views.outbox, name='outbox'),
    url(r'^inquiries$', views.inquiries, name='inquiries'),
    url(r'^sent_inquiries$', views.sent_inquiries, name='sent_inquiries'),
    url(r'^quotations$', views.quotations, name='quotations'),
    url(r'^sent_quotations$', views.sent_quotations, name='sent_quotations'),
    url(r'^messages$', views.messages, name='messages'),
    url(r'^sent_messages$', views.sent_messages, name='sent_messages'),
    url(r'^mark_seen$', views.mark_seen, name='mark_seen'),
    url(r'^enquire/$', unified.enquire, name='unified_enquire'),


    # url(r'^edit/(?P<id>[^/]+)/$', 'forum.views.edit_ques', name='edit_ques'),
]
