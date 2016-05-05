from django.shortcuts import render, redirect, render_to_response, RequestContext, HttpResponse
from allauth.socialaccount.models import SocialAccount, SocialToken
import urllib.request as urllib2
from xml.etree import ElementTree as etree
from allauth.socialaccount.models import SocialToken
from .models import ContactEmails, MailSend
from django.contrib.auth.models import User
# from userprofile.models import UserProfile
from datetime import datetime, timedelta, time, date
from workplace.models import Workplace
# from home import tasks


def get_google_contacts(request):
    # social = request.user.social_auth.get(provider='google-oauth2')
    user =request.user

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
            c = ContactEmails.object.create(email=email, provider='google', user=user)

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
            c = ContactEmails.object.create(email=email, provider='google', user=user)

    return locals()

#
# def intro_wp_mail():
#     todaydate = date.today()
#     startdate = todaydate + timedelta(days=1)
#     enddate = startdate - timedelta(days=6)
#     workplace = Workplace.objects.filter(date__range=[enddate, startdate], workplace_type__in=['A', 'B'])
#     for w in workplace:
#         members = w.get_members()
#         for m in members:
#             product_day_1_mail = ''
#             mail_body = product_day_1_mail.format(m,)
#             time = todaydate + timedelta(hours=1)
#             c = MailSend.objects.create(user=m.user, body=mail_body, date=time)


def intro_user_mail():
    todaydate = date.today()
    startdate = todaydate + timedelta(days=1)
    enddate = startdate - timedelta(days=6)
    users = User.objects.filter(date_joined__range=[enddate, startdate], workplace_type__in=['A', 'B'])
    for u in users:
        basic_intro_to_corelogs = ''
        mail_body = basic_intro_to_corelogs.format(u,)
        time = todaydate + timedelta(hours=1)
        # c = MailSend.objects.create(user=m.user, body=mail_body, date=time)


def check_no_wp(id):
    up = User.objects.get(id=id).userprofile
    if up.workplace_type == 'N':
        set_wp_now = 'Hi {0}, no workplace'
        mail_body = set_wp_now.format(up)
        now = datetime.now()
        MailSend.objects.get_or_create(user=up.user, body=mail_body, reasons='swp', date=now + timedelta(minutes=1))

        # MailSend.objects.get_or_create(user=up.user, body=mail_body, reason='reason', date=now + timedelta(days=1))
        # MailSend.objects.get_or_create(user=up.user, body=mail_body, reason='reason', date=now + timedelta(days=3))
        # MailSend.objects.get_or_create(user=up.user, body=mail_body, reason='reason', date=now + timedelta(days=5))
    elif up.workplace_type in ['A', 'B']:
        send_intro_template = 'Hi {0}, workplace_type'
        mail_body = send_intro_template.format()
        now = datetime.now()
        MailSend.objects.get_or_create(user=up.user, body=mail_body, reasons='reason', date=now + timedelta(minutes=2))
        MailSend.objects.get_or_create(user=up.user, body=mail_body, reasons='reason', date=now + timedelta(days=2))
        wp = up.primary_workplace
        now = datetime.now()
        product_intro_mail = 'Hi {0}, Product intro mail'
        mail_body2 = product_intro_mail.format(up)
        MailSend.objects.get_or_create(user=up.user, body=mail_body2, reasons='pim', date=now + timedelta(minutes=2))

# def check_wp_type(up):
#     if up.workplace_type in ['A', 'B']:
#         send_intro_template = 'Hi {0}, workplace_type'
#         mail_body = send_intro_template.format()
#         now = datetime.now()
#         MailSend.objects.get_or_create(user=up.user, body=mail_body, reasons='reason', date=now + timedelta(minutes=2))
#         MailSend.objects.get_or_create(user=up.user, body=mail_body, reasons='reason', date=now + timedelta(days=2))
#         wp = up.primary_workplace
#         now = datetime.now()
#         product_intro_mail = 'Hi {0}, Product intro mail'
#         mail_body2 = product_intro_mail.format(up)
#         MailSend.objects.get_or_create(user=up.user, body=mail_body2, reasons='pim', date=now + timedelta(minutes=2))


def check_no_products(id):
    up = User.objects.get(id=id).userprofile
    wp = up.primary_workplace
    now = datetime.now()
    product_intro_mail = 'Hi {0}, Product intro mail'
    mail_body = product_intro_mail.format(up)
    MailSend.objects.get_or_create(user=up.user, body=mail_body, reasons='pim', date=now + timedelta(minutes=2))
    if wp.get_product_count() == 0:
        list_product_now = 'Hi {0}, no product'
        mail_body = list_product_now.format(up)

        MailSend.objects.get_or_create(user=up.user, body=mail_body, reasons='treason', date=now + timedelta(minutes=5))
    else:
        list_more_products = 'Hi {0}, list more products'
        mail_body = list_more_products.format(up)
        MailSend.objects.get_or_create(user=up.user, body=mail_body, reasons='lmp', date=now + timedelta(minutes=5))





