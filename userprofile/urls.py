from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',

    # url(r'^accounts/', include('allauth.urls')),
    # url(r'^$', 'home.views.home', name='home'),

    url(r'^set_interests/$', 'userprofile.views.set_interests', name='set_interests'),
    url(r'^delete_interest/$', 'userprofile.views.delete_interest', name='delete_interest'),
    url(r'^set_experience/$', 'userprofile.views.set_experience', name='set_experience'),
    url(r'^edit/$', 'userprofile.views.edit', name='edit'),
    url(r'^(?P<username>[^/]+)/$', 'userprofile.views.profile', name='profile'),
    url(r'^check_email/$', 'userprofile.views.check_email', name='check_email'),
    url(r"^check_username/$", 'userprofile.views.check_username', name="check_username"),

)
