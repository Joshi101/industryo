from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^get_google_contacts/$', views.get_google_contacts, name='get_google_contacts'),
    url(r'^get_fb_contacts/$', views.get_facebook_contacts, name='get_facebook_contacts'),
]
