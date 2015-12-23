from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^workplace_data$', 'workplace.views.workplace_data', name='workplace_data'),
    url(r'^activity/$', 'home.data.activity', name='activity'),
    url(r'^details/$', 'home.data.details', name='details'),
    url(r'^send/$', 'home.email.send', name='send'),
    url(r'^send_mail/$', 'home.email.send_mail', name='send_mail'),
    url(r'^send_html/$', 'home.email.send_html', name='send_html'),

    url(r'^enquiry_all/$', 'activities.views.enquiry_all', name='enquiry_all'),
    url(r'^enquiry/^(?P<slug>[^/]+)/$', 'activities.views.enquiry', name='enquiry'),

)