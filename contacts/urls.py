from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^get_google_contacts/$', 'contacts.views.get_google_contacts', name='get_google_contacts'),
)