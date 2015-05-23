from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'industryo.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^$', 'home.views.home', name='home'),
    url(r'^search/$', 'home.views.home', name='search'),
    url(r'^logout$', 'django.contrib.auth.views.logout', {'next_page': 'login'}, name='logout'),
    url(r'^workplace/register/$', 'workplace.views.workplace_register', name='register'),
    url(r'^set/$', 'workplace.views.set_workplace', name='set'),
    url(r'^create_tag/$', 'tags.views.create_tag', name='search'),
    url(r'^ask/$', 'forum.views.ask', name='ask'),
    url(r'^q_tag/$', 'forum.views.question_tagged', name='q_tag'),
    url(r'^searchtag/$', 'tags.views.search_tag', name='searchtag'),
    url(r'^question/(?P<slug>[^/]+)/$', 'forum.views.get_question', name='question'),
    url(r'^forum/', include('forum.urls', namespace='forum')),
    url(r'^workplace/', include('workplace.urls', namespace='workplace')),

)
