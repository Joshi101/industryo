from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
from . import views


urlpatterns = [
    url(r'^refer/$', views.refer, name='refer'),
]
