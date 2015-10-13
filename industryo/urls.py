from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'industryo.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^$', 'home.views.home', name='home'),
    url(r'^about/$', 'home.views.about', name='about'),
    url(r'^notifications/$', 'activities.views.notifications', name='notifications'),
    url(r'^notify/$', 'activities.views.notify', name='notify'),
    url(r'^count_notify/$', 'activities.views.count_notify', name='count_notify'),
    url(r'^search/$', 'home.views.home', name='search'),

    url(r'^logout$', 'django.contrib.auth.views.logout', {'next_page': 'home'}, name='logout'),
    url(r'^workplace/register/$', 'workplace.views.workplace_register', name='register'),
    url(r'^set/$', 'workplace.views.set_workplace', name='set'),
    url(r'^details/$', 'userprofile.views.set_details', name='details'),

    url(r'^create_tag/$', 'tags.views.create_tag', name='create_tag'),
    url(r'^searchtag/$', 'tags.views.search_tag', name='search_tag'),
    url(r'^q_tag/$', 'forum.views.question_tagged', name='q_tag'),
    url(r'^sitemap/$', 'workplace.views.sitemap', name='sitemap'),
    url(r'^searchworkplace/$', 'workplace.views.search_workplace', name='searchworkplace'),
    url(r'^send_an_email/$', 'home.views.send_an_email', name='send_an_email'),
    url(r'^send_set_wp_email/$', 'home.views.send_set_wp_email', name='send_set_wp_email'),

    url(r'^forum/', include('forum.urls', namespace='forum')),
    url(r'^user/', include('userprofile.urls', namespace='user')),
    url(r'^workplace/', include('workplace.urls', namespace='workplace')),
    url(r'^nodes/', include('nodes.urls', namespace='nodes')),
    url(r'^tags/', include('tags.urls', namespace='tags')),
    url(r'^products/', include('products.urls', namespace='products')),
    url(r'^messages/', include('chat.urls', namespace='messages')),
    url(r'^internal/', include('activities.urls', namespace='activities')),

    url(r'^home/right/$', 'home.views.home_right', name='home_right'),



    url(r'^robots.txt/$', TemplateView.as_view(template_name='robots.txt')),
    url(r'^images/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
