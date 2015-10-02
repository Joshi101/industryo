from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'chat.views.inbox', name='inbox'),
    url(r'^new/$', 'chat.views.new', name='new_message'),
    url(r'^send/$', 'chat.views.send', name='send_message'),
    url(r'^delete/$', 'chat.views.delete', name='delete_message'),
    url(r'^users/$', 'chat.views.users', name='users_message'),
    url(r'^check/$', 'chat.views.check', name='check_message'),
    url(r'^(?P<username>[^/]+)/$', 'chat.views.messages', name='messages'),
)