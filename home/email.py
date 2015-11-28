from django.shortcuts import render, redirect, render_to_response, RequestContext
from nodes.models import Node
from nodes.forms import UploadImageForm
from userprofile.models import UserProfile
from activities.models import Notification
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from home import tasks
from django.core.mail import EmailMultiAlternatives
from datetime import datetime, timedelta, time, date


@login_required
def send(request):
    if 'q' in request.GET:
        print("baba")
        s = request.GET.get('q')
        if s == 'set_wp':
            id = request.GET.get('id')
            print(id)
            tasks.send_one(id, n=16)
        elif s == 'set_wp_all':
            todaydate = date.today()
            startdate = todaydate + timedelta(days=1)
            enddate = startdate - timedelta(days=200)
            lis = User.objects.filter(date_joined__range=[enddate, startdate], userprofile__primary_workplace=None)
            for i in lis:
                print(i.id)
                tasks.send_one(i.id, n=16)

    return redirect("/internal/details/?q=u")

@login_required
def send_an_email(request):
    userprofiles = UserProfile.objects.filter(primary_workplace__workplace_type='C')
    # userprofiles = UserProfile.objects.filter(id__lte=1)
    for u in userprofiles:
        tasks.text_mail(u.id, n=16)
    return redirect('/')


def send_set_wp_email(request):

    if request.user.is_authenticated():
        users = User.objects.all()
        for user in users:
            if not user.userprofile.primary_workplace:
                user_email = user.email
                if user.first_name:
                    name = user.get_full_name()
                else:
                    name = user.username
                template = u'''Hi {0},

Did you check www.corelogs.com ? We are getting great questions and answers on our forum. and we need people who can answer.

You have still not set your workplace till now.
To see optimized content, you should tell us where do you work or study.

Thanks & Regards

Surya Prakash
CoreLogs
'''
                content = template.format(name)
                try:
                    send_mail('CoreLogs- Set your Workplace', content, 'site.corelogs@gmail.com', [user_email])
                except Exception:
                    pass
        return redirect('/kabira')
    else:
        return redirect('/rahima')


