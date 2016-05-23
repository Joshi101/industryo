from django.shortcuts import render, redirect, render_to_response, RequestContext, HttpResponse
from allauth.socialaccount.models import SocialAccount, SocialToken
import urllib.request as urllib2
from xml.etree import ElementTree as etree
from allauth.socialaccount.models import SocialToken
from .models import ContactEmails, MailSend
from django.contrib.auth.models import User
from datetime import datetime, timedelta, time, date
import pytz
from activities.models import Enquiry
from django.template.loader import render_to_string, get_template
from django.template import Context
from home.templates import *


def get_google_contacts(request):
    # social = request.user.social_auth.get(provider='google-oauth2')
    user =request.user

    # Code dependent upon django-allauth. Will change if we shift to another module

    # if request.user.userprofile.get_provider() != "google":
    a = SocialAccount.objects.get(user=user, provider='Google')
    b = SocialToken.objects.get(account=a)
    # access = b.token
    access_token = b.token
    url = 'https://www.google.com/m8/feeds/contacts/default/full' + '?access_token=' + access_token + '&max-results=1000'
    req = urllib2.Request(url, headers={'User-Agent' : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.30 (KHTML, like Gecko) Ubuntu/11.04 Chromium/12.0.742.112 Chrome/12.0.742.112 Safari/534.30"})
    contacts = urllib2.urlopen(req).read()
    contacts_xml = etree.fromstring(contacts)

    result = []

    for entry in contacts_xml.findall('{http://www.w3.org/2005/Atom}entry'):
        for address in entry.findall('{http://schemas.google.com/g/2005}email'):
            email = address.attrib.get('address')
            result.append(email)
            c = ContactEmails.object.create(email=email, provider='google', user=user)

    return render(request, 'search/random_text_print.html', locals())


def get_facebook_contacts(request):
    user = request.user
    a = SocialAccount.objects.get(user=user, provider='facebook')
    b = SocialToken.objects.get(account=a)
    # access = b.token
    me = a.extra_data['id']
    access_token = b.token
    url = 'https://graph.facebook.com/'+me+'/friends?access_token='+access_token
    req = urllib2.Request(url, headers={'User-Agent' : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.30 (KHTML, like Gecko) Ubuntu/11.04 Chromium/12.0.742.112 Chrome/12.0.742.112 Safari/534.30"})
    contacts = urllib2.urlopen(req).read()
    return render(request, 'search/random_text_print.html', locals())


def get_google_contacts_i(user):
    # social = request.user.social_auth.get(provider='google-oauth2')
    user = user

    # Code dependent upon django-allauth. Will change if we shift to another module

    # if request.user.userprofile.get_provider() != "google":
    a = SocialAccount.objects.get(user=user)
    b = SocialToken.objects.get(account=a)
    # access = b.token
    access_token = b.token
    url = 'https://www.google.com/m8/feeds/contacts/default/full' + '?access_token=' + access_token + '&max-results=1000'
    req = urllib2.Request(url, headers={'User-Agent' : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.30 (KHTML, like Gecko) Ubuntu/11.04 Chromium/12.0.742.112 Chrome/12.0.742.112 Safari/534.30"})
    contacts = urllib2.urlopen(req).read()
    contacts_xml = etree.fromstring(contacts)

    result = []

    for entry in contacts_xml.findall('{http://www.w3.org/2005/Atom}entry'):
        for address in entry.findall('{http://schemas.google.com/g/2005}email'):
            email = address.attrib.get('address')
            result.append(email)
            c = ContactEmails.objects.create(email=email, provider='google', user=user)

    return locals()


'''abbrebiations:
lmp: List more products
swp: Set workplace
wim: workplace intro mail
pim: Product intro mail
npy: no products yet
ipm: inquiry product mail
iwm: inquiry wp mail
jcm: join corelogs mail
'''


def check_no_wp(id):
    up = User.objects.get(id=id).userprofile
    now_utc = datetime.now(pytz.utc)
    now = datetime.now()
    if up.workplace_type == 'N':
        subject = '[CoreLogs] {0}, Register your Company'.format(up)
        mail_body = set_wp_mail.format(up)
        if up.date_joined > now_utc - timedelta(minutes=10):
            MailSend.objects.create(user=up.user, body=mail_body, reasons='swp', from_email='2',
                                    date=now_utc + timedelta(minutes=1), email=up.get_email0(), subject=subject)
        elif up.date_joined > now_utc - timedelta(days=7):
            MailSend.objects.create(user=up.user, body=mail_body, reasons='swp', from_email='2',
                                    date=now_utc + timedelta(days=2), email=up.get_email0(), subject=subject)
    elif up.workplace_type in ['A', 'B']:
        check_no_products(id)
        wp = up.primary_workplace
        mail_body = wp_intro_mail.format(up, wp, wp.slug)
        subject = '[CoreLogs] The Front Page of {0} on Internet'.format(wp)
        if up.date_joined > now_utc - timedelta(minutes=10):
            MailSend.objects.create(user=up.user, body=mail_body, reasons='wim', from_email='3',
                                    date=now_utc + timedelta(minutes=2), email=up.get_email0(), subject=subject)
        elif up.date_joined > now_utc - timedelta(days=7):
            MailSend.objects.create(user=up.user, body=mail_body, reasons='wim', from_email='3',
                                    date=now_utc + timedelta(days=2), email=up.get_email0(), subject=subject)

        # mail_body2 = render_to_string('emails/product_intro_mail.html', {'0': up, '1': wp, '2': wp.slug})
        # mail_body2 = product_intro_mail.format(up, wp, wp.slug)
        # subject2 = '[CoreLogs] {0}, List Products & Services among SMEs'.format(up)
        # if up.date_joined > now_utc - timedelta(hours=10):
        #     MailSend.objects.create(user=up.user, body=mail_body2, reasons='pim', subject=subject2,
        #                             date=now_utc + timedelta(minutes=2), email=up.get_email0())


def check_no_products(id):
    up = User.objects.get(id=id).userprofile
    if up.workplace_type in ['A', 'B']:
        wp = up.primary_workplace
        now = datetime.now()
        now_utc = datetime.now(pytz.utc)
        mail_body = product_intro_mail.format(up, wp, wp.slug)
        subject = '[CoreLogs] {0}, List Products & Services among SMEs'.format(up)
        if up.date_joined > now_utc - timedelta(minutes=10):
            MailSend.objects.create(user=up.user, body=mail_body, reasons='pim', from_email='3',
                                    date=now_utc + timedelta(minutes=2), email=up.get_email0(), subject=subject)
            MailSend.objects.create(user=up.user, body=mail_body, reasons='pim', from_email='3',
                                    date=now_utc + timedelta(hours=23), email=up.get_email0(), subject=subject)
        if wp.get_product_count() == 0:
            mail_body2 = no_products_yet.format(up, wp, wp.slug)
            subject2 = '[CoreLogs] {0}, Nobody has listed any Product from your Company'.format(up)
            if up.date_joined > now_utc - timedelta(minutes=10):
                MailSend.objects.create(user=up.user, body=mail_body2, reasons='npy', from_email='2',
                                        date=now_utc + timedelta(days=1), email=up.get_email_prod(), subject=subject2)
            elif up.date_joined > now_utc - timedelta(days=7):
                MailSend.objects.create(user=up.user, body=mail_body2, reasons='npy', from_email='2',
                                        date=now_utc + timedelta(days=2), email=up.get_email_prod(), subject=subject2)
        else:
            mail_body = list_more_products.format(up, wp, wp.slug, wp.get_product_count())
            subject = '[CoreLogs] {0}, List More Products & Services'.format(up)
            if up.date_joined > now_utc - timedelta(minutes=10):
                MailSend.objects.create(user=up.user, body=mail_body, reasons='lmp', from_email='2',
                                        date=now_utc + timedelta(minutes=5), email=up.get_email_prod(), subject=subject)
            elif up.date_joined > now_utc - timedelta(days=7):
                MailSend.objects.create(user=up.user, body=mail_body, reasons='lmp', from_email='2',
                                        date=now_utc + timedelta(days=2), email=up.get_email_prod(), subject=subject)


def check_no_inquiry(id):
    e = Enquiry.objects.get(id=id)
    if e.seen is False:
        now = datetime.now()
        now_utc = datetime.now(pytz.utc)
        if e.product:
            to_up = e.product.user.userprofile
            mail_body = inquiry_product_mail.format(to_up, e.product.slug, e.product,
                                                    e.product.producer.slug, e.product.producer)
            subject = '[CoreLogs] Important! You Got an Inquiry'
            if e.date > now_utc - timedelta(minutes=10):
                MailSend.objects.create(user=to_up.user, body=mail_body, reasons='ipm', from_email='1', enquiry=e,
                                        date=now_utc + timedelta(minutes=2), email=to_up.get_email_prod(), subject=subject)
            elif e.date > now_utc - timedelta(days=7):
                MailSend.objects.create(user=to_up.user, body=mail_body, reasons='ipm', subject=subject, from_email='2',
                                        date=now_utc + timedelta(hours=44), email=to_up.get_email_prod(), enquiry=e)

        else:
            wp = e.workplace
            subject = '[CoreLogs] Important! You Got an Inquiry'
            if wp.get_members_count() < 4:
                members = wp.get_members()
                for up in members:
                    if e.date > now_utc - timedelta(minutes=10):
                        mail_body = inquiry_workplace_mail.format(up)
                        MailSend.objects.create(user=up.user, body=mail_body, reasons='iwm', subject=subject, from_email='2',
                                                date=now_utc + timedelta(minutes=2), email=up.get_email_prod, enquiry=e)
                    elif e.date > now_utc - timedelta(days=7):
                        mail_body = inquiry_workplace_mail.format(up)
                        MailSend.objects.create(user=up.user, body=mail_body, reasons='iwm', subject=subject, from_email='2',
                                                date=now_utc + timedelta(hours=44), email=up.get_email_prod, enquiry=e)
            else:
                members = wp.get_members().order_by('?')[:3]
                for up in members:
                    if e.date > now_utc - timedelta(minutes=10):
                        mail_body = inquiry_workplace_mail.format(up)
                        MailSend.objects.create(user=up.user, body=mail_body, reasons='iwm', subject=subject, from_email='2',
                                                date=now_utc + timedelta(minutes=2), email=up.get_email_prod, enquiry=e)
                    elif e.date > now_utc - timedelta(days=7):
                        mail_body = inquiry_workplace_mail.format(up)
                        MailSend.objects.create(user=up.user, body=mail_body, reasons='iwm', subject=subject, from_email='2',
                                                date=now_utc + timedelta(hours=44), email=up.get_email_prod, enquiry=e)


def check_contact_email(id):
    to_send = ContactEmails.objects.filter(user=id)
    up = User.objects.get(id=id).userprofile
    now_utc = datetime.now(pytz.utc)
    now = datetime.now()
    subject = '[CoreLogs] {0} Invited You to Check it Out'.format(up)
    if len(to_send) < 200:
        for s in to_send:
            mail_body = join_corelogs_mail.format(s.first_name, up)
            MailSend.objects.create(email=s.email, body=mail_body, reasons='jcm', from_email='4',
                                    date=now_utc + timedelta(minutes=2), subject=subject)
    else:
        """Yield successive n-sized chunks from to_send."""
        for i in range(0, len(to_send), 100):
            to_send_n = to_send[i:i+100]
            for s in to_send_n:
                mail_body = render_to_string('emails/join_corelogs_mail.html').format(s.first_name, up)
                MailSend.objects.create(email=s.email, body=mail_body, reasons='jcm', from_email='4',
                                        date=now_utc + timedelta(days=i/100), subject=subject)


def fuck_shit(request):
    up = User.objects.get(id=1).userprofile
    wp = up.primary_workplace
    now = datetime.now()
    now_utc = datetime.now(pytz.utc)
    result = render_to_string('emails/product_intro_mail.html').format(up, wp, wp.slug)
    subject = '[CoreLogs] Important! You Got an Inquiry'
    MailSend.objects.create(user=up.user, body=result, reasons='wim',
                            date=now_utc + timedelta(days=2), email=up.get_email0(), subject=subject)
    return render(request, 'search/random_text_print.html', locals())


# from background_task.models import Task
#
#
# def reschedule():
#     t = Task.objects.all()
#     now = datetime.now(pytz.utc)
#     c = 0
#     for i in t:
#         if len(t.task_params)> 10:
#             if i.task_params[-8] is '4':
#                 t.run_at = now + timedelta(minutes=c)
#                 t.save()
#                 c = c+1
