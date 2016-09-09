from django.shortcuts import render, HttpResponse, redirect
from activities.models import Enquiry
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta, date
from products.models import Products
from workplace.models import Workplace
from home.tasks import execute_view
import json


def enquire(request):
    yesterday = date.today() - timedelta(days=1)
    if request.method == 'POST':
        message = request.POST.get('message')
        # if len(message.split(' ')) == 1:
        #     pass
        # elif len(message.split(' ')) < 4:
        #     if 'http' or 'www' in message:
        #         pass
        # elif len(message.split(' ')) > 70:
        #     pass
        if request.user.is_authenticated():
            p = request.POST.get('pid')
            w = request.POST.get('wid')
            user = request.user
            phone = request.POST.get('phone')
            e = Enquiry.objects.filter(user=user, date__gt=yesterday)
            if p:
                prod = Products.objects.get(id=p)
                if e.count() < 5:
                    e = Enquiry.objects.create(product=prod, user=user, message=message, phone_no=phone,
                                               workplace=prod.producer)
                    users = e.product.producer.get_members()
                    # user.userprofile.notify_inquired(e, users)
                    # send_enq_mail(e)
                    execute_view('check_no_inquiry', e.id,
                                 schedule=timedelta(seconds=30))

            if w:
                workplace = Workplace.objects.get(id=w)
                if e.count() < 5:
                    # Checking if the same person has created more than 5
                    # inquiries that day
                    e = Enquiry.objects.create(
                        workplace=workplace, user=user, message=message, phone_no=phone)
                    users = workplace.get_members()
                    # user.userprofile.notify_inquired(e, users)
                    execute_view('check_no_inquiry', e.id,
                                 schedule=timedelta(seconds=30))
            # if request.is_ajax():
            #     return HttpResponse(json.dumps(response), content_type="application/json")
            # else:
            return redirect('/marketplace')
        else:
            email = request.POST.get('email')
            name = request.POST.get('name')
            company = request.POST.get('company')
            p = request.POST.get('pid')
            w = request.POST.get('wid')
            message = request.POST.get('message')
            phone = request.POST.get('phone')
            e = Enquiry.objects.filter(email=email, date__gt=yesterday)
            response = {}
            if p:
                prod = Products.objects.get(id=p)
                if e.count() < 5:
                    # Checking if the same person has created more than 5
                    # inquiries that day
                    e = Enquiry.objects.create(product=prod, name=name, company=company,
                                               email=email, message=message,
                                               phone_no=phone)
                    up = prod.user.userprofile
                    # up.notify_inquired(e)
                    # send_enq_mail(e)
                    execute_view('check_no_inquiry', e.id,
                                 schedule=timedelta(seconds=30))
            if w:
                workplace = Workplace.objects.get(id=w)
                if e.count() < 5:
                    e = Enquiry.objects.create(workplace=workplace, name=name, company=company,
                                               message=message, phone_no=phone)
                    # up.notify_inquired(e)
                    execute_view('check_no_inquiry', e.id,
                                 schedule=timedelta(seconds=30))
            response['data'] = {'name': name, 'company': company, 'email': email}
            if request.is_ajax():
                return HttpResponse(json.dumps(response), content_type="application/json")
            else:
                return redirect('/marketplace')
