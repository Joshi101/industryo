from django.conf.urls import include, url
from django.contrib import admin
from . import views

urlpatterns = [

    # url(r'^accounts/', include('allauth.urls')),
    # url(r'^$', 'home.views.home', name='home'),

    url(r'^$', views.get_all_tags, name='all_tags'),

    url(r'^follow/$', views.follow_tag, name='follow'),
    url(r'^create/$', views.create, name='create'),
    url(r'^search_n_tags$', views.search_n_tags, name='search_n_tags'),
    url(r'^describe/$', views.describe_tag, name='describe_tag'),
    url(r'^companies/(?P<slug>[^/]+)/$', views.tag_companies, name='companies'),
    url(r'^products/(?P<slug>[^/]+)/$', views.tag_products, name='products'),
    url(r'^leads/(?P<slug>[^/]+)/$', views.tag_leads, name='leads'),
    url(r'^delete/(?P<slug>[^/]+)/$', views.delete_tag, name='delete_tag'),
    url(r'^(?P<slug>[^/]+)/$', views.get_tag, name='get_tag'),

]
