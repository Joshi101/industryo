from django.conf.urls import include, url
from . import views

urlpatterns = [
    # url(r'^search_n_tags$', 'tags.views.search_n_tags', name='search_n_tags'),
    # url(r'^questions/$', views.question_search, name='question_search'),
    url(r'^articles/$', views.article_search, name='article_search'),
    url(r'^tags/$', views.tag_search, name='tag_search'),
    url(r'^users/$', views.user_search, name='user_search'),
    url(r'^workplaces/$', views.workplace_search, name='workplace_search'),
    url(r'^products/$', views.product_search, name='product_search'),
]
