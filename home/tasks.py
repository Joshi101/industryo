from background_task import background
from django.contrib.auth.models import User
from django.core.mail import send_mail
from activities.models import Notification
from django.core.mail import EmailMultiAlternatives
from .templates import *


@background(schedule=60)
def send_text_mail(id, n):
    u = User.objects.get(id=id)
    user_email = u.email

    subject = ""

    content = Template19.format(u.userprofile)

    send_mail(subject, content, 'sp@corelogs.com', [user_email])

@background(schedule=60)
def send_html_mail(id, n):
    u = User.objects.get(id=id)
    user_email = u.email
    up = u.userprofile
    if n == 25:
        template = Temp_set_wp
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
        if u.userprofile.primary_workplace.workplace_type == 'A':
            template = Temp_post_set_a
        elif u.userprofile.primary_workplace.workplace_type == 'B':
            template = Temp_post_set_b
        elif u.userprofile.primary_workplace.workplace_type == 'C':
            template = Temp_post_set_c
        else:       # u.userprofile.primary_workplace.workplace_type == 'O':
            template = Temp_post_set_o
        subject = "[CoreLogs] Your Workplace Profile"
        html_content = template.format(up, up.primary_workplace, up.primary_workplace.slug)
    else:
        template = Template_Team_all
        subject = "[CoreLogs] - How we are planning to revolutionize the world of Teams & Engineers."
        html_content = template.format(up)

    from_email, to = 'sp@corelogs.com', user_email
    text_content = 'CoreLogs Invites teams to rent Components and safety equipment'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

@background(schedule=60)
def send_list_text_mail(mail, n):
    mail = mail

    subject = "CoreLogs Invites you & your company to the best Ecosystem of SMEs on Internet"

    content = Template_final_sme_invite
    send_mail(subject, content, 'rohit9gag@gmail.com', [mail])

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


@background(schedule=60)
def notify_user(id, n):
    notification = Notification.objects.get(id=id)
    user = notification.to_user
    if user.email:
        user_email = user.email
    else:
        user_email = 'rohit9gag@gmail.com'
    if user.first_name:
        name = user.get_full_name()
    else:
        name = user.username

    question = notification.question
    node = notification.node
    answer = notification.answer

    from_user = notification.from_user

    if n == 1:
        template = Template1
        content = template.format(name, from_user, node)
    elif n == 2:
        template = Template2
        content = template.format(name, from_user, question)
    elif n == 3:
        template = Template3
        ans_q = answer.question
        content = template.format(name, from_user, ans_q)
    elif n == 4:
        template = Template4
        content = template.format(name, from_user, node)
    elif n == 5:
        template = Template5
        content = template.format(name, from_user, node)
    elif n == 6:
        template = Template6
        content = template.format(name, from_user, question)
    elif n == 7:
        template = Template7
        ans_q = answer.question
        content = template.format(name, from_user, ans_q)
    elif n == 8:
        template = Template8
        content = template.format(name, from_user, question)
    elif n == 9:
        template = Template9
        content = template.format(name, from_user, question)
    elif n == 10:
        template = Template10
        ans_q = answer.question
        content = template.format(name, from_user, ans_q)
    elif n == 11:
        template = Template11
        ans_q = answer.question
        content = template.format(name, from_user, ans_q)
    elif n == 12:
        template = Template12
        workplace = user.userprofile.primary_workplace
        content = template.format(name, from_user, workplace)
    elif n == 13:
        template = Template13
        content = template.format(name, from_user, question)
    elif n == 14:
        template = Template14
        content = template.format(name, from_user, question)
    send_mail('CoreLogs- background test', content, 'site.corelogs@gmail.com', ['rohit9gag@gmail.com'])


# liked
Template1 = u'''Hi {0},

{1} likes your feed {2}. Have a look at his/her profile .

CoreLogs - The Engineer's Forum is dependent on your will to share your knowledge. Your Questions get answered only\
 because somebody takes the pain of answering it. Be helpful to the community. Find a question you can answer.

 Visit www.corelogs.com today.

 Admin
 CoreLogs
 (www.corelogs.com)
'''


# q_commented
Template2 = u'''Hi {0},

{1} has commented on your question {2}. Have a look at his/her profile.

CoreLogs - The Engineer's Forum is dependent on your will to share your knowledge. Your Questions get answered only\
 because somebody takes the pain of answering it. Be helpful to the community. Find a question you can answer.

 Visit www.corelogs.com today.

 Admin
 CoreLogs
 (www.corelogs.com)
'''

# a_commented
Template3 = u'''Hi {0},

{1} has commented on your Answer on the question {2}. Have a look at his/her profile.

CoreLogs - The Engineer's Forum is dependent on your will to share your knowledge. Your Questions get answered only\
 because somebody takes the pain of answering it. Be helpful to the community. Find a question you can answer.

 Visit www.corelogs.com today.

 Admin
 CoreLogs
 (www.corelogs.com)
'''


# n_commented
Template4 = u'''Hi {0},

{1} has commented on your feed {2}. Have a look at his/her profile.

CoreLogs - The Engineer's Forum is dependent on your will to share your knowledge. Your Questions get answered only\
 because somebody takes the pain of answering it. Be helpful to the community. Find a question you can answer.

 Visit www.corelogs.com today.

 Admin
 CoreLogs
 (www.corelogs.com)
'''


# also_n_commented
Template5 = u'''Hi {0},

{1} has also commented on the feed {2}. Have a look at his/her profile.

CoreLogs - The Engineer's Forum is dependent on your will to share your knowledge. Your Questions get answered only\
 because somebody takes the pain of answering it. Be helpful to the community. Find a question you can answer.

 Visit www.corelogs.com today.

 Admin
 CoreLogs
 (www.corelogs.com)
'''

