from django.shortcuts import render, redirect, render_to_response, RequestContext
from nodes.models import Node
from forum.models import Question
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from workplace.models import Workplace
from home import tasks
from datetime import datetime, timedelta, time, date
from .templates import *
from contacts.models import MailSend
from datetime import datetime
import pytz
from passwords.passwords import *
from django.core.mail import EmailMultiAlternatives, get_connection
import time, random


# @login_required
def send_all_sme():
    # now = datetime.now()
    wps = Workplace.objects.filter(workplace_type__in=['A', 'B'])  #.exclude(id=1)
    from_s = ['dashboard@corelogs.com', 'sme@corelogs.com', 'network@corelogs.com', 'arvind@corelogs.com',
              'sp@corelogs.com', 'info@corelogs.com', 'marketing@corelogs.com', 'admin@corelogs.com']

    dic = {'dashboard@corelogs.com': dashboard, 'sme@corelogs.com': smes, 'network@corelogs.com': network,
           'arvind@corelogs.com': arvind, 'sp@corelogs.com': sp, 'info@corelogs.com': info,
           'marketing@corelogs.com': mark, 'admin@corelogs.com': admin}
    while True:

        for i in from_s:
            print(i)
            my_username = i
            my_password = dic[i]
            my_host = 'smtp.zoho.com'
            my_port = 587
            my_use_tls = True
            connection = get_connection(host=my_host,
                                        port=my_port,
                                        username=my_username,
                                        password=my_password,
                                        use_tls=my_use_tls)

            print(len(wps))
            aa = wps[:10]
            wps = wps[10:]
            print(len(wps))
            # print()
            try:
                print('done upto before '+str(aa[0])+' id '+str(aa[0].id))
            except Exception:
                print('done upto before '+str(aa[0].id))
            emails = []
            for wp in aa:
                if len(wp.get_members()) < 7:
                    members = wp.get_members()
                    for mem in members:
                        e = mem.get_best_email()
                        # print(e)
                        emails.append(e)
                        if wp.office_mail_id:
                            a = wp.office_mail_id
                            b = a.split(',')
                            emails.extend(b)
                            emails = list(set(emails))
                    # print(emails)

                else:
                    emails = emails
                    print('wtf')
            print(emails)
            if emails:
                subject = 'Overview of CoreLogs & Benefits to SMEs'
                html_content = Template_SME_all
                try:
                    connection.open()
                    from_email = my_username

                    text_content = '''Hi,

Greetings from CoreLogs. You have registered your company on CoreLogs. Let me give you a quick overview of CoreLogs and what benefits SMEs can get from it.

CoreLogs is a business enabling platform for SMEs which brings the buyers and sellers/manufacturers and service providers on the same platform along with their products and requirements and boosts business through free interactions via inquiries, leads, quotations and direct messages.

It has 3 basic components:

1. Uniform identity to all SMEs on Internet: CoreLogs gives free and uniform company profile to all SMEs big or small across segments. The company profile will serve as SMEs' identity on internet the way facebook/ linkedin profile is for individuals. We have thousands of SMEs registered and we are expanding fast with an aim to bring all SMEs on one platform.
2. The Business Oriented Network: Bringing all SMEs on one Platform and letting them interact for all business purposes via leads, inquiries, messages and quotations we have created a network of SMEs. Here we bring you together with SMEs of your segment, your city/ Industrial areas and companies of your concern. Companies can always share updates with the entire network at one place.
3. Basic CRM tools & Analytics: On CoreLogs, you list all products/ services and Requirements and get inquiries, quotations and messages from SMEs directly. You can easily manage all of these at one place and thus we help you in getting new customers as well as a basic customer relationship management services. And on company dashboard, we bring you basic analytics data about your company.

Combining all these, we are becoming a one stop platform for small, medium and large businesses. And we are working very hard to create an open platform for SMEs and it is incomplete without you people. Also, to expand the network fast, we ask you to invite more SMEs to CoreLogs. Sooner or later every business is going to be on CoreLogs. More SMEs from your network on CoreLogs brings yo in center and helps you get more business.

If you registered on CoreLogs more than 20 days ago, you need to visit it again and update your profile. We have added features and made the flow easier. And yes the platform is getting bigger everyday.

Any Queries? Mail us at sp@corelogs.com or reply to this email.

Thanks
Surya Prakash
Founder, CoreLogs
                    '''
                    msg = EmailMultiAlternatives(subject, text_content, from_email, emails, connection=connection)
                    msg.attach_alternative(html_content, "text/html")
                    # msg.send()
                    try:
                        msg.send()
                    except Exception:
                        print(emails)
                except Exception:
                    print(emails)
                print('waiting for a while')
                time.sleep(120)
            else:
                print('emails hi nahi tha')
                time.sleep(5)
        print('One Loop COmpleted')
        time.sleep(600)





