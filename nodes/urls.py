from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',

    # url(r'^accounts/', include('allauth.urls')),
    # url(r'^$', 'home.views.home', name='home'),
    url(r'^articles/$', 'nodes.views.articles', name='articles'),
    url(r'^like/$', 'nodes.views.like', name='like'),
    url(r'^comment/$', 'nodes.views.comment', name='comment'),
    url(r'^upload/$', 'nodes.views.upload_image', name='upload'),
    url(r'^post/$', 'nodes.views.post', name='post'),
    url(r'^delete/$', 'nodes.views.delete', name='delete'),
    url(r'^write/$', 'nodes.views.write', name='write'),
    url(r'^set_logo/$', 'nodes.views.set_logo', name='set_logo'),
    url(r'^set_profile_image/$', 'nodes.views.set_profile_image', name='set_profile_image'),
    url(r'^set_product_image/(?P<slug>[^/]+)/$', 'nodes.views.set_product_image', name='set_product_image'),
    url(r'^set_tag_logo/(?P<slug>[^/]+)/$', 'nodes.views.set_tag_logo', name='set_tag_logo'),
    url(r'^(?P<slug>[^/]+)/$', 'nodes.views.node', name='node'),

)
