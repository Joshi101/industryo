from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from activities.models import Notification, Enquiry
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
import json
from workplace.models import Workplace
from products.models import Products
from datetime import datetime, timedelta, time, date


# @login_required
def notifications(request):
    user = request.user
    read = Notification.objects.filter(to_user=user, is_read=True)
    unread = Notification.objects.filter(to_user=user, is_read=False)
    for notification in unread:
        notification.is_read = True
        notification.save()
    return render(request, 'activities/notifications.html', {'read': read, 'unread': unread})


def count_notify(request):
    if request.method == 'GET':
        response = {}
        user = request.user
        unread_all = Notification.objects.filter(to_user=user, is_read=False)
        c = unread_all.count()
        response['count'] = c
        return HttpResponse(json.dumps(response), content_type="application/json")


def notify(request):
    if request.method == 'GET':
        response = {}
        r_html = {}
        r_elements = []
        user = request.user
        unread = Notification.objects.filter(to_user=user, is_read=False)[:5]
        c = unread.count()
        if c < 5:
            d = 5 - c
            read = Notification.objects.filter(to_user=user, is_read=True)[:d]
        for notification in unread:
            notification.is_read = True
            notification.save()
        r_elements = ['hover_box']
        r_html['hover_box'] = render_to_string('activities/notify_box.html', {'unread': unread, 'read': read, 'count': c})
        response['html'] = r_html
        response['elements'] = r_elements
        return HttpResponse(json.dumps(response), content_type="application/json")
    return redirect('/')

@login_required
# @ajax_required
def last_notifications(request):
    user = request.user
    notifications = Notification.objects.filter(to_user=user, is_read=False)[:5]
    for notification in notifications:
        notification.is_read = True
        notification.save()
    return render(request, 'activities/last_notifications.html', {'notifications': notifications})

@login_required
# @ajax_required
def check_notifications(request):
    user = request.user
    notifications = Notification.objects.filter(to_user=user, is_read=False)[:5]
    return HttpResponse(len(notifications))
# Create your views here.


# def check_notifications(request):
#     todaydate = date.today()
#     startdate = todaydate + timedelta(days=1)
#     enddate = startdate - timedelta(days=6)
#     notifications = Notification.objects.filter(date__range=[enddate, startdate])
#
#



# Create your views here.
