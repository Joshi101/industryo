from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView


urlpatterns = patterns('',

    url(r'^$', 'leads.views.leads', name='leads'),
    url(r'^edit_add/(?P<slug>[^/]+)/$', 'leads.views.edit_add_lead', name='edit_add'),

    url(r'^close/$', 'leads.views.close_lead', name='close'),
    url(r'^reply/$', 'leads.views.reply', name='reply'),
    url(r'^(?P<slug>[^/]+)/$', 'leads.views.get_lead', name='lead'),
    # url(r'^edit/(?P<id>[^/]+)/$', 'forum.views.edit_ques', name='edit_ques'),
)
