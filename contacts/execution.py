from .models import MailSend
from datetime import datetime, timedelta
from home.tasks import execute_view, send_mail_contacts
from contacts.views import check_no_wp, check_no_products
import pytz
from .models import ContactEmails
from home.templates import join_corelogs_mail
import random

"""Whats happening is: During creation of user profile, a task is created which checks after 5 minutes whether
    the user has set the workplace or not.
    The task is there in contact.views check_no_wp() That creates a mailsend object with time 2 minutes afterwards
    Then when here check_executables() is run, it checks whether the user has yet set the wp or not
     if not, it sends set wp mail and then creates a task to be executed after a day and the whole process keeps on
     going like that
     Now, once workplace is set here in check_executable,
      first, a check_wp_type is run through check_view(check_wp_type(), mail.user.userprofile)
      after tht, it is checked whether any product has been listed or not
     with check_view(check_no_products(), mail.user.userprofile)

     And yes, all the mails are sent through creating tasks
"""


def check_executable():
    start_time = datetime.now(pytz.utc)
    end_time = start_time - timedelta(minutes=30)
    mails = MailSend.objects.filter(date__range=[end_time, start_time], sent=False)[:4]
    for mail in mails:

        if mail.reasons in ['pim', 'wim']:
            """This is the segment where the mail is sent directly and no associated task is created
            example are product intro mail, workplace intro mail,
            perhaps review mail
            """
            email = mail.email
            body = mail.body
            subject = mail.subject
            send_mail_contacts(email, body, subject, mail.from_email)
            mail.sent = True
            mail.save()
        elif mail.reasons == "swp":
            """This part is for sending workplace related mails
            Here associated tasks are also created pertaining to workplace and also to check products
            """
            if mail.user.userprofile.workplace_type == 'N':
                email = mail.email
                body = mail.body
                subject = mail.subject
                send_mail_contacts(email, body, subject, mail.from_email)
                execute_view('check_no_wp', mail.user.id, schedule=timedelta(days=2))
            else:
                check_no_wp(mail.user.id)
            mail.sent = True
            mail.save()
            '''Here, product related mails are handled
            and i think we will be adding check product data completeness or things like that
            Task for checking the same thing after few days is also created
            '''
            email = mail.email
            body = mail.body
            subject = mail.subject
            send_mail_contacts(email, body, subject, mail.from_email)
            execute_view('check_no_products', mail.user.id, schedule=timedelta(days=2))
            mail.sent = True
            mail.save()
        elif mail.reasons in ['ipm', 'iwm']:
            email = mail.email
            body = mail.body
            subject = mail.subject
            send_mail_contacts(email, body, subject, mail.from_email)
            execute_view('check_no_inquiry', mail.enquiry.id, schedule=timedelta(days=2))
            mail.sent = True
            mail.save()
        elif mail.reasons == 'jcm':
            pass
            # email = mail.email
            # body = mail.body
            # subject = mail.subject
            # send_mail_contacts(email, body, subject, mail.from_email)
            # mail.sent = True
            # mail.save()
        elif mail.reasons == ['bm', 'bulk_m']:
            email = mail.email
            body = mail.body
            subject = mail.subject
            send_mail_contacts(email, body, subject, mail.from_email)
            mail.sent = True
            mail.save()
        elif mail.reasons in ['lqm', 'lcm']:
            if mail.reasons == 'lcm':
                execute_view('close_lead', mail.random_id, schedule=timedelta(days=5))
            email = mail.email
            body = mail.body
            subject = mail.subject
            send_mail_contacts(email, body, subject, mail.from_email)
            mail.sent = True
            mail.save()
    # loop_view()
    # return redirect('/')


def send_marketing():
    pass
    # start_time = datetime.now(pytz.utc)
    # now_utc = datetime.now()
    # to_send = ContactEmails.objects.filter(sent=False, user__userprofile__workplace_type='B')[:4]
    # for s in to_send:
    #     up = s.user.userprofile
    #     subject = '[CoreLogs] {0} Invited You to Check it Out'.format(up)
    #     mail_body = join_corelogs_mail.format(s.first_name, up)
    #     MailSend.objects.create(email=s.email, body=mail_body, reasons='jcm', from_email=random.choice([2, 3, 4]),
    #                             date=now_utc + timedelta(minutes=2), subject=subject)
    #     s.sent = True
    #     s.save()
    # end_time = start_time - timedelta(minutes=30)
    # mails = MailSend.objects.filter(date__range=[end_time, start_time], sent=False, reasons='jcm')[:4]
    # for mail in mails:
    #     if mail.reasons == 'jcm':
    #         email = mail.email
    #         body = mail.body
    #         subject = mail.subject
    #         send_mail_contacts(email, body, subject, mail.from_email)
    #         mail.sent = True
    #         mail.save()


def check_view(func, arg):
    func(arg)


# Create your tests here.
