from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'industryo.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),


    # url(r'^accounts/', include('allauth.urls')),
    # url(r'^$', 'home.views.home', name='home'),

    url(r'^$', 'forum.views.questions', name='questions'),
    url(r'^w/$', 'forum.views.w_questions', name='w_questions'),
    url(r'^s/$', 'forum.views.s_questions', name='s_questions'),
    url(r'^ask/$', 'forum.views.ask', name='ask'),
    url(r'^ques_comment/$', 'forum.views.ques_comment', name='ques_comment'),
    url(r'^ans_comment/$', 'forum.views.ans_comment', name='ans_comment'),
    url(r'^answer/$', 'forum.views.reply', name='answer'),
    url(r'^voteup/$', 'forum.views.voteup', name='voteup'),
    url(r'^tagged/$', 'forum.views.question_tagged', name='tagged'),
    url(r'^delete_question/$', 'forum.views.delete_question', name='delete_question'),
    url(r'^delete_answer/$', 'forum.views.delete_answer', name='delete_answer'),
    url(r'^votedown/$', 'forum.views.votedown', name='votedown'),
    url(r'^searchtag/$', 'tags.views.search_tag', name='searchtag'),
    url(r'^(?P<slug>[^/]+)/$', 'forum.views.get_question', name='question'),


)
