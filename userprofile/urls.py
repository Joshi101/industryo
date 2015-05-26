from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',

    # url(r'^accounts/', include('allauth.urls')),
    # url(r'^$', 'home.views.home', name='home'),

    url(r'^set_interests/$', 'userprofile.views.set_interests', name='set_interests'),
    url(r'^(?P<username>[^/]+)/$', 'userprofile.views.profile', name='profile'),


)
