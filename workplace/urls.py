from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',

    # url(r'^accounts/', include('allauth.urls')),
    # url(r'^$', 'home.views.home', name='home'),

    url(r'^set_about/$', 'workplace.views.set_about', name='set_about'),
    url(r'^set_details/$', 'workplace.views.set_details', name='set_details'),

    url(r'^fodder/$', 'workplace.views.fodder', name='fodder'),
    url(r'^todder/$', 'workplace.views.todder', name='todder'),

    url(r'^cw/$', 'workplace.views.change_workplace', name='change_workplace'),
    url(r'^set_tags/$', 'workplace.views.set_tags', name='set_tags'),
    url(r'^set_tags_short/$', 'workplace.views.set_tags_short', name='set_tags_short'),
    url(r'^set_capabilities/$', 'workplace.views.set_capabilities', name='set_capabilities'),
    url(r'^set_product_details/$', 'workplace.views.set_product_details', name='set_product_details'),
    url(r'^add_product/$', 'products.views.add_product', name='add_product'),
    url(r'^delete_tag/$', 'workplace.views.delete_tag', name='delete_tag'),
    url(r'^questions/$', 'workplace.views.workplace_questions', name='questions'),
    url(r'^answers/$', 'workplace.views.workplace_answers', name='answers'),
    url(r'^feeds/$', 'workplace.views.workplace_feeds', name='feed'),
    url(r'^articles/$', 'workplace.views.workplace_articles', name='articles'),
    url(r'^side_panel/$', 'workplace.views.side_panel', name='side_panel'),
    url(r'^add_tag/$', 'workplace.views.add_tag', name='add_tag'),

    url(r'^edit_links/$', 'workplace.views.edit_links', name='edit_links'),     # ye
    url(r'^edit_contacts/$', 'workplace.views.edit_contacts', name='edit_contacts'),        # aur ye

    url(r'^(?P<slug>[^/]+)/about/$', 'workplace.views.workplace_about', name='about'),
    url(r'^(?P<slug>[^/]+)/activity/$', 'workplace.views_new.activity', name='activity'),
    url(r'^(?P<slug>[^/]+)/dashboard/$', 'workplace.views_new.dashboard', name='dashboard'),
    # url(r'^capabilities/(?P<slug>[^/]+)/$', 'workplace.views.workplace_capabilities', name='capabilities'),
    url(r'^(?P<slug>[^/]+)/members/$', 'workplace.views_new.members', name='members'),
    url(r'^(?P<slug>[^/]+)/products/$', 'workplace.views_new.products', name='products'),
    url(r'^get_top_scorers/(?P<slug>[^/]+)/$', 'workplace.views.get_top_scorers', name='get_top_scorers'),
    url(r'^invite_colleague/$', 'workplace.views.invite_colleague', name='invite_colleague'),
    url(r'^category/(?P<slug>[^/]+)/$', 'products.views.category_wp', name='category_wp'),

    url(r'^edit/$', 'workplace.views.edit_workplace', name='edit'),
    url(r'^random_card/$', 'workplace.views.random_card', name='random_card'),
    url(r'^change_type/$', 'workplace.views.change_type', name='change_type'),

    url(r'^(?P<slug>[^/]+)/$', 'workplace.views_new.workplace_profile', name='workplace_profile'),

)
