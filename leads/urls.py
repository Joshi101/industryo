from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView


urlpatterns = patterns('',

    url(r'^$', 'leads.views.leads', name='leads'),
    url(r'^edit_add/(?P<slug>[^/]+)/$', 'leads.views.edit_add_lead', name='edit_add'),

    url(r'^close/(?P<id>[^/]+)/$', 'leads.views.close_lead', name='close'),
    url(r'^pre_edit_reply/(?P<id>[^/]+)/$', 'leads.views.pre_edit_reply', name='pre_edit_reply'),
    url(r'^edit_reply/(?P<id>[^/]+)/$', 'leads.views.edit_reply', name='edit_reply'),
    url(r'^reply/$', 'leads.views.reply_lead', name='reply'),

    url(r'^send_quotation/$', 'leads.views.send_quotation', name='send_quotation'),

    url(r'^reply/accept/(?P<id>[^/]+)/$', 'leads.views.accept_reply', name='accept_reply'),
    url(r'^reply/delete/(?P<id>[^/]+)/$', 'leads.views.delete_tag', name='delete_tag'),
    url(r'^(?P<slug>[^/]+)/$', 'leads.views.get_lead', name='lead'),
    # url(r'^edit/(?P<id>[^/]+)/$', 'forum.views.edit_ques', name='edit_ques'),
)
