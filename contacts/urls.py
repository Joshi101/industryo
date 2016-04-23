from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'chat.views.inbox', name='inbox'),
)