from background_task import background
from django.contrib.auth.models import User
from activities.models import Notification
from django.core.mail import EmailMultiAlternatives
from home.templates import *
from contacts.views import check_no_wp, get_google_contacts_i, check_no_inquiry, check_contact_email
from datetime import timedelta
from django.core.mail import get_connection, send_mail
from passwords.passwords import *
from leads.views import close_lead1
import ast


@background(schedule=40)
def execute_view(view, id):
    if view == 'check_no_wp':
        check_no_wp(id)
    elif view == 'check_no_inquiry':
        check_no_inquiry(id)
    elif view == 'check_contact_email':
        check_contact_email(id)
    elif view == 'close_lead':
        close_lead1(id)


# @background(schedule=60)
# def send_mail_contacts(email, body, subject, from_email):
#     subject = subject
#     user_email = email
#     html_content = body
#     # if from_email == 'A':
#     from_email, to = 'sp@corelogs.com', user_email
#     text_content = 'CoreLogs Invites teams to rent Components and safety equipment'
#     msg = EmailMultiAlternatives(subject, text_content, from_email, [user_email])
#     msg.attach_alternative(html_content, "text/html")
#     msg.send()


@background(schedule=60)
def send_mail_contacts(**kwargs):
    subject = kwargs['subject']
    to = kwargs['email']
    if '[' in to:
        to = ast.literal_eval(to)
    else:
        to = [to]
    html_content = kwargs['body']
    text_content = kwargs.get('text')
    if not text_content:
        text_content = 'CoreLogs Invites teams to rent Components and safety equipment'
    my_host = 'email-smtp.us-west-2.amazonaws.com'
    my_port = 587
    my_username = sp_username
    my_password = sp_password

    # my_host = 'smtp.gmail.com'
    # my_port = 587
    # my_username = 'rohit9gag@gmail.com'
    # my_password = 'SP@nitj.09'

    from_email = 'sp@corelogs.com'
    my_use_tls = True
    connection = get_connection(host=my_host,
                                port=my_port,
                                username=my_username,
                                password=my_password,
                                use_tls=my_use_tls)
    connection.open()
    msg = EmailMultiAlternatives(subject, text_content, from_email, to, connection=connection)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    connection.close()


@background(schedule=60*4)
def get_contacts(id):
    user = User.objects.get(id=id)
    provider = user.userprofile.get_provider()
    if provider == 'google':
        get_google_contacts_i(user)
        execute_view('check_contact_email', id, schedule=timedelta(minutes=20))

    else:
        pass

@background(schedule=2)
def send_html_mail_post(id, n, subject, arguments):
    u = User.objects.get(id=id)
    user_email = u.email
    up = u.userprofile
    a = eval(arguments)
    template = n
    subject = subject
    html_content = template.format(*a)

    from_email, to = 'sp@corelogs.com', user_email
    text_content = 'CoreLogs Invites teams to rent Components and safety equipment'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [user_email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

@background(schedule=60)
def send_html_mail(id, n):
    u = User.objects.get(id=id)
    user_email = u.email
    up = u.userprofile

    if n == 22:
        template = n
        subject = "[CoreLogs] - How we are planning to revolutionize the world of Teams & Engineers."
        html_content = template.format(up)
    elif n == 33:
        template = Template_Team_all
        subject = "CoreLogs partnering up with Mega ATV Championship for the Event"
        html_content = template.format(up, up.primary_workplace.slug, up.primary_workplace)

    elif n == 50:       # message
        template = Temp_message
        subject = "[CoreLogs] You have received a new Message"
        html_content = template.format(up)

    elif n == 52:       # message
        template = Temp_set_wp
        subject = "Tell us the name of your company"
        html_content = template.format(up)

    elif n == 44:       # message
        template = Template_SME_all
        subject = "[CoreLogs] Lets Grow Together"
        html_content = template.format(up, up.primary_workplace.slug, up.primary_workplace)

    elif n == 88:
        pass
        # if u.userprofile.primary_workplace.workplace_type == 'A':
        #     # template = render_to_string('emails/set_wp_now.txt', {'0': up})
        # elif u.userprofile.primary_workplace.workplace_type == 'B':
        #     template = Temp_post_set_b
        # elif u.userprofile.primary_workplace.workplace_type == 'C':
        #     template = Temp_post_set_c
        # else:       # u.userprofile.primary_workplace.workplace_type == 'O':
        #     # template = get_te
        #     template = Temp_post_set_o
        # subject = "[CoreLogs] Your Workplace Profile"
        # html_content = template.format(up, up.primary_workplace, up.primary_workplace.slug)
    else:
        template = Template_Team_all
        subject = "[CoreLogs] - How we are planning to revolutionize the world of Teams & Engineers."
        # html_content = template.format(up)

    from_email, to = 'sp@corelogs.com', user_email
    text_content = 'CoreLogs Invites teams to rent Components and safety equipment'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()


@background(schedule=60)
def send_list_html_mail(mail, n):

    user_email = [mail]

    subject = "Request to feature your Products on our Marketplace."

    template = Temp_new_in
    html_content = template
    from_email, to = 'sprksh.j@gmail.com', user_email
    text_content = 'CoreLogs Invites you & your company to the best Ecosystem of SMEs on Internet. We invite you to www.corelogs.com'
    msg = EmailMultiAlternatives(subject, text_content, from_email, user_email)
    msg.attach_alternative(html_content, "text/html")
    msg.send()



