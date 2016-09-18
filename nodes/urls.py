from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
from . import views

urlpatterns = [

    # url(r'^accounts/', include('allauth.urls')),
    # url(r'^$', 'home.views.home', name='home'),
    url(r'^articles/$', views.articles, name='articles'),
    url(r'^like/$', views.like, name='like'),
    url(r'^comment/$', views.comment, name='comment'),
    url(r'^upload/$', views.upload_image, name='upload'),
    url(r'^add_image/$', views.add_image, name='add_image'),
    url(r'^post/$', views.post, name='post'),
    url(r'^delete/$', views.delete, name='delete'),
    url(r'^delete_image/$', views.delete_node_image, name='delete_image'),
    url(r'^write/$', views.write, name='write'),

    url(r'^what_to_write/$', TemplateView.as_view(template_name='nodes/what_to_write.html'), name='what_to_write'),
    url(r'^help/$', TemplateView.as_view(template_name='nodes/help.html'), name='help'),
    url(r'^set_logo/$', views.set_logo, name='set_logo'),
    url(r'^set_profile_image/$', views.set_profile_image, name='set_profile_image'),
    url(r'^set_product_image/(?P<slug>[^/]+)/$', views.set_product_image, name='set_product_image'),
    url(r'^set_tag_logo/(?P<slug>[^/]+)/$', views.set_tag_logo, name='set_tag_logo'),
    url(r'^set_category_logo/(?P<slug>[^/]+)/$', views.set_category_logo, name='set_category_logo'),

    url(r'^edit/(?P<id>[^/]+)/$', views.edit, name='edit'),
    url(r'^(?P<slug>[^/]+)/$', views.node, name='node'),

]
