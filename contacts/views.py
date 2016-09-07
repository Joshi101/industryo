from django.shortcuts import render, HttpResponse
from allauth.socialaccount.models import SocialAccount, SocialToken
import urllib.request as urllib2
from xml.etree import ElementTree as etree
from allauth.socialaccount.models import SocialToken
from .models import ContactEmails, MailSend, Emails
from django.contrib.auth.models import User
from datetime import datetime, timedelta, time, date
import pytz
from activities.models import Enquiry
from django.template.loader import render_to_string, get_template
from django.template import Context
from home.templates import *
import random
from workplace.models import Workplace


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
lqm: lead quotation mail
nm: notification mail
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
        pass
        # for s in to_send:
        #     mail_body = join_corelogs_mail.format(s.first_name, up)
            # MailSend.objects.create(email=s.email, body=mail_body, reasons='jcm', from_email='4',
            #                         date=now_utc + timedelta(minutes=2), subject=subject)

    else:
        """Yield successive n-sized chunks from to_send."""
        pass
        # for i in range(0, len(to_send), 100):
        #     to_send_n = to_send[i:i+100]
        #     for s in to_send_n:
        #         mail_body = render_to_string('emails/join_corelogs_mail.html').format(s.first_name, up)
                # MailSend.objects.create(email=s.email, body=mail_body, reasons='jcm', from_email='4',
                #                         date=now_utc + timedelta(days=i/100), subject=subject)


def fuck_shit(request):
    result = []
    start = datetime.now(pytz.utc)
    end = start - timedelta(days=10)
    s = MailSend.objects.filter(date__range=[end, start], reasons='jcm')
    for a in s:
        result.append(a.email)
    return render(request, 'search/random_text_print.html', locals())


# from threading import Thread


def send_timed():
    now_utc = datetime.now(pytz.utc)
    rang = list(range(4, 13))
    if now_utc.hour in rang:
        to_send_all = ContactEmails.objects.filter(sent=False).order_by('-id')[:100]

        # for i in range(0, len(to_send_all), 40):
        #     to_send_n = to_send_all[i:i+40]
        for s in to_send_all:
            minutes = 5
            from_email = [1, 2, 3, 4]
            mail_body = render_to_string('emails/join_corelogs_mail.html').format(s.first_name, s.user.userprofile)
            subject = '{0} from {1} invited you. Are you from an SME'.format(s.user.userprofile, s.get_company)
            MailSend.objects.create(email=s.email, body=mail_body, reasons='jcm', from_email=random.choice(from_email),
                                    date=now_utc + timedelta(minutes=minutes), subject=subject)
            s.sent = True
            s.save()
            minutes += 1
    else:
        pass    # chill
        # to_send_all = ContactEmails.objects.filter(sent=False, reasons='jcm').order_by('-id')[:100]
        # for s in to_send_all:
        #     s.date = s.date + timedelta(hours=2)
        #     s.save()
'''
This is to send emails to google contacts.
'''


def thread_send(to_send_n):
    now_utc = datetime.now(pytz.utc)
    for s in to_send_n:
        minutes = 5
        mail_body = render_to_string('emails/join_corelogs_mail.html').format(s.first_name, s.user.userprofile)
        subject = 'Hey {0}, {1} asked us to invite you. Are U an SME'.format(s.first_name, s.user.userprofile)
        MailSend.objects.create(email=s.email, body=mail_body, reasons='jcm', from_email='4',
                                date=now_utc + timedelta(minutes=minutes), subject=subject)
        minutes += 1


    # make 8 groups of 40 emails each
    # send 1 group mail from each email id and set timer to stop for 3 minutes

# def check_leads_mail(id, x):
#     lead = L


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

