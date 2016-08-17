from django.conf.urls import include, url
from home import data as home_data
from home import email as home_email
from workplace import views as workplace_views
from products import views as products_views

urlpatterns = [
    url(r'^workplace_data$', workplace_views.workplace_data, name='workplace_data'),
    url(r'^activity/$', home_data.activity, name='activity'),
    url(r'^details/$', home_data.details, name='details'),
    url(r'^send/$', home_email.send, name='send'),
    url(r'^send_mail/$', home_email.send_mail, name='send_mail'),
    url(r'^send_html/$', home_email.send_html, name='send_html'),
    url(r'^send_new_wp/$', home_email.send_new_wp, name='send_new_wp'),

    url(r'^change_wp_u/$', home_data.change_wp_u, name='change_wp_u'),
    url(r'^change_p_o/$', home_data.change_p_o, name='change_p_o'),

    url(r'^products/(?P<id>[^/]+)/edit_desc/$', products_views.int_edit_desc, name='int_edit_desc'),
    url(r'^products/(?P<id>[^/]+)/edit_category/$', products_views.int_edit_category, name='int_edit_category'),
    url(r'^(?P<id>[^/]+)/set_details/$', products_views.set_int_details, name='set_int_details'),
    url(r'^products/(?P<id>[^/]+)/change_image/$', products_views.int_change_image, name='int_change_image'),
    url(r'^products/(?P<slug>[^/]+)/$', products_views.int_product, name='int_product'),
    url(r'^add_product/$', products_views.int_add_product, name='int_add_product'),
    url(r'^category/(?P<slug>[^/]+)/$', products_views.int_category, name='int_category'),
]
