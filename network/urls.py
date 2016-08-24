from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    url(r'^$', views.network, name='network'),
    url(r'^products$', views.network_products, name='products'),
    url(r'^companies$', views.network_companies, name='companies'),
    url(r'^feed$', views.network_feeds, name='feed'),
    url(r'^side_overview$', views.side_overview, name='side_overview'),
    url(r'^search_tags$', views.search_tags, name='search_tags'),
    url(r'^add_tag$', views.add_tag, name='add_tag'),
    url(r'^connect$', views.connect, name='connect'),
]
