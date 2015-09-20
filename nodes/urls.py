from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import TemplateView

urlpatterns = patterns('',

    # url(r'^accounts/', include('allauth.urls')),
    # url(r'^$', 'home.views.home', name='home'),
    url(r'^articles/$', 'nodes.views.articles', name='articles'),
    url(r'^like/$', 'nodes.views.like', name='like'),
    url(r'^comment/$', 'nodes.views.comment', name='comment'),
    url(r'^upload/$', 'nodes.views.upload_image', name='upload'),
    url(r'^post/$', 'nodes.views.post', name='post'),
    url(r'^delete/$', 'nodes.views.delete', name='delete'),
    url(r'^delete_image/$', 'nodes.views.delete_node_image', name='delete_image'),
    url(r'^write/$', 'nodes.views.write', name='write'),

    url(r'^what_to_write/$', TemplateView.as_view(template_name='nodes/what_to_write.html'), name='what_to_write'),
    url(r'^help/$', TemplateView.as_view(template_name='nodes/help.html'), name='help'),
    url(r'^set_logo/$', 'nodes.views.set_logo', name='set_logo'),
    url(r'^set_profile_image/$', 'nodes.views.set_profile_image', name='set_profile_image'),
    url(r'^set_product_image/(?P<slug>[^/]+)/$', 'nodes.views.set_product_image', name='set_product_image'),
    url(r'^set_tag_logo/(?P<slug>[^/]+)/$', 'nodes.views.set_tag_logo', name='set_tag_logo'),

    url(r'^edit/(?P<id>[^/]+)/$', 'nodes.views.edit', name='edit'),
    url(r'^(?P<slug>[^/]+)/$', 'nodes.views.node', name='node'),
    
)
