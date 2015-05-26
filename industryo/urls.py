from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'industryo.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^$', 'home.views.home', name='home'),
    url(r'^notifications/$', 'activities.views.notifications', name='notifications'),
    url(r'^search/$', 'home.views.home', name='search'),
    url(r'^logout$', 'django.contrib.auth.views.logout', {'next_page': 'home'}, name='logout'),
    url(r'^workplace/register/$', 'workplace.views.workplace_register', name='register'),
    url(r'^set/$', 'workplace.views.set_workplace', name='set'),
    url(r'^create_tag/$', 'tags.views.create_tag', name='search'),
    url(r'^ask/$', 'forum.views.ask', name='ask'),
    url(r'^q_tag/$', 'forum.views.question_tagged', name='q_tag'),
    url(r'^searchtag/$', 'tags.views.search_tag', name='searchtag'),
    url(r'^searchworkplace/$', 'workplace.views.search_workplace', name='searchworkplace'),
    url(r'^searchsegment/$', 'workplace.views.search_segment', name='searchsegment'),
    url(r'^searchasset/$', 'workplaceprofile.views.search_asset', name='searchasset'),
    url(r'^searchmaterial/$', 'workplaceprofile.views.search_material', name='searchmaterial'),
    url(r'^searchoperation/$', 'workplaceprofile.views.search_operation', name='searchoperation'),
    url(r'^question/(?P<slug>[^/]+)/$', 'forum.views.get_question', name='question'),
    url(r'^forum/', include('forum.urls', namespace='forum')),
    url(r'^user/', include('userprofile.urls', namespace='user')),
    url(r'^workplace/', include('workplace.urls', namespace='workplace')),
    url(r'^nodes/', include('nodes.urls', namespace='nodes')),
    url(r'^images/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    # url(r'^searchworkplace/$', 'workplace.views.search_workplace', name='searchworkplace'),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
