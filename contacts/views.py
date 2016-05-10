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
from django.template.loader import render_to_string


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
        mail_body = render_to_string('emails/set_wp_mail.html', {'0': up})
        if up.date_joined > now_utc - timedelta(hours=10):
            MailSend.objects.create(user=up.user, body=mail_body, reasons='swp', date=now + timedelta(minutes=1))
        elif up.date_joined > now_utc - timedelta(days=7):
            MailSend.objects.create(user=up.user, body=mail_body, reasons='swp', date=now + timedelta(days=2))
    elif up.workplace_type in ['A', 'B']:
        check_no_products(id)
        wp = up.primary_workplace
        mail_body = render_to_string('emails/wp_intro_mail.html', {'0': up, '1': wp, '2': wp.slug})
        if up.date_joined > now_utc - timedelta(hours=10):
            MailSend.objects.create(user=up.user, body=mail_body, reasons='wim', date=now + timedelta(minutes=2))
        elif up.date_joined > now_utc - timedelta(days=7):
            MailSend.objects.create(user=up.user, body=mail_body, reasons='wim', date=now + timedelta(days=2))

        product_intro_mail = 'Hi {0}, Product intro mail'
        mail_body2 = render_to_string('emails/product_intro_mail.html', {'0': up, '1': wp, '2': wp.slug})
        if up.date_joined > now_utc - timedelta(hours=10):
            MailSend.objects.create(user=up.user, body=mail_body2, reasons='pim', date=now + timedelta(minutes=2))


def check_no_products(id):
    up = User.objects.get(id=id).userprofile
    if up.workplace_type in ['A', 'B']:
        wp = up.primary_workplace
        now = datetime.now()
        now_utc = datetime.now(pytz.utc)
        mail_body = render_to_string('emails/product_intro_mail.html', {'0': up, '1': wp, '2': wp.slug})
        if up.date_joined > now_utc - timedelta(hours=10):
            MailSend.objects.create(user=up.user, body=mail_body, reasons='pim', date=now + timedelta(minutes=2))
            MailSend.objects.create(user=up.user, body=mail_body, reasons='pim', date=now + timedelta(hours=23))
        if wp.get_product_count() == 0:
            mail_body = render_to_string('emails/no_products_yet.html', {'0': up, '1': wp, '2': wp.slug})
            if up.date_joined > now_utc - timedelta(hours=10):
                MailSend.objects.create(user=up.user, body=mail_body, reasons='npy', date=now + timedelta(minutes=5))
            elif up.date_joined > now_utc - timedelta(days=7):
                MailSend.objects.create(user=up.user, body=mail_body, reasons='npy', date=now + timedelta(days=2))
        else:

            mail_body = render_to_string('emails/no_products_yet.html', {'0': up, '1': wp.get_product_count(),
                                                                         '2': wp.slug, '3': wp.get_product_count()})
            if up.date_joined > now_utc - timedelta(hours=10):
                MailSend.objects.create(user=up.user, body=mail_body, reasons='lmp', date=now + timedelta(minutes=5))
            elif up.date_joined > now_utc - timedelta(days=7):
                MailSend.objects.create(user=up.user, body=mail_body, reasons='lmp', date=now + timedelta(days=2))


def check_no_inquiry(id):
    e = Enquiry.objects.get(id=id)
    if e.seen is False:
        now = datetime.now()
        now_utc = datetime.now(pytz.utc)
        if e.product:
            to_up = e.product.user.userprofile
            inquiry_product_mail = 'Hi {0}, You got an Inquiry'
            mail_body = inquiry_product_mail.format(to_up)
            if e.date > now_utc - timedelta(hours=10):
                MailSend.objects.create(user=to_up.user, body=mail_body, reasons='ipm', date=now + timedelta(minutes=2))
            elif e.date > now_utc - timedelta(days=7):
                MailSend.objects.create(user=to_up.user, body=mail_body, reasons='ipm', date=now + timedelta(hours=44))

        else:
            wp = e.workplace
            inquiry_workplace_mail = 'Hi {0}, You got an Inquiry about workplace'
            if wp.get_members_count() < 4:
                members = wp.get_members()
                for up in members:
                    if e.date > now_utc - timedelta(hours=10):
                        mail_body = inquiry_workplace_mail.format(up)
                        MailSend.objects.create(user=up.user, body=mail_body, reasons='iwm', date=now + timedelta(minutes=2))
                    elif e.date > now_utc - timedelta(days=7):
                        mail_body = inquiry_workplace_mail.format(up)
                        MailSend.objects.create(user=up.user, body=mail_body, reasons='iwm', date=now + timedelta(hours=44))
            else:
                members = wp.get_members()[:3]
                for up in members:
                    if e.date > now_utc - timedelta(hours=10):
                        mail_body = inquiry_workplace_mail.format(up)
                        MailSend.objects.create(user=up.user, body=mail_body, reasons='iwm', date=now + timedelta(minutes=2))
                    elif e.date > now_utc - timedelta(days=7):
                        mail_body = inquiry_workplace_mail.format(up)
                        MailSend.objects.create(user=up.user, body=mail_body, reasons='iwm', date=now + timedelta(hours=44))


def check_contact_email(id):
    to_send = ContactEmails.objects.filter(user=id)
    up = User.objects.get(id=id).userprofile
    now_utc = datetime.now(pytz.utc)
    now = datetime.now()
    if len(to_send)<200:
        for s in to_send:
            mail_body = render_to_string('emails/join_corelogs_mail.html', {'0': s.first_name, '1': up})
            MailSend.objects.create(email=s.email, body=mail_body, reasons='jcm', date=now + timedelta(minutes=2))
    else:
        """Yield successive n-sized chunks from to_send."""
        for i in range(0, len(to_send), 100):
            to_send_n = to_send[i:i+100]
            for s in to_send_n:
                mail_body = render_to_string('emails/join_corelogs_mail.html', {'0': s.first_name, '1': up})
                MailSend.objects.create(email=s.email, body=mail_body, reasons='jcm', date=now + timedelta(days=i-1))







