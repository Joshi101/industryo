from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
from leads.models import Leads, Reply
from tags.models import Tags
import json
import traceback
from nodes.models import Images, Document
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from contacts.models import MailSend
from datetime import datetime, timedelta
from threading import Thread
from home.templates import *
from django.contrib.auth.decorators import login_required


def delete_tag(request, id):
    if request.method == 'POST':
        lead = Leads.objects.get(id=id)
        tag = request.POST.get('tag')
        t = Tags.objects.get(tag=tag)
        lead.tags.remove(t)
        lead.save()
        return HttpResponse()


def edit_add_lead(request, slug):
    user = request.user
    response = {}
    if slug == 'new':
        if request.method == 'POST':
            if request.POST.get('lead'):
                now = datetime.now()
                ls = {}
                if user.is_authenticated():
                    ls = Leads.objects.filter(user=user, date__range=[now-timedelta(days=1), now])
                if len(ls) < 100:
                    if user.is_authenticated():
                        wp = user.userprofile.primary_workplace
                        l = Leads.objects.create(lead=request.POST['lead'], user=user, workplace=wp)
                    else:
                        l = Leads.objects.create(lead=request.POST['lead'], name=request.POST['user_name'], email=request.POST['user_email'], company_name=request.POST['user_company'], mobile_number=request.POST['user_mobile'])
                    t = Thread(target=leads_mail, args=(l.id, 'created'))
                    t.start()
                    direct = l._meta.get_all_field_names()
                    dictionary = {}
                    for key in request.POST:
                        if key in direct:
                            try:
                                dictionary[key] = request.POST[key]
                            except:
                                tb = traceback.format_exc()
                        elif key == 'city':
                            l.set_tags(request.POST[key])
                        elif key == 'other':
                            l.set_tags(request.POST[key])
                        if key == 'anonymous1':
                            l.anonymous = False
                            l.save()

                    for key in dictionary:
                        setattr(l, key, dictionary[key])
                    l.save()
                    image1 = request.FILES.get('photo', None)
                    if image1:
                        i = Images()
                        x = i.upload_image(image=image1, user=user)
                        l.image = x
                        l.save()
                    response['l_id'] = l.id

                    doc1 = request.FILES.get('doc1', None)
                    if doc1:
                        d = Document()
                        x = d.upload_doc(doc=doc1, user=user)
                        l.doc = x
                        l.save()
                    return redirect('/leads/')
                else:
                    return HttpResponse()
        else:
            first_time = True
            if user.is_authenticated():
                lg = Leads.objects.filter(user=user)
                if len(lg) > 1:
                    first_time = False
            return render(request, 'leads/edit.html', {'first_time': False})
    else:
        l = Leads.objects.get(slug=slug)
        direct = l._meta.get_all_field_names()
        dictionary = {}
        if request.method == 'POST' and user == l.user:
            for key in request.POST:
                if key in direct:
                    try:
                        dictionary[key] = request.POST[key]
                    except:
                        tb = traceback.format_exc()
                elif key == 'city':
                    l.set_tags(request.POST[key])
                elif key == 'other':
                    l.set_tags(request.POST[key])
                if key == 'anonymous1':
                            l.anonymous = False
                            l.save()

            for key in dictionary:
                setattr(l, key, dictionary[key])
            l.save()
            image1 = request.FILES.get('photo', None)
            if image1:
                i = Images()
                x = i.upload_image(image=image1, user=user)
                l.image = x
                l.save()
            response['l_id'] = l.id

            doc1 = request.FILES.get('doc', None)
            if doc1:
                d = Document()
                x = d.upload_doc(doc=doc1, user=user)
                l.doc = x
                l.save()
            response['l_id'] = l.id
            return HttpResponse(json.dumps(response), content_type="application/json")
        else:
            dictionary = {'lead': l, 'first_time': True}
            return render(request, 'leads/edit.html', dict(list(l.__dict__.items()) + list(dictionary.items())))


def leads(request):
    q = request.GET.get('q')
    user = request.user
    if user.is_authenticated():
        if user.userprofile.workplace_type is not 'N':
            wp = user.userprofile.primary_workplace
    if q == 'open':
        leads = Leads.object.filter(status=True).order_by('-date')
    elif q == 'closed':
        leads = Leads.object.filter(status=False).order_by('-date')
    elif q == 'my':
        leads = Leads.object.filter(user=user).order_by('-date')
    else:
        leads = Leads.objects.all().order_by('-date')
    paginator = Paginator(leads, 10)
    page = request.GET.get('page')
    try:
        result_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        result_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        return
    if page:
        return render(request, 'leads/five_leads.html', {'result_list': result_list})
    else:
        # return render(request, 'home.html', {'result_list': result_list})
        return render(request, 'leads/leads.html', {'result_list': result_list})


@login_required
def get_lead(request, slug):
    lead = Leads.objects.get(slug=slug)
    replies = Reply.objects.filter(lead=lead)
    user = request.user
    user_reply = Reply.objects.filter(user=user, lead=lead)
    if request.user == lead.user:
        show_all = True
    elif len(user_reply) > 0:
        show_one = True
    lead.seen_by += 1
    lead.save()
    return render(request, 'leads/lead.html', locals())


def close_lead(request, id):
    lead = Leads.objects.get(id=id)
    if request.user == lead.user:
        if lead.status:
            lead.status = False
            lead.save()
        else:
            lead.status = True
            lead.save()
    return HttpResponse


