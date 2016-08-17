from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import TemplateView
from django.contrib.auth.views import logout
from django.views.static import serve
from home import sitemaps as home_sitemap
from home import nav_content as home_nav_content
from home import views as home_views
from home import commands as home_commands
from products import views as products_views
from activities import views as activities_views
from search import views as search_views
from workplace import views as workplace_views
from userprofile import views as userprofile_views
from tags import views as tags_views
from forum import views as forum_views
from contacts import views as contacts_views
from contacts import execution as contacts_execution

urlpatterns = [
    url(r'^sitemap\.xml$', home_sitemap.sitemap),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^$', home_views.home, name='home'),
    url(r'^feed/$', home_views.feed, name='feed'),
    url(r'^network/$', home_views.network, name='network'),
    url(r'^feedback/$', home_views.feedback, name='feedback'),

    url(r'^marketplace$', products_views.all_products, name='marketplace'),

    url(r'^notifications/$', activities_views.notifications, name='notifications'),
    url(r'^notify/$', activities_views.notify, name='notify'),
    url(r'^count_notify/$', activities_views.count_notify, name='count_notify'),

    url(r'^search/$', search_views.search, name='search'),
    url(r'^searchq/$', search_views.searchq, name='searchq'),
    url(r'^forum_search/$', search_views.forum_search, name='forum_search'),
    url(r'^article_search/$', search_views.article_search, name='article_search'),
    url(r'^product_search/$', search_views.product_search, name='product_search'),
    url(r'^workplace_search/$', search_views.workplace_search,
        name='workplace_search'),
    url(r'^user_search/$', search_views.user_search, name='user_search'),

    url(r'^logout$', logout,
        {'next_page': 'home'}, name='logout'),
    url(r'^set/$', workplace_views.set_workplace, name='set'),
    url(r'^details/$', userprofile_views.set_details, name='details'),

    url(r'^create_tag/$', tags_views.create_tag, name='create_tag'),
    url(r'^searchtag/$', tags_views.search_tag, name='search_tag'),
    url(r'^q_tag/$', forum_views.question_tagged, name='q_tag'),
    url(r'^searchworkplace/$', workplace_views.search_workplace,
        name='searchworkplace'),
    url(r'^searchperson/$', userprofile_views.search_person, name='searchperson'),

    url(r'^join_wp/(?P<slug>[^/]+)/$',
        workplace_views.join_wp, name='join_wp'),

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
    url(r'^inbox/', include('inbox.urls', namespace='inbox')),

    url(r'^home/right/$', home_views.home_right, name='home_right'),
    url(r'^home/right_down/$', home_views.home_right_down, name='home_right_down'),

    url(r'^about/$', TemplateView.as_view(template_name='about.html')),
    url(r'^contact/$', TemplateView.as_view(template_name='contacts.html')),
    url(r'^terms/$', TemplateView.as_view(template_name='terms.html')),
    url(r'^team/$', TemplateView.as_view(template_name='team.html')),
    url(r'^sitemap/$', TemplateView.as_view(template_name='sitemap/sitemap.html'), name='sitemap'),
    url(r'^sitemap/people$', home_views.people),
    url(r'^sitemap/workplaces$', home_views.workplaces),
    url(r'^sitemap/tags$', home_views.tags),
    url(r'^sitemap/questions$', home_views.questions),
    url(r'^sitemap/articles$', home_views.articles),
    url(r'^sitemap/products$', home_views.products),
    url(r'^sitemap/categories$', home_views.categories),
    url(r'^sitemap/categories_wp$', home_views.categories_wp),
    url(r'^sitemap/nodes$', home_views.nodes),
    url(r'^sitemap/leads$', home_views.leads),

    url(r'^exec/$', home_commands.task_exec),
    url(r'^check_exec/$', contacts_execution.check_executable),
    url(r'^fuck_shit/$', contacts_views.fuck_shit),

    url(r'^create_api/$', workplace_views.create_api),
    url(r'^create_api2/$', workplace_views.create_api2),
    url(r'^create_api3/$', workplace_views.create_api3),

    url(r'^category/$', products_views.all_category, name='all_category'),
    url(r'^category/(?P<slug>[^/]+)/$', products_views.category, name='category'),
    url(r'^category/(?P<slug>[^/]+)/products/$', products_views.category_prod, name='category_prod'),
    url(r'^category/(?P<slug>[^/]+)/workplace/$', products_views.category_wp, name='category_wp'),

    url(r'^nav_suggest/$', home_nav_content.nav_suggest, name='nav_suggest'),

    url(r'^robots.txt/$', TemplateView.as_view(template_name='robots.txt')),
    url(r'^images/(?P<path>.*)$', serve,
        {'document_root': settings.MEDIA_ROOT}),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
