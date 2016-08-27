from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from activities.models import Notification
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import json


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
def last_notifications(request):
    user = request.user
    notifications = Notification.objects.filter(to_user=user, is_read=False)[:5]
    for notification in notifications:
        notification.is_read = True
        notification.save()
    return render(request, 'activities/last_notifications.html', {'notifications': notifications})

@login_required
def check_notifications(request):
    user = request.user
    notifications = Notification.objects.filter(to_user=user, is_read=False)[:5]
    return HttpResponse(len(notifications))


def create_notifications(**kwargs):
    to_user = kwargs['to_user']
    from_user = kwargs['from_users']
    to_users = kwargs['to_users']
    node = workplace = answer = question = enquiry = None
    direct = ['node', 'workplace', 'answer', 'question', 'enquiry']
    for key in kwargs:
        if key in direct:
            key = kwargs['key']
    typ = kwargs['typ']
    if to_users:
        for to_user in to_users:
            if not from_user == to_user:
                n = Notification.objects.create(from_user=from_user, to_user=to_user, typ=typ, workplace=workplace,
                                                node=node, answer=answer, question=question, enquiry=enquiry)
    elif to_user:
        if not from_user == to_user:
            n = Notification.objects.create(from_user=from_user, to_user=to_user, typ=typ, workplace=workplace,
                                            node=node, answer=answer, question=question, enquiry=enquiry)


def delete_notifications(**kwargs):
    to_user = kwargs['to_user']
    from_user = kwargs['from_users']
    to_users = kwargs['to_users']
    node = workplace = answer = question = enquiry = None
    direct = ['node', 'workplace', 'answer', 'question', 'enquiry']
    for key in kwargs:
        if key in direct:
            key = kwargs['key']
    typ = kwargs['typ']
    if to_users:
        for to_user in to_users:
            if not from_user == to_user:
                n = Notification.objects.create(from_user=from_user, to_user=to_user, typ=typ, workplace=workplace,
                                                node=node, answer=answer, question=question, enquiry=enquiry).delete()
    elif to_user:
        if not from_user == to_user:
            Notification.objects.create(from_user=from_user, to_user=to_user, typ=typ, workplace=workplace,
                                        node=node, answer=answer, question=question, enquiry=enquiry).delete()


# Create your views here.