# also_q_commented
Template6 = u'''Hi {0},

{1} has also commented on the Question {2}. Have a look at his/her profile.

CoreLogs - The Engineer's Forum is dependent on your will to share your knowledge. Your Questions get answered only\
 because somebody takes the pain of answering it. Be helpful to the community. Find a question you can answer.

 Visit www.corelogs.com today.

 Admin
 CoreLogs
 (www.corelogs.com)
'''

# also_a_commented
Template7 = u'''Hi {0},

{1} has also commented on the Answer on the Question {2}. Have a look at his/her profile.

CoreLogs - The Engineer's Forum is dependent on your will to share your knowledge. Your Questions get answered only\
 because somebody takes the pain of answering it. Be helpful to the community. Find a question you can answer.

 Visit www.corelogs.com today.

 Admin
 CoreLogs
 (www.corelogs.com)
'''

# q_upvoted
Template8 = u'''Hi {0},

{1} has voted up your Question {2}. Have a look at his profile.

CoreLogs - The Engineer's Forum is dependent on your will to share your knowledge. Your Questions get answered only\
 because somebody takes the pain of answering it. Be helpful to the community. Find a question you can answer.

 Visit www.corelogs.com today.

 Admin
 CoreLogs
 (www.corelogs.com)
'''

# q_downvoted
Template9 = u'''Hi {0},

{1} has voted down your Question {2}. Have a look at his profile.

Find out why or edit the question to meet the standards.

CoreLogs - The Engineer's Forum is dependent on your will to share your knowledge. Your Questions get answered only\
 because somebody takes the pain of answering it. Be helpful to the community. Find a question you can answer.

 Visit www.corelogs.com today.

 Admin
 CoreLogs
 (www.corelogs.com)
'''

# a_upvoted
Template10 = u'''Hi {0},

{1} has voted down your Answer on the question {2}. Have a look at his profile.

CoreLogs - The Engineer's Forum is dependent on your will to share your knowledge. Your Questions get answered only\
 because somebody takes the pain of answering it. Be helpful to the community. Keep on answering and helping.

 Visit www.corelogs.com today.

 Admin
 CoreLogs
 (www.corelogs.com)
'''

# a_downvoted
Template11 = u'''Hi {0},

{1} has voted down your Answer on the question {2}. Have a look at his/her profile.

You can Edit your question to make it more useful.

CoreLogs - The Engineer's Forum is dependent on your will to share your knowledge. Your Questions get answered only\
 because somebody takes the pain of answering it. Be helpful to the community. Find a question you can answer.

 Visit www.corelogs.com today.

 Admin
 CoreLogs
 (www.corelogs.com)
'''

# also_joined
Template12 = u'''Hi {0},

{1} has joined your Workplace {2}. Have a look at his/her profile.

CoreLogs - The Engineer's Forum is dependent on your will to share your knowledge. Your Questions get answered only\
 because somebody takes the pain of answering it. Be helpful to the community. Find a question you can answer.

 Visit www.corelogs.com today.

 Admin
 CoreLogs
 (www.corelogs.com)
'''

# answered
Template13 = u'''Hi {0},

{1} has answered your Question {2}. Have a look at his/her profile.

CoreLogs - The Engineer's Forum is dependent on your will to share your knowledge. Your Questions get answered only\
 because somebody takes the pain of answering it. Be helpful to the community. Find a question you can answer.

 Visit www.corelogs.com today.

 Admin
 CoreLogs
 (www.corelogs.com)
'''

# also_answered
Template14 = u'''Hi {0},

{1} has also answered the Question {2}. Have a look at his/her profile.

CoreLogs - The Engineer's Forum is dependent on your will to share your knowledge. Your Questions get answered only\
 because somebody takes the pain of answering it. Be helpful to the community. Find a question you can answer.

 Visit www.corelogs.com today.

 Admin
 CoreLogs
 (www.corelogs.com)
'''

# Regular email for teams
Template15 = u'''Hi {0},


'''

Template16 = u'''Hi {0}


Thanks
Surya Prakash
Founder
CoreLogs
'''

# test_mail
Template17 = u'''
Hi {0},
'''

# list_mail
Template19 = u'''
Hi {0},

Hope you know about the facebook event #CaptureYourTeam being organized by CoreLogs and have participated or planning to participate in it soon.

You can learn about the event at https://www.facebook.com/notes/corelogs/rules-and-regulations-for-online-event/1635293750068276)

Although the prize money we are giving away is not too much as you might know, we want your team to participate in the
event and there are multiple reasons for that:

1. This event is not about money but making the people aware of coreLogs and its philosophy of bringing the concept of
open source and knowledge sharing in the core segment of engineering.

2. We hope that CoreLogs.com becomes a website that you and everybody involved in automotive competitions can rely upon
for solving their technical and other procurement & customization related problems. But to achieve that, first we
together need to create & nourish a community by proactively helping others so that the community may help us when we are in need.

We Would request you to participate in the event and make it a great success. We also want you to visit www.corelogs.com
often, ask and answer questions on the forum.

We have also launched CoreLogs for Engineers and Small & medium scale industries and through CoreLogs, you can connect
to people working there. Also invite your friends, fellow teams, manufacturers you purchase from and in general everybody
related to core segment of engineering.

Any suggestions, reviews, complaints etc are welcome. Please share your views. They help us greatly.

Thanks

Surya Prakash
Founder
CoreLogs
'''



