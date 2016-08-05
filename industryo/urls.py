from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView
# from django.contrib.sitemaps.views import sitemap
# from .sitemaps import sitemaps

urlpatterns = patterns('',
    url(r'^sitemap\.xml$', 'home.sitemaps.sitemap'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^$', 'home.views.home', name='home'),
    url(r'^feed/$', 'home.views.feed', name='feed'),
    url(r'^feedback/$', 'home.views.feedback', name='feedback'),

    url(r'^marketplace$', 'products.views.all_products', name='marketplace'),

    url(r'^notifications/$', 'activities.views.notifications', name='notifications'),
    url(r'^notify/$', 'activities.views.notify', name='notify'),
    url(r'^count_notify/$', 'activities.views.count_notify', name='count_notify'),

    url(r'^search/$', 'search.views.search', name='search'),
    url(r'^searchq/$', 'search.views.searchq', name='searchq'),
    url(r'^forum_search/$', 'search.views.forum_search', name='forum_search'),
    url(r'^article_search/$', 'search.views.article_search', name='article_search'),
    url(r'^product_search/$', 'search.views.product_search', name='product_search'),
    url(r'^workplace_search/$', 'search.views.workplace_search', name='workplace_search'),
    url(r'^user_search/$', 'search.views.user_search', name='user_search'),

    url(r'^logout$', 'django.contrib.auth.views.logout', {'next_page': 'home'}, name='logout'),
    url(r'^set/$', 'workplace.views.set_workplace', name='set'),
    url(r'^details/$', 'userprofile.views.set_details', name='details'),

    url(r'^create_tag/$', 'tags.views.create_tag', name='create_tag'),
    url(r'^searchtag/$', 'tags.views.search_tag', name='search_tag'),
    url(r'^q_tag/$', 'forum.views.question_tagged', name='q_tag'),
    url(r'^searchworkplace/$', 'workplace.views.search_workplace', name='searchworkplace'),
    url(r'^searchperson/$', 'userprofile.views.search_person', name='searchperson'),

    url(r'^join_wp/(?P<slug>[^/]+)/$', 'workplace.views.join_wp', name='join_wp'),

    url(r'^search/', include('search.urls', namespace='search')),
    url(r'^forum/', include('forum.urls', namespace='forum')),
    url(r'^user/', include('userprofile.urls', namespace='user')),
    url(r'^workplace/', include('workplace.urls', namespace='workplace')),
    url(r'^nodes/', include('nodes.urls', namespace='nodes')),
    url(r'^tags/', include('tags.urls', namespace='tags')),
    url(r'^products/', include('products.urls', namespace='products')),
    url(r'^messages/', include('chat.urls', namespace='messages')),
    url(r'^internal/', include('activities.urls', namespace='activities')),
    url(r'^contacts/', include('contacts.urls', namespace='contacts')),
    url(r'^leads/', include('leads.urls', namespace='leads')),

    url(r'^home/right/$', 'home.views.home_right', name='home_right'),
    url(r'^home/right_down/$', 'home.views.home_right_down', name='home_right_down'),

    url(r'^about/$', TemplateView.as_view(template_name='about.html')),
    url(r'^contact/$', TemplateView.as_view(template_name='contacts.html')),
    url(r'^terms/$', TemplateView.as_view(template_name='terms.html')),
    url(r'^team/$', TemplateView.as_view(template_name='team.html')),
    url(r'^sitemap/$', TemplateView.as_view(template_name='sitemap/sitemap.html'), name='sitemap'),
    url(r'^sitemap/people$', 'home.views.people'),
    url(r'^sitemap/workplaces$', 'home.views.workplaces'),
    url(r'^sitemap/tags$', 'home.views.tags'),
    url(r'^sitemap/questions$', 'home.views.questions'),
    url(r'^sitemap/articles$', 'home.views.articles'),
    url(r'^sitemap/products$', 'home.views.products'),
    url(r'^sitemap/categories$', 'home.views.categories'),
    url(r'^sitemap/categories_wp$', 'home.views.categories_wp'),
    url(r'^sitemap/nodes$', 'home.views.nodes'),
    url(r'^sitemap/leads$', 'home.views.leads'),

    url(r'^exec/$', 'home.commands.task_exec'),
    url(r'^check_exec/$', 'contacts.execution.check_executable'),
    url(r'^fuck_shit/$', 'contacts.views.fuck_shit'),

    url(r'^create_api/$', 'workplace.views.create_api'),
    url(r'^create_api2/$', 'workplace.views.create_api2'),
    url(r'^create_api3/$', 'workplace.views.create_api3'),

    url(r'^category/$', 'products.views.all_category', name='all_category'),
    url(r'^category/(?P<slug>[^/]+)/$', 'products.views.category', name='category'),
    url(r'^category/(?P<slug>[^/]+)/products/$', 'products.views.category_prod', name='category_prod'),
    url(r'^category/(?P<slug>[^/]+)/workplace/$', 'products.views.category_wp', name='category_wp'),

    url(r'^nav_advert/$', 'home.views.nav_advert', name='nav_advert'),

    url(r'^robots.txt/$', TemplateView.as_view(template_name='robots.txt')),
    url(r'^images/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
