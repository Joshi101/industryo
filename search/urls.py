from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    #url(r'^search_n_tags$', 'tags.views.search_n_tags', name='search_n_tags'),
    url(r'^questions/$', 'search.views.question_search', name='question_search'),
    url(r'^articles/$', 'search.views.article_search', name='article_search'),
    url(r'^tags/$', 'search.views.tag_search', name='tag_search'),
    url(r'^users/$', 'search.views.user_search', name='user_search'),
    url(r'^workplaces/$', 'search.views.workplace_search', name='workplace_search'),
    url(r'^products/$', 'search.views.product_search', name='product_search'),
)