def fill_emails():
    users = User.objects.filter(userprofile__isnull=False)
    for user in users:
        if user.userprofile.primary_workplace:
            wp = user.userprofile.primary_workplace
            t = wp.workplace_type
        else:
            wp = None
            t = 'N'
        if user.email:
            try:
                e = Emails.objects.get(email=user.email)
                pass
            except Exception:
                e = Emails.objects.create(email=user.email, user=user, workplace=wp, workplace_type=t)
        if user.userprofile.email:
            try:
                elsa = Emails.objects.get(email=user.userprofile.email)
                pass
            except Exception:
                elsa = Emails.objects.create(email=user.userprofile.email, user=user, workplace=wp,
                                             workplace_type=t)
        if user.userprofile.product_email:
            try:
                els = Emails.objects.get(email=user.userprofile.product_email)
                pass
            except Exception:
                els = Emails.objects.create(email=user.userprofile.product_email, user=user, workplace=wp,
                                            workplace_type=t)

        if wp:
            if wp.office_mail_id:
                email1 = wp.office_mail_id.split(',')
                print(email1)
                for em in email1:
                    try:
                        e = Emails.objects.get(email=em)
                        pass
                    except Exception:
                        eo = Emails.objects.create(email=em, workplace=wp, workplace_type=t)

    wps = Workplace.objects.filter(userprofile__isnull=True)
    for w in wps:
        print(w.id)
        if w.office_mail_id:
            email1 = w.office_mail_id.split(',')
            for em in email1:
                # if not em in
                try:
                    e = Emails.objects.get(email=em)
                    pass
                except Exception:
                    e = Emails.objects.create(email=em, workplace=w, workplace_type=w.workplace_type)


def fill_emails_daily():
    now = datetime.now()
    users = User.objects.filter(userprofile__isnull=False, date_joined__range=[now-timedelta(days=1), now])
    for user in users:
        if user.userprofile.primary_workplace:
            wp = user.userprofile.primary_workplace
            t = wp.workplace_type
        else:
            wp = None
            t = 'N'
        if user.email:
            try:
                e = Emails.objects.get(email=user.email)
                pass
            except Exception:
                e = Emails.objects.create(email=user.email, user=user, workplace=wp, workplace_type=t)
        if user.userprofile.email:
            try:
                elsa = Emails.objects.get(email=user.userprofile.email)
                pass
            except Exception:
                elsa = Emails.objects.create(email=user.userprofile.email, user=user, workplace=wp,
                                             workplace_type=t)
        if user.userprofile.product_email:
            try:
                els = Emails.objects.get(email=user.userprofile.product_email)
                pass
            except Exception:
                els = Emails.objects.create(email=user.userprofile.product_email, user=user, workplace=wp,
                                            workplace_type=t)

        if wp:
            if wp.office_mail_id:
                email1 = wp.office_mail_id.split(',')
                # print(email1)
                for em in email1:
                    try:
                        e = Emails.objects.get(email=em)
                        pass
                    except Exception:
                        eo = Emails.objects.create(email=em, workplace=wp, workplace_type=t)

    wps = Workplace.objects.filter(userprofile__isnull=True, date__range=[now-timedelta(days=1), now])
    for w in wps:
        print(w.id)
        if w.office_mail_id:
            email1 = w.office_mail_id.split(',')
            for em in email1:
                # if not em in
                try:
                    e = Emails.objects.get(email=em)
                    pass
                except Exception:
                    e = Emails.objects.create(email=em, workplace=w, workplace_type=w.workplace_type)


def wp_email(wp):
    if wp.office_mail_id:
        email1 = wp.office_mail_id.split(',')
        for em in email1:
            # if not em in
            try:
                e = Emails.objects.get(email=em)
                pass
            except Exception:
                e = Emails.objects.create(email=em, workplace=wp, workplace_type=wp.workplace_type)


def up_email(up):
    if up.primary_workplace:
        wp = up.primary_workplace
        t = wp.workplace_type
    else:
        wp = None
        t = 'N'
    if up.email:
        try:
            elsa = Emails.objects.get(email=up.email)
            pass
        except Exception:
            elsa = Emails.objects.create(email=up.email, user=up.user, workplace=wp, workplace_type=t)


def un_subscribe(request):
    email = request.GET.get('email')
    c = Emails.objects.get(email=email)
    c.unsubscribed = 1
    c.save()
    return HttpResponse()

# def send_weekly_overview():
