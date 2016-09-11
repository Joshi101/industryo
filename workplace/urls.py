from django.conf.urls import include, url
from . import views, views_new
from products import views as products_views

urlpatterns = [

    url(r'^fodder/$', views.fodder, name='fodder'),
    url(r'^todder/$', views.todder, name='todder'),

    url(r'^cw/$', views.change_workplace, name='change_workplace'),
    url(r'^add_product/$', products_views.add_product, name='add_product'),
    url(r'^delete_tag/$', views.delete_tag, name='delete_tag'),
    url(r'^side_panel/$', views.side_panel, name='side_panel'),
    url(r'^add_tag/$', views.add_tag, name='add_tag'),


    url(r'^(?P<slug>[^/]+)/activity/$', views_new.activity, name='activity'),
    url(r'^(?P<slug>[^/]+)/dashboard/$', views_new.dashboard, name='dashboard'),
    url(r'^(?P<slug>[^/]+)/members/$', views_new.members, name='members'),
    url(r'^(?P<slug>[^/]+)/products/$', views_new.products, name='products'),
    url(r'^invite_colleague/$', views.invite_colleague, name='invite_colleague'),
    url(r'^category/(?P<slug>[^/]+)/$', products_views.category_wp, name='category_wp'),

    url(r'^edit/$', views.edit_workplace, name='edit'),
    url(r'^random_card/$', views.random_card, name='random_card'),
    url(r'^change_type/$', views.change_type, name='change_type'),

    url(r'^set_logo/$', views_new.set_logo, name='set_logo'),
    url(r'^(?P<slug>[^/]+)/$', views_new.workplace_profile, name='workplace_profile'),

]
