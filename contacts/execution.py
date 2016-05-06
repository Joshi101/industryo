from .models import MailSend
from datetime import datetime, timedelta
from home.tasks import execute_view, send_mail_contacts
from contacts.views import check_no_wp, check_no_products
import pytz

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
    end_time = start_time - timedelta(minutes=15)
    mails = MailSend.objects.filter(date__range=[end_time, start_time], sent=False)
    for mail in mails:

        if mail.reasons in ['pim', 'wim']:
            """This is the segment where the mail is sent directly and no associated task is created
            example are product intro mail, workplace intro mail,
            perhaps review mail
            """
            email = mail.email
            body = mail.body
            subject = mail.subject
            send_mail_contacts(email, body, subject)
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
                send_mail_contacts(email, body, subject)
                execute_view('check_no_wp', mail.user.id, schedule=timedelta(days=2))
                mail.sent = True
                mail.save()
            else:
                check_view(check_no_wp(), mail.user.userprofile)
                # if mail.user.userprofile.workplace_type in ['A', 'B']:
                #     check_view(check_no_products(), mail.user.id)
        elif mail.reasons in ["lmp", 'npy']:
            '''Here, product related mails are handled
            and i think we will be adding check product data completeness or things like that
            Task for checking the same thing after few days is also created
            '''
            email = mail.email
            body = mail.body
            subject = mail.subject
            send_mail_contacts(email, body, subject)
            execute_view('check_no_products', mail.user.id, schedule=timedelta(days=2))
        else:
            # Arrangements for sending enquiry mail over a week
            pass

    # loop_view()


def check_view(func, arg):
    func(arg)


# Create your tests here.
