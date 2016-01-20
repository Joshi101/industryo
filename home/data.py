from django.shortcuts import render, redirect, render_to_response, RequestContext
from workplace.models import Workplace, WpTags
from products.models import Products
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from datetime import datetime, timedelta, time, date


@login_required
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

@login_required
def details(request):
    if 'q' in request.GET:
        s = request.GET.get('q')
        todaydate = date.today()
        startdate = todaydate + timedelta(days=1)
        enddate = startdate - timedelta(days=40)
        users = User.objects.filter(date_joined__range=[enddate, startdate])
        workplaces = Workplace.objects.filter(date__range=[enddate, startdate])
        if s == 'ub':
            lis = User.objects.filter(date_joined__range=[enddate, startdate], userprofile__primary_workplace__workplace_type='B')
            text = "Users from SMES"
            tt = "u"
        elif s == 'uc':
            lis = User.objects.filter(date_joined__range=[enddate, startdate], userprofile__primary_workplace__workplace_type='C')
            text = "Users from Teams"
            tt = "u"
        elif s == 'ua':
            lis = User.objects.filter(date_joined__range=[enddate, startdate], userprofile__primary_workplace__workplace_type='A')
            text = "Users from Large scale Industries"
            tt = "u"
        elif s == 'uo':
            lis = User.objects.filter(date_joined__range=[enddate, startdate], userprofile__primary_workplace__workplace_type='O')
            text = "Users from Educational Institutions"
            tt = "u"
        elif s == 'u':
            lis = User.objects.filter(date_joined__range=[enddate, startdate], userprofile__primary_workplace=None)
            text = "Users who have not set their Workplace"
            tt = "u"
            tm = "q"

        elif s == 'wb':
            lis = Workplace.objects.filter(date__range=[enddate, startdate], workplace_type='B')
            text = "SMEs registered"
            tt = "w"
        elif s == 'wc':
            lis = Workplace.objects.filter(date__range=[enddate, startdate], workplace_type='C')
            text = "Teams Registered"
            tt = "w"
        elif s == 'wa':
            lis = Workplace.objects.filter(date__range=[enddate, startdate], workplace_type='A')
            text = "Large scale Industries registered"
            tt = "w"
        elif s == 'wo':
            lis = Workplace.objects.filter(date__range=[enddate, startdate], workplace_type='O')
            text = "Educational Institutions registered"
            tt = "w"

        elif s == 'p':
            lis = Products.objects.filter(date__range=[enddate, startdate])
            text = "Products registered"
            tt = "p"
        elif s == 'wpt':
            lis = WpTags.objects.filter(date__range=[enddate, startdate])
            text = "Workplace Tags created"
            tt = "wpt"

        c = len(lis)
        return render(request, 'activities/activity.html', locals())
    else:
        return render(request, 'activities/activity.html', locals())


