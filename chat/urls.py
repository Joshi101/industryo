from django.conf.urls import  include, url
from . import views

urlpatterns = [
    url(r'^send/$', views.send_message, name='send_message'),
    url(r'^reply/$', views.reply, name='reply'),
    url(r'^delete/$', views.delete, name='delete_message'),
    url(r'^check/$', views.delete, name='check_message'),
    url(r'^send_mail$', views.send_mail, name='send_mail'),
]
