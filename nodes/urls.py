from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',

    # url(r'^accounts/', include('allauth.urls')),
    # url(r'^$', 'home.views.home', name='home'),

    url(r'^upload/$', 'nodes.views.upload_image', name='upload'),
    url(r'^set_logo/$', 'nodes.views.set_logo', name='set_logo'),
    url(r'^set_profile_image/$', 'nodes.views.set_profile_image', name='set_profile_image'),


)
