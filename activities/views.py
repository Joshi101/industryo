from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from activities.models import Notification
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import json
from datetime import datetime, timedelta
from contacts.models import MailSend


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
    to_user = kwargs.get('to_user')
    from_user = kwargs['from_user']
    to_users = kwargs.get('to_users')
    typ = kwargs['typ']
    node = kwargs.get('node')
    workplace = kwargs.get('workplace')
    answer = kwargs.get('answer')
    question = kwargs.get('question')
    enquiry = kwargs.get('enquiry')
    if to_users:
        for user in to_users:
            if not from_user == user:
                n = Notification.objects.create(from_user=from_user, to_user=user, notification_type=typ, workplace=workplace,
                                                node=node, answer=answer, question=question, enquiry=enquiry)
    elif to_user:
        if not from_user == to_user:
            n = Notification.objects.create(from_user=from_user, to_user=to_user, notification_type=typ, workplace=workplace,
                                            node=node, answer=answer, question=question, enquiry=enquiry)


def delete_notifications(**kwargs):
    to_user = kwargs.get('to_user')
    from_user = kwargs['from_user']
    to_users = kwargs.get('to_users')
    typ = kwargs.get('typ')
    node = kwargs.get('node')
    workplace = kwargs.get('workplace')
    answer = kwargs.get('answer')
    question = kwargs.get('question')
    enquiry = kwargs.get('enquiry')
    if to_users:
        for user in to_users:
            if not from_user == user:
                n = Notification.objects.filter(from_user=from_user, to_user=user, notification_type=typ, workplace=workplace,
                                                node=node, answer=answer, question=question, enquiry=enquiry).delete()
    elif to_user:
        if not from_user == to_user:
            Notification.objects.filter(from_user=from_user, to_user=to_user, notification_type=typ, workplace=workplace,
                                        node=node, answer=answer, question=question, enquiry=enquiry).delete()


def notification_mails():
    now = datetime.now()
    start_time = now - timedelta(hours=1)
    notification_all = Notification.objects.filter(mail_sent=False, date__range=[start_time, now+timedelta(days=1)])
    for n in notification_all:
        if n.notification_type in ['L', 'U', 'C', 'J', 'N', 'A']:
            subject = n.get_subject()
            html_content = n.get_html()
            text_content = n.get_text()
            m = MailSend.objects.create(email=n.to_user.email, subject=subject, body=html_content, reasons='nm',
                                        text_content=text_content, date=now)
            n.mail_sent = True
            n.save()


# Create your views here.