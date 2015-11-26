from django.shortcuts import render, redirect, render_to_response, RequestContext
from nodes.models import Node
from nodes.forms import UploadImageForm
from userprofile.models import UserProfile
from workplace.models import Workplace, WpTags
from forum.models import Question
from tags.models import Tags
from products.models import Products
from itertools import chain
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from operator import attrgetter
from activities.models import Notification
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from datetime import datetime, timedelta, time, date


def activity(request):

    c = User.objects.all()
    workplaces = Workplace.objects.all()

    todaydate = date.today()
    startdate = todaydate + timedelta(days=1)
    enddate = startdate - timedelta(days=6)
    users = User.objects.filter(date_joined__range=[enddate, startdate])
    workplaces = Workplace.objects.filter(date__range=[enddate, startdate])
    products = Products.objects.filter(date__range=[enddate, startdate])
    # wptags = W
    return render(request, 'activities/activity.html', locals())


def details(request):
    if 'q' in request.GET:
        s = request.GET.get('q')
        todaydate = date.today()
        startdate = todaydate + timedelta(days=1)
        enddate = startdate - timedelta(days=200)
        users = User.objects.filter(date_joined__range=[enddate, startdate])
        workplaces = Workplace.objects.filter(date__range=[enddate, startdate])
        if s == 'ub':
            lis = User.objects.filter(date_joined__range=[enddate, startdate], user__userprofile__primary_workplace__workplace_type='B')
            text = "Users from SMES"
        elif s == 'uc':
            lis = User.objects.filter(date_joined__range=[enddate, startdate], user__userprofile__primary_workplace__workplace_type='C')
            text = "Users from Teams"
        elif s == 'ua':
            lis = User.objects.filter(date_joined__range=[enddate, startdate], user__userprofile__primary_workplace__workplace_type='A')
            text = "Users from Large scale Industries"
        elif s == 'uo':
            lis = User.objects.filter(date_joined__range=[enddate, startdate], user__userprofile__primary_workplace__workplace_type='O')
            text = "Users from Educational Institutions"
        elif s == 'u':
            lis = User.objects.filter(date_joined__range=[enddate, startdate], user__userprofile__primary_workplace=None)
            text = "Users who have not set their Workplace"

        elif s == 'wb':
            lis = Workplace.objects.filter(date__range=[enddate, startdate], workplace_type='B')
            text = "SMEs registered"
        elif s == 'wc':
            lis = Workplace.objects.filter(date__range=[enddate, startdate], workplace_type='C')
            text = "Teams Registered"
        elif s == 'wa':
            lis = Workplace.objects.filter(date__range=[enddate, startdate], workplace_type='A')
            text = "Large scale Industries registered"
        elif s == 'wo':
            lis = Workplace.objects.filter(date__range=[enddate, startdate], workplace_type='O')
            text = "Educational Institutions registered"

        c = len(lis)
        return render(request, 'activities/activity.html', locals())
    else:
        return render(request, 'activities/activity.html', locals())