@login_required
def send(request):
    if 'q' in request.GET:
        s = request.GET.get('q')
        if s == 'set_wp':
            id = request.GET.get('id')
            tasks.send_html_mail(id, n=52)
        elif s == 'set_wp_all':
            todaydate = date.today()
            startdate = todaydate + timedelta(days=1)
            enddate = startdate - timedelta(days=30)
            lis = User.objects.filter(date_joined__range=[enddate, startdate], userprofile__primary_workplace=None)
            for i in lis:
                tasks.send_html_mail(i.id, n=52)

    return redirect("/internal/details/?q=u")


@login_required
def send_html(request):
    users = User.objects.filter(userprofile__workplace_type='B')
    now_utc = datetime.now()
    seconds = 40
    template = all_sme_template
    subject = '[CoreLogs] Important notification. See Company DashBoard'
    for user in users:
        up = user.userprofile
        wp = up.primary_workplace
        html_content = template.format(up, wp, wp.slug)
        MailSend.objects.create(user=user, email=user.email, body=html_content, reasons='bulk_m', subject=subject,
                                from_email=random.choice([2, 3, 4]), date=now_utc + timedelta(seconds=seconds))
        seconds += 30


@login_required
def send_mail(request):
    if request.method == 'POST':
        users = []
        users1 = []
        now_utc = datetime.now(pytz.UTC)
        s = request.POST.get('q')
        subject = request.POST.get('subject')

        arguments = request.POST.get('arguments')       # Send tuple like (up, up.primary_workplace)
        bod = request.POST.get('mail')
        body = bod.replace("?:", "{").replace(":?", "}")

        if s == "meh":
            users = User.objects.filter(id__in=[1])

        elif s == 'set_wp_all':
            todaydate = date.today()
            startdate = todaydate + timedelta(days=1)
            enddate = startdate - timedelta(days=40)
            users = User.objects.filter(date_joined__range=[enddate, startdate], userprofile__primary_workplace=None)

        elif s == "alh":
            users = User.objects.all()

        elif s == "ah":
            users = User.objects.filter(userprofile__primary_workplace__workplace_type='A')

        elif s == "bh":
            users = User.objects.filter(userprofile__primary_workplace__workplace_type='B')

        elif s == "ch":
            users = User.objects.filter(userprofile__primary_workplace__workplace_type='C')

        elif s == "oh":
            users = User.objects.filter(userprofile__primary_workplace__workplace_type='O')

        elif s == "nh":
            users = User.objects.filter(userprofile__primary_workplace=None)

        elif s == "ranh":
            questions = Question.objects.filter(answered=False)
            for q in questions:
                tasks.send_html_mail_post(q.user.id, n=Template_answer_your_own_question.format(q.user.userprofile,
                                                                                                q.slug, q.title))

        elif s[:13] == 'mail_wp_users':
            y = s.split('&')[1]
            w = Workplace.objects.get(id=str(y))
            userps = w.get_members()
            users1 = []
            if userps:
                for u in userps:
                    users1.append(u.user)
            else:
                pass
                # wp_mail = w.office_mail_id
                # wp = Workplace.objects.get()
                # a = eval(arguments)
                # html_content = body.format(*a)
                # MailSend.objects.create(email=wp_mail, body=html_content, reasons='dm', subject=subject,
                #                         from_email=random.choice([2, 3, 4]), date=now_utc)

        elif s == "lh":
            # pi = []
            for u in list_new:
                tasks.send_list_html_mail(u, n=22)
            #     if len(pi) < 3:
            #         pi.append(u)
            #     elif len(pi) == 3:
            #         pi.append(u)
            #         tasks.send_list_html_mail(pi, n=22)
            #         pi = []
            # tasks.send_list_html_mail(pi, n=22)
        minutes = 1
        if users:
            for user in users:
                up = user.userprofile
                a = eval(arguments)
                template = body
                html_content = template.format(*a)

                MailSend.objects.create(user=user, email=user.email, body=html_content, reasons='bm', subject=subject,
                                        from_email=random.choice([2, 3, 4]), date=now_utc + timedelta(minutes=minutes))
                minutes += 1
        if users1:
            for user in users1:
                up = user.userprofile
                a = eval(arguments)
                template = body
                html_content = template.format(*a)

                MailSend.objects.create(user=user, email=user.email, body=html_content, reasons='dm', subject=subject,
                                        from_email=random.choice([2, 3, 4]), date=now_utc + timedelta(minutes=minutes))
                minutes += 1
    return redirect('/internal/activity')


def send_new_wp(request):
    now_utc = datetime.now(pytz.UTC)
    wps = Workplace.objects.filter(date__range=[now_utc-timedelta(days=5), timedelta(days=3)])

    minutes = 1
    for w in wps:
        ms = w.get_members()
        for m in ms:
            subject = u''''Your Company {0} is Registered'''.format(w)
            html_content = new_sme_tem.format(m, w, w.slug)
            MailSend.objects.create(user=m.user, email=m.user.email, body=html_content, reasons='bm', subject=subject,
                                    from_email=random.choice([2, 3, 4]), date=now_utc + timedelta(minutes=minutes))
            minutes += 1

list_new = []