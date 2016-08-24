from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [

    # url(r'^accounts/', include('allauth.urls')),
    # url(r'^$', 'home.views.home', name='home'),

    url(r'^$', views.all_products, name='marketplace'),
    url(r'^home/$', views.home, name='home'),

    url(r'^random/$', views.random, name='random'),
    url(r'^delete/$', views.delete, name='delete'),
    url(r'^add_product/$', views.add_product, name='add_product'),

    url(r'^edit_add/(?P<id>[^/]+)/$', views.edit_add_product, name='edit_add'),

    url(r'^enquire/$', views.enquire, name='enquire'),
    url(r'^int_c/$', views.initial_category, name='initial_category'),
    url(r'^c_r/$', views.c_r, name='c_r'),
    url(r'^cat_u/$', views.category_update, name='cat_u'),

    url(r'^enquiry_all/$', views.enquiry_all, name='enquiry_all'),
    url(r'^category/(?P<slug>[^/]+)/$', views.category, name='category'),
    url(r'^new_category/$', views.new_category, name='new_category'),

    url(r'^(?P<id>[^/]+)/set_details/$', views.set_details, name='set_details'),
    url(r'^(?P<id>[^/]+)/edit_desc/$', views.edit_desc, name='edit_desc'),
    url(r'^(?P<id>[^/]+)/edit_category/$', views.edit_category, name='edit_category'),
    url(r'^(?P<id>[^/]+)/change_image/$', views.change_image, name='change_image'),
    url(r'^(?P<slug>[^/]+)/$', views.product, name='product'),
    url(r'^(?P<slug>[^/]+)/set_tags_short/$', views.set_tags_short, name='set_tags_short'),

]
