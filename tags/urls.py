from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',

    # url(r'^accounts/', include('allauth.urls')),
    # url(r'^$', 'home.views.home', name='home'),

    url(r'^$', 'tags.views.get_all_tags', name='all_tags'),
    url(r'^(?P<slug>[^/]+)/$', 'tags.views.get_tag', name='get_tag'),

)
