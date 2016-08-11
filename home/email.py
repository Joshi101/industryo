from django.shortcuts import render, redirect, render_to_response, RequestContext
from nodes.models import Node
from forum.models import Question
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from workplace.models import Workplace
from home import tasks
from datetime import datetime, timedelta, time, date
from .templates import *
from contacts.models import MailSend
import random
from datetime import datetime
import pytz


@login_required
def send_all_sme():
    wps = Workplace.objects.filter(workplace_type__in=['A', 'B'])
    for wp in wps:
        emails = []
        if len(wp.get_members())< 6:
            members = wp.get_members()



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
    users = User.objects.filter(userprofile__workplace_type='B')
    now_utc = datetime.now()
    seconds = 40
    template = all_sme_template
    subject = '[CoreLogs] Important notification. See Company DashBoard'
    for user in users:
        up = user.userprofile
        wp = up.primary_workplace
        html_content = template.format(up, wp, wp.slug)
        MailSend.objects.create(user=user, email=user.email, body=html_content, reasons='bulk_m', subject=subject,
                                from_email=random.choice([2, 3, 4]), date=now_utc + timedelta(seconds=seconds))
        seconds += 30


@login_required
def send_mail(request):
    if request.method == 'POST':
        users = []
        users1 = []
        now_utc = datetime.now(pytz.UTC)
        s = request.POST.get('q')
        subject = request.POST.get('subject')

        arguments = request.POST.get('arguments')       # Send tuple like (up, up.primary_workplace)
        bod = request.POST.get('mail')
        body = bod.replace("?:", "{").replace(":?", "}")

        if s == "meh":
            users = User.objects.filter(id__in=[1])

        elif s == 'set_wp_all':
            todaydate = date.today()
            startdate = todaydate + timedelta(days=1)
            enddate = startdate - timedelta(days=40)
            users = User.objects.filter(date_joined__range=[enddate, startdate], userprofile__primary_workplace=None)

        elif s == "alh":
            users = User.objects.all()

        elif s == "ah":
            users = User.objects.filter(userprofile__primary_workplace__workplace_type='A')

        elif s == "bh":
            users = User.objects.filter(userprofile__primary_workplace__workplace_type='B')

        elif s == "ch":
            users = User.objects.filter(userprofile__primary_workplace__workplace_type='C')

        elif s == "oh":
            users = User.objects.filter(userprofile__primary_workplace__workplace_type='O')

        elif s == "nh":
            users = User.objects.filter(userprofile__primary_workplace=None)

        elif s == "ranh":
            questions = Question.objects.filter(answered=False)
            for q in questions:
                tasks.send_html_mail_post(q.user.id, n=Template_answer_your_own_question.format(q.user.userprofile,
                                                                                                q.slug, q.title))

        elif s[:13] == 'mail_wp_users':
            y = s.split('&')[1]
            w = Workplace.objects.get(id=str(y))
            userps = w.get_members()
            users1 = []
            if userps:
                for u in userps:
                    users1.append(u.user)
            else:
                pass
                # wp_mail = w.office_mail_id
                # wp = Workplace.objects.get()
                # a = eval(arguments)
                # html_content = body.format(*a)
                # MailSend.objects.create(email=wp_mail, body=html_content, reasons='dm', subject=subject,
                #                         from_email=random.choice([2, 3, 4]), date=now_utc)

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
        minutes = 1
        if users:
            for user in users:
                up = user.userprofile
                a = eval(arguments)
                template = body
                html_content = template.format(*a)

                MailSend.objects.create(user=user, email=user.email, body=html_content, reasons='bm', subject=subject,
                                        from_email=random.choice([2, 3, 4]), date=now_utc + timedelta(minutes=minutes))
                minutes += 1
        if users1:
            for user in users1:
                up = user.userprofile
                a = eval(arguments)
                template = body
                html_content = template.format(*a)

                MailSend.objects.create(user=user, email=user.email, body=html_content, reasons='dm', subject=subject,
                                        from_email=random.choice([2, 3, 4]), date=now_utc + timedelta(minutes=minutes))
                minutes += 1
    return redirect('/internal/activity')


def send_new_wp(request):
    now_utc = datetime.now(pytz.UTC)
    wps = Workplace.objects.filter(date__range=[now_utc-timedelta(days=5), timedelta(days=3)])

    minutes = 1
    for w in wps:
        ms = w.get_members()
        for m in ms:
            subject = u''''Your Company {0} is Registered'''.format(w)
            html_content = new_sme_tem.format(m, w, w.slug)
            MailSend.objects.create(user=m.user, email=m.user.email, body=html_content, reasons='bm', subject=subject,
                                    from_email=random.choice([2, 3, 4]), date=now_utc + timedelta(minutes=minutes))
            minutes += 1

list_new = []