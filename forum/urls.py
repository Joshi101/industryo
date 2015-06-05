from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'industryo.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),


    # url(r'^accounts/', include('allauth.urls')),
    # url(r'^$', 'home.views.home', name='home'),

    url(r'^$', 'forum.views.questions', name='questions'),
    url(r'^ques_comment/$', 'forum.views.ques_comment', name='ques_comment'),
    url(r'^ans_comment/$', 'forum.views.ans_comment', name='ans_comment'),
    url(r'^answer/$', 'forum.views.reply', name='answer'),
    url(r'^voteup/$', 'forum.views.voteup', name='voteup'),
    url(r'^tagged/$', 'forum.views.question_tagged', name='tagged'),
    url(r'^votedown/$', 'forum.views.votedown', name='votedown'),
    url(r'^(?P<slug>[^/]+)/$', 'forum.views.get_question', name='question'),


)
