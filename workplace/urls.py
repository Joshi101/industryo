from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',

    # url(r'^accounts/', include('allauth.urls')),
    # url(r'^$', 'home.views.home', name='home'),


    url(r'^set_about/$', 'workplace.views.set_about', name='set_about'),
    url(r'^set_tags/$', 'workplace.views.set_tags', name='set_tags'),
    url(r'^set_capabilities/$', 'workplace.views.set_capabilities', name='set_capabilities'),
    url(r'^set_product_details/$', 'workplace.views.set_product_details', name='set_product_details'),
    url(r'^add_product/$', 'products.views.add_product', name='add_product'),
    url(r'^delete_tags/$', 'workplace.views.delete_tags', name='delete_tags'),
    url(r'^questions/$', 'workplace.views.workplace_questions', name='questions'),
    url(r'^answers/$', 'workplace.views.workplace_answers', name='answers'),
    url(r'^feeds/$', 'workplace.views.workplace_feeds', name='feed'),
    url(r'^articles/$', 'workplace.views.workplace_articles', name='articles'),
    url(r'^(?P<slug>[^/]+)/$', 'workplace.views.workplace_profile', name='workplace_profile'),
    url(r'^get_top_scorers/(?P<slug>[^/]+)/$', 'workplace.views.get_top_scorers', name='get_top_scorers'),

)
