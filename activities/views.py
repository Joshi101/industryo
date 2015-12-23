from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from activities.models import Notification, Enquiry
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.decorators import login_required
import json
from workplace.models import Workplace
from products.models import Products


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
        unread_all = Notification.objects.filter(to_user=user, is_read=True)
        c = unread_all.count()
        unread = unread_all[:5]
        for notification in unread:
            notification.is_read = True
            notification.save()
        r_elements = ['hover_box']
        r_html['hover_box'] = render_to_string('activities/notify_box.html', {'unread': unread, 'count':c})
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




@login_required
def enquiry_all(request):
    user = request.user
    company = user.userprofile.primary_workplace
    products = Products.objects.filter(producer=company)
    enquiries = []
    for p in products:
        e = Enquiry.objects.filter(product=p)
        if e:
            enquiries.append(e)
    # enquiries = Enquiry.objects.filter(workplace=company)
    print(enquiries)

    return render(request, 'enquiry/e_box.html', {
        'enquiries': enquiries,
        })



def enquiry(request, slug):
    id = request.GET.get('slug')
    enquiry = Enquiry.objects.get(id=id)

    return render()




# Create your views here.
