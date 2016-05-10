from django.shortcuts import render, redirect, render_to_response, RequestContext
from nodes.models import Node
from forum.models import Question
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from home import tasks
# from django.core.mail import EmailMultiAlternatives
from datetime import datetime, timedelta, time, date
from .templates import *


@login_required
def send(request):
    if 'q' in request.GET:
        s = request.GET.get('q')
        if s == 'set_wp':
            id = request.GET.get('id')
            tasks.send_html_mail(id, n=52)
        elif s == 'set_wp_all':
            todaydate = date.today()
            startdate = todaydate + timedelta(days=1)
            enddate = startdate - timedelta(days=30)
            lis = User.objects.filter(date_joined__range=[enddate, startdate], userprofile__primary_workplace=None)
            for i in lis:
                tasks.send_html_mail(i.id, n=52)

    return redirect("/internal/details/?q=u")


@login_required
def send_html(request):
    pass
@login_required
def send_mail(request):
    if request.method == 'POST':
        s = request.POST.get('q')
        subject = request.POST.get('subject')

        arguments = request.POST.get('arguments')
        bod = request.POST.get('mail')
        body = bod.replace("//", "{").replace("/?", "}")
        if s == "meh":
            u = User.objects.get(id=1)
            tasks.send_html_mail_post(u.id, n=body, subject=subject, arguments=arguments)
        elif s == 'set_wp_all':
            todaydate = date.today()
            startdate = todaydate + timedelta(days=1)
            enddate = startdate - timedelta(days=40)
            lis = User.objects.filter(date_joined__range=[enddate, startdate], userprofile__primary_workplace=None)
            for i in lis:
                tasks.send_html_mail_post(i.id, n=body, subject=subject, arguments=arguments)
        # elif s == 'set_wp':
        #     id = request.GET.get('id')
        #     tasks.send_html_mail(id, n=52)
        elif s == "alh":
            users = User.objects.all()
            for u in users:
                tasks.send_html_mail_post(u.id, n=body, subject=subject, arguments=arguments)
        elif s == "ah":
            users = User.objects.filter(userprofile__primary_workplace__workplace_type='A')
            for u in users:
                tasks.send_html_mail_post(u.id, n=body, subject=subject, arguments=arguments)
        elif s == "bh":
            users = User.objects.filter(userprofile__primary_workplace__workplace_type='B')
            for u in users:
                tasks.send_html_mail_post(u.id, n=body, subject=subject, arguments=arguments)
        elif s == "ch":
            users = User.objects.filter(userprofile__primary_workplace__workplace_type='C')
            for u in users:
                tasks.send_html_mail_post(u.id, n=body, subject=subject, arguments=arguments)
        elif s == "oh":
            users = User.objects.filter(userprofile__primary_workplace__workplace_type='O')
            for u in users:
                tasks.send_html_mail_post(u.id, n=body, subject=subject, arguments=arguments)
        elif s == "nh":
            users = User.objects.filter(userprofile__primary_workplace=None)
            for u in users:
                tasks.send_html_mail_post(u.id, n=body, subject=subject, arguments=arguments)
        elif s == "ranh":
            questions = Question.objects.filter(answered=False)
            for q in questions:
                tasks.send_html_mail_post(q.user.id, n=Template_answer_your_own_question.format(q.user.userprofile, q.slug, q.title))

        elif s == "lh":
            # pi = []
            for u in list_new:
                tasks.send_list_html_mail(u, n=22)
            #     if len(pi) < 3:
            #         pi.append(u)
            #     elif len(pi) == 3:
            #         pi.append(u)
            #         tasks.send_list_html_mail(pi, n=22)
            #         pi = []
            # tasks.send_list_html_mail(pi, n=22)

    return redirect('/internal/activity')

list_new = []