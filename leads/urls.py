from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
from . import views

urlpatterns = [

    url(r'^$', views.leads, name='leads'),
    url(r'^edit_add/(?P<slug>[^/]+)/$', views.edit_add_lead, name='edit_add'),

    url(r'^close/(?P<id>[^/]+)/$', views.close_lead, name='close'),
    url(r'^pre_edit_reply/(?P<id>[^/]+)/$', views.pre_edit_reply, name='pre_edit_reply'),
    url(r'^edit_reply/(?P<id>[^/]+)/$', views.edit_reply, name='edit_reply'),
    url(r'^reply/$', views.reply_lead, name='reply'),

    url(r'^send_quotation/$', views.send_quotation, name='send_quotation'),

    url(r'^reply/accept/(?P<id>[^/]+)/$', views.accept_reply, name='accept_reply'),
    url(r'^reply/delete/(?P<id>[^/]+)/$', views.delete_tag, name='delete_tag'),
    url(r'^(?P<slug>[^/]+)/$', views.get_lead, name='lead'),
    # url(r'^edit/(?P<id>[^/]+)/$', 'forum.views.edit_ques', name='edit_ques'),
]
