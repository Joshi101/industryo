from django.shortcuts import render
from activities.models import Notification
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required


# @login_required
def notifications(request):
    user = request.user
    read = Notification.objects.filter(to_user=user, is_read=True)
    unread = Notification.objects.filter(to_user=user, is_read=False)
    for notification in unread:
        notification.is_read = True
        notification.save()
    return render(request, 'activities/notifications.html', {'read': read, 'unread': unread})

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


# Create your views here.
