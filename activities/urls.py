from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^workplace_data$', 'workplace.views.workplace_data', name='workplace_data'),

)