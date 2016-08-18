from django.conf.urls import include, url
from django.contrib import admin
from . import views
from workplace import views as workplace_views

urlpatterns = [

    # url(r'^accounts/', include('allauth.urls')),
    # url(r'^$', 'home.views.home', name='home'),

    url(r'^set_o/(?P<username>[^/]+)/$', workplace_views.set_others_wp, name='set_o'),

    url(r'^set_interests/$', views.set_interests, name='set_interests'),
    url(r'^delete_interest/$', views.delete_interest, name='delete_interest'),
    url(r'^set_experience/$', views.set_experience, name='set_experience'),
    url(r'^edit/$', views.edit, name='edit'),
    url(r'^check_email/$', views.check_email, name='check_email'),
    url(r"^check_username/$", views.check_username, name="check_username"),
    url(r'^(?P<username>[^/]+)/$', views.profile, name='profile'),
]
