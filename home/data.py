from django.shortcuts import render, redirect
from workplace.models import Workplace, WpTags
from products.models import Products, Category
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from datetime import datetime, timedelta, time, date
from activities.models import Enquiry
import pytz
from contacts.models import MailSend
from tags.models import Tags


@login_required
def activity(request):

    c = User.objects.all()
    workplaces = Workplace.objects.all()

    now = datetime.now(pytz.utc)
    startdate = now
    enddate = startdate - timedelta(days=7)
    sme_c_w = Workplace.objects.filter(workplace_type='B', date__range=[enddate, startdate]).count()
    prod_c_w = Products.objects.filter(date__range=[enddate, startdate]).count()
    inq_c_w = Enquiry.objects.filter(date__range=[enddate, startdate]).count()
    u_c_w = User.objects.filter(date_joined__range=[enddate, startdate]).count()
    # # wptags = W
    sme_c = Workplace.objects.filter(workplace_type__in=['B', 'A']).count()
    prod_c = Products.objects.all().count()
    inq_c = Enquiry.objects.all().count()
    u_c = User.objects.all().count()
    startdate = datetime.now(pytz.utc)
    enddate = startdate - timedelta(days=1)
    m = MailSend.objects.filter(sent=True, date__range=[enddate, startdate])
    c_s = len(m)
    return render(request, 'activities/activity.html', locals())

@login_required
def details(request):
    if 'q' in request.GET:
        s = request.GET.get('q')
        # todaydate = date.today()
        startdate = datetime.now(pytz.utc)
        enddate = startdate - timedelta(days=7)
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
            lis = User.objects.filter(date_joined__range=[startdate-timedelta(days=200), startdate], userprofile__primary_workplace=None)
            text = "Users who have not set their Workplace"
            tt = "u"
            tm = "q"

        elif s == 'wb':
            lis = Workplace.objects.filter(date__range=[startdate-timedelta(days=200), startdate], workplace_type='B')
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
            lis = Products.objects.filter(date__range=[startdate-timedelta(days=100), startdate])
            # lis = Products.objects.filter(date__range=[enddate, startdate])
            text = "Products Listed"
            tt = "p"

        elif s == 'c':
            lis = Category.objects.all()
            # lis = Products.objects.filter(date__range=[enddate, startdate])
            text = "Categories"
            tt = "c"

        elif s == 'pp':
            lis = Products.objects.filter(categories=None)
            # lis = Products.objects.filter(date__range=[enddate, startdate])
            text = "Products Listed"
            tt = "p"
        elif s == 'wpt':
            lis = WpTags.objects.filter(date__range=[startdate-timedelta(days=200), startdate])
            text = "Workplace Tags created"
            tt = "wpt"
        elif s == 'enq':
            lis = Enquiry.objects.filter(date__range=[startdate-timedelta(days=60), startdate])
            return render(request, 'activities/enquiry.html', locals())
        elif s == 'ms':
            lis = MailSend.objects.filter(date__range=[startdate-timedelta(days=1), startdate])
            tt = "ms"
            text = "Mail Send in Queue for today"
        elif s == 'tt':
            lis = Tags.objects.filter(date__range=[startdate - timedelta(days=100), startdate])
            tt = "tt"
            text = "Tags Created in last 4 days"
        c = len(lis)
        return render(request, 'activities/activity.html', locals())
    else:

        return render(request, 'activities/activity.html', locals())


def change_wp_u(request):
    if request.method == 'POST':
        u = request.POST.get('u')
        w = request.POST.get('w')
        workplace = Workplace.objects.get(slug=w)
        us = u.split(', ')
        for use in us:
            user = User.objects.get(username=use)
            user.userprofile.primary_workplace = workplace
            user.userprofile.save()
        return redirect('/')

    else:
        return render(request, 'activities/input.html', locals())


def change_p_o(request):
    if request.method == 'POST':
        u = request.POST.get('u')
        w = request.POST.get('w')
        uploader = User.objects.get(username=u)
        to_be_uploader = User.objects.get(username=w)
        p = Products.objects.filter(user=uploader)
        for prod in p:
            prod.user = to_be_uploader
            prod.save()
        return redirect('/')

    else:
        return render(request, 'activities/input.html', locals())