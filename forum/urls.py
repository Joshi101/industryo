from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
from . import views
from tags import views as tags_views


urlpatterns = [
    url(r'^$', views.questions, name='questions'),
    url(r'^w/$', views.w_questions, name='w_questions'),
    url(r'^s/$', views.s_questions, name='s_questions'),
    url(r'^ask/$', views.ask, name='ask'),
    url(r'^ask/(?P<tag>[^/]+)$', views.ask, name='ask'),
    url(r'^ask/$', views.ask, name='ask'),

    url(r'^help/$', TemplateView.as_view(template_name='forum/help.html'), name='help'),
    url(r'^why_should_i_answer/$', TemplateView.as_view(template_name='forum/why_should_i_answer.html'), name='why_should_i_answer'),
    url(r'^how_to_ask/$', TemplateView.as_view(template_name='forum/how_to_ask.html'), name='how_to_ask'),
    url(r'^ques_comment/$', views.ques_comment, name='ques_comment'),
    url(r'^ans_comment/$', views.ans_comment, name='ans_comment'),
    url(r'^answer/$', views.reply, name='answer'),
    url(r'^voteup/$', views.voteup, name='voteup'),
    url(r'^tagged/$', views.question_tagged, name='tagged'),

    url(r'^q_tags/$', views.q_tags, name='q_tags'),
    url(r'^delete_question/$', views.delete_question, name='delete_question'),
    url(r'^delete_answer/$', views.delete_answer, name='delete_answer'),
    url(r'^delete_image/$', views.delete_question_image, name='delete_image'),
    url(r'^votedown/$', views.votedown, name='votedown'),
    url(r'^searchtag/$', tags_views.search_tag, name='searchtag'),
    url(r'^category/$', views.category, name='category'),
    url(r'^edit/(?P<id>[^/]+)/$', views.edit_ques, name='edit_ques'),
    url(r'^(?P<slug>[^/]+)/$', views.get_question, name='question'),
]
