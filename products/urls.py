from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',

    # url(r'^accounts/', include('allauth.urls')),
    # url(r'^$', 'home.views.home', name='home'),

    url(r'^random/$', 'products.views.random', name='random'),
    url(r'^delete/$', 'products.views.delete', name='delete'),
    url(r'^add_product/$', 'products.views.add_product', name='add_product'),
    url(r'^enquire/$', 'products.views.enquire', name='enquire'),
    url(r'^(?P<id>[^/]+)/edit_desc/$', 'products.views.edit_desc', name='edit_desc'),
    url(r'^(?P<id>[^/]+)/change_image/$', 'products.views.change_image', name='change_image'),
    url(r'^(?P<slug>[^/]+)/$', 'products.views.product', name='product'),
    url(r'^(?P<slug>[^/]+)/set_tags_short/$', 'products.views.set_tags_short', name='set_tags_short'),

)