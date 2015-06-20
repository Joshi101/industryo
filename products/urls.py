from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',

    # url(r'^accounts/', include('allauth.urls')),
    # url(r'^$', 'home.views.home', name='home'),

    url(r'^delete/$', 'products.views.delete', name='delete'),
    url(r'^add_product/$', 'products.views.add_product', name='add_product'),
    url(r'^(?P<slug>[^/]+)/$', 'products.views.product', name='product'),

)
