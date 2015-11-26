from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^workplace_data$', 'workplace.views.workplace_data', name='workplace_data'),
    url(r'^activity/$', 'home.data.activity', name='activity'),
    url(r'^details/$', 'home.data.details', name='details'),

)