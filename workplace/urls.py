from django.conf.urls import include, url
from django.contrib import admin
from . import views, views_new
from products import views as products_views

urlpatterns = [

    # url(r'^accounts/', include('allauth.urls')),
    # url(r'^$', 'home.views.home', name='home'),

    url(r'^set_about/$', views.set_about, name='set_about'),
    url(r'^set_details/$', views.set_details, name='set_details'),

    url(r'^fodder/$', views.fodder, name='fodder'),
    url(r'^todder/$', views.todder, name='todder'),

    url(r'^cw/$', views.change_workplace, name='change_workplace'),
    # url(r'^set_tags/$', views.set_tags, name='set_tags'),
    # url(r'^set_tags_short/$', views.set_tags_short, name='set_tags_short'),
    url(r'^set_capabilities/$', views.set_capabilities, name='set_capabilities'),
    url(r'^set_product_details/$', views.set_product_details, name='set_product_details'),
    url(r'^add_product/$', products_views.add_product, name='add_product'),
    url(r'^delete_tag/$', views.delete_tag, name='delete_tag'),
    url(r'^questions/$', views.workplace_questions, name='questions'),
    url(r'^answers/$', views.workplace_answers, name='answers'),
    url(r'^feeds/$', views.workplace_feeds, name='feed'),
    url(r'^articles/$', views.workplace_articles, name='articles'),
    url(r'^side_panel/$', views.side_panel, name='side_panel'),
    url(r'^add_tag/$', views.add_tag, name='add_tag'),

    url(r'^edit_links/$', views.edit_links, name='edit_links'),     # ye
    url(r'^edit_contacts/$', views.edit_contacts, name='edit_contacts'),        # aur ye

    url(r'^(?P<slug>[^/]+)/about/$', views.workplace_about, name='about'),
    url(r'^(?P<slug>[^/]+)/activity/$', views_new.activity, name='activity'),
    url(r'^(?P<slug>[^/]+)/dashboard/$', views_new.dashboard, name='dashboard'),
    # url(r'^capabilities/(?P<slug>[^/]+)/$', views.workplace_capabilities, name='capabilities'),
    url(r'^(?P<slug>[^/]+)/members/$', views_new.members, name='members'),
    url(r'^(?P<slug>[^/]+)/products/$', views_new.products, name='products'),
    url(r'^get_top_scorers/(?P<slug>[^/]+)/$', views.get_top_scorers, name='get_top_scorers'),
    url(r'^invite_colleague/$', views.invite_colleague, name='invite_colleague'),
    url(r'^category/(?P<slug>[^/]+)/$', products_views.category_wp, name='category_wp'),

    url(r'^edit/$', views.edit_workplace, name='edit'),
    url(r'^random_card/$', views.random_card, name='random_card'),
    url(r'^change_type/$', views.change_type, name='change_type'),

    url(r'^set_logo/$', views_new.set_logo, name='set_logo'),
    url(r'^(?P<slug>[^/]+)/$', views_new.workplace_profile, name='workplace_profile'),

]
