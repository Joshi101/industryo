from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',

    # url(r'^accounts/', include('allauth.urls')),
    # url(r'^$', 'home.views.home', name='home'),


    url(r'^set_about/$', 'workplace.views.set_about', name='set_about'),
    url(r'^set_tags/$', 'workplace.views.set_tags', name='set_tags'),
    url(r'^set_capabilities/$', 'workplace.views.set_capabilities', name='set_capabilities'),
    url(r'^set_product_details/$', 'workplace.views.set_product_details', name='set_product_details'),
    url(r'^(?P<slug>[^/]+)/$', 'workplace.views.workplace_profile', name='workplace_profile'),
    url(r'^get_top_scorers/(?P<slug>[^/]+)/$', 'workplace.views.get_top_scorers', name='get_top_scorers'),

)
