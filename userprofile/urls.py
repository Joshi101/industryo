from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',

    # url(r'^accounts/', include('allauth.urls')),
    # url(r'^$', 'home.views.home', name='home'),

    url(r'^set_skills/$', 'userprofile.views.set_skills', name='set_skills'),
    url(r'^(?P<slug>[^/]+)/$', 'userprofile.views.profile', name='profile'),


)
