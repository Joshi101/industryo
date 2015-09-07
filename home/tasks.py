from background_task import background
from django.contrib.auth.models import User
from django.core.mail import send_mail
from activities.models import Notification


@background(schedule=60)
def notify_user(id, n):
    notifcation = Notification.objects.get(id=id)
    user = notifcation.to_user
    user_email = user.email
    name = user.get_full_name()
    question = notifcation.question
    node = notifcation.node
    answer = notifcation.answer
    ans_q = answer.question
    from_user = notifcation.from_user
    workplace = user.primary_workplace

    if n == 1:
        template = Template1
        content = template.format(name, from_user, node)
    elif n == 2:
        template = Template2
        content = template.format(name, from_user, question)
    elif n == 3:
        template = Template3
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
        content = template.format(name, from_user, ans_q)
    elif n == 8:
        template = Template8
        content = template.format(name, from_user, question)
    elif n == 9:
        template = Template9
        content = template.format(name, from_user, question)
    elif n == 10:
        template = Template10
        content = template.format(name, from_user, ans_q)
    elif n == 11:
        template = Template11
        content = template.format(name, from_user, ans_q)
    elif n == 12:
        template = Template12
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