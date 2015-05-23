from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',

    # url(r'^accounts/', include('allauth.urls')),
    # url(r'^$', 'home.views.home', name='home'),

    url(r'^search_workplace/$', 'workplace.views.search_workplace', name='search_workplace'),
    url(r'^set_segment/$', 'workplace.views.set_segment', name='set_segment'),
    url(r'^edit/$', 'workplaceprofile.views.edit_workplace_profile', name='edit'),
    url(r'^(?P<slug>[^/]+)/$', 'workplace.views.workplace_profile', name='workplace_profile'),

)