def close_lead1(id):
    lead = Leads.objects.get(id=id)
    if lead.status:
        lead.status = False
        lead.save()
        t = Thread(target=leads_mail, args=(id, 'close'))
        t.start()
    else:
        pass


def accept_reply(request, id):
    quotation = Reply.objects.get(id=id)
    if request.user == quotation.lead.user:
        if quotation.selected:
            quotation.selected = False
            quotation.save()
        else:
            quotation.selected = True
            quotation.save()
            t = Thread(target=quotation_mail, args=(quotation.id, 'accepted'))
            t.start()
    return HttpResponse


@login_required
def reply_lead(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        user = request.user
        wp = user.userprofile.primary_workplace
        lead = Leads.objects.get(id=id)
        # r = Reply()
        # direct = r._meta.get_all_field_names()
        direct = ['message', 'price', 'time_to_deliver', 'taxes', 'delivery_charges', 'payment_terms', 'quality_assurance']
        dictionary = {}
        now = datetime.now()
        rs = Reply.objects.filter(user=user, date__range=[now-timedelta(days=1), now])
        if len(rs) < 10:
            reply = Reply.objects.create(user=user, workplace=wp, lead=lead)
            t = Thread(target=quotation_mail, args=(reply.id, 'quotation'))
            t.start()
            for key in request.POST:
                if key in direct:
                    try:
                        dictionary[key] = request.POST[key]
                    except:
                        tb = traceback.format_exc()
            for key in dictionary:
                setattr(reply, key, dictionary[key])
            reply.save()
            doc1 = request.FILES.get('doc21', None)
            doc2 = request.FILES.get('doc22', None)
            if doc1:
                d = Document()
                x = d.upload_doc(doc=doc1, user=user)
                reply.doc = x
                reply.save()
            if doc2:
                d = Document()
                x = d.upload_doc(doc=doc2, user=user)
                reply.doc = x
                reply.save()
            lead.responses +=1
            lead.save()
        return redirect('/leads/'+lead.slug)


def pre_edit_reply(request, id):
    reply = Reply.objects.get(id=id)
    return render(request, 'leads/quotation_edit.html', locals())


def edit_reply(request, id):
    reply = Reply.objects.get(id=id)
    dictionary = {}
    response = {}
    if request.user == reply.user:
        if request.method == 'POST':
            direct = ['message', 'price', 'time_to_deliver', 'taxes', 'delivery_charges', 'payment_terms', 'quality_assurance']
            for key in request.POST:
                if key in direct:
                    try:
                        dictionary[key] = request.POST[key]
                    except:
                        tb = traceback.format_exc()
            for key in dictionary:
                setattr(reply, key, dictionary[key])
            reply.save()
            response['status'] = True
            return HttpResponse(json.dumps(response), content_type="application/json")
        else:
            return render(request, 'leads/one_reply_2.html', locals())


def leads_mail(id, x):
    lead = Leads.objects.get(id=id)
    user = lead.user
    now = datetime.now()
    if x == 'created':
        mail_body = lead_created.format(user.userprofile, lead, lead.slug)
        subject = 'Hey {0} You Just Created a FREE Business Lead on CoreLogs'.format(user.userprofile)
        MailSend.objects.create(email=user.email, body=mail_body, reasons='lcm', from_email='4',
                                date=now + timedelta(minutes=2), subject=subject)
    if x == 'close':
        mail_body = lead_closed.format(user.userprofile, lead, lead.slug)
        subject = 'Hey {0} Your Lead has been Closed on CoreLogs'.format(lead.user.userprofile)
        MailSend.objects.create(email=user.email, body=mail_body, reasons='jcm', from_email='4',
                                date=now + timedelta(minutes=2), subject=subject)


def quotation_mail(id, x):
    reply = Reply.objects.get(id=id)
    lead = reply.lead
    replies = Reply.objects.filter(lead=lead)
    now = datetime.now()
    if x == 'quotation':
        if len(replies) == 1:
            mail_body = one_quotation.format(lead.user.userprofile, lead, lead.slug)
            subject = 'Hey {0} You have got a quotation on Lead on CoreLogs'.format(reply.lead.user.userprofile)
            MailSend.objects.create(email=reply.lead.user.email, body=mail_body, reasons='jcm', from_email='4',
                                    date=now + timedelta(minutes=2), subject=subject)
        elif len(replies) == 2:
            mail_body = multiple_quotation.format(lead.user.userprofile, lead, lead.slug)
            subject = 'Hey {0} You have got Multiple quotations on Lead'.format(reply.lead.user.userprofile)
            MailSend.objects.create(email=reply.lead.user.email, body=mail_body, reasons='jcm', from_email='4',
                                    date=now + timedelta(minutes=2), subject=subject)
        else:
            pass
    elif x == 'accepted':
        mail_body = quotation_accepted.format(reply.user.userprofile, lead, lead.slug)
        subject = 'Your Quotation on this lead has been accepted See Details'.format(reply.lead.user.userprofile)
        MailSend.objects.create(email=reply.lead.user.email, body=mail_body, reasons='jcm', from_email='4',
                                date=now + timedelta(minutes=2), subject=subject)
        if len(replies) > 1:
            for r in replies:
                if not r == reply:
                    mail_body = quotation_rejected.format(reply.user.userprofile, lead, lead.slug)
                    subject = 'Hey {0} You have got a quotation on Lead on CoreLogs'.format(reply.lead.user.userprofile)
                    MailSend.objects.create(email=reply.lead.user.email, body=mail_body, reasons='jcm', from_email='4',
                                            date=now + timedelta(minutes=2), subject=subject)
