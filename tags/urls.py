from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',

    # url(r'^accounts/', include('allauth.urls')),
    # url(r'^$', 'home.views.home', name='home'),

    url(r'^$', 'tags.views.get_all_tags', name='all_tags'),

    url(r'^search_n_tags$', 'tags.views.search_n_tags', name='search_n_tags'),
    url(r'^describe/(?P<slug>[^/]+)/$', 'tags.views.describe_tag', name='describe_tag'),
    url(r'^(?P<slug>[^/]+)/$', 'tags.views.get_tag', name='get_tag'),

)
