from django.shortcuts import render, redirect
import os
import subprocess
from chat.models import Message
from datetime import datetime, timedelta, time, date
from home import tasks
from activities.models import Notification


def task_exec(request):
    print('oye bubbly')
    # os.system('cd ..')
    # subprocess.call(['python manage.py process_tasks'])
    subprocess.Popen('python manage.py process_tasks')
    print('oye oye bubbly')
    return redirect('/')


# def check_message_for_mail(request):
#     yesterday = datetime.date.today() - datetime.timedelta(days=1)
#     messages = Message.objects.filter(date__gt=yesterday)
#     li = []
#     for m in messages:
#         user = m.user
#         if not user in li:
#             li.append(user)
#
#     for u in li:
#         tasks.send_one(u.id, n=99)


# def check_notification_for_mail(request):
#     yesterday = date.today() - timedelta(days=1)
#     notifs = Notification.objects.filter(date__gt=yesterday)
#     li = []
#     for m in notifs:
#         user = m.to_user
#         if not user in li:
#             li.append(user)
