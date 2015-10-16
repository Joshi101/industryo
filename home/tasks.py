from background_task import background
from django.contrib.auth.models import User
from django.core.mail import send_mail
from activities.models import Notification

from django.core.mail import EmailMultiAlternatives

@background(schedule=60)
def bhakk(id, n):
    user = User.objects.get(id=id)
    if user.email:
        user_email = user.email
    else:
        user_email = 'rohit9gag@gmail.com'
    if user.first_name:
        name = user.get_full_name()
    else:
        name = user.username
    if n == 15:
        template = Template15
        html_content = template.format(name)
    subject, from_email, to = 'CoreLogs The platform for teams', 'sp@corelogs.com', user_email
    text_content = 'This is an important message.'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    # try:
    #     send_mail('CoreLogs- background test', content, 'site.corelogs@gmail.com', ['sprksh.j@gmail.com'])
    # except Exception:
    #     pass

@background(schedule=60)
def luck(id, n):
    user = User.objects.get(id=id)
    if user.email:
        user_email = user.email
    else:
        user_email = 'rohit9gag@gmail.com'
    if user.first_name:
        name = user.get_full_name()
    else:
        name = user.username
    workplace = user.userprofile.primary_workplace
    url = 'www.corelogs.com/workplace/'+workplace.slug

    template = Template16
    content = template.format(name, workplace, url)
    send_mail('Baja/ Supra Teams Feedbacks', content, 'sp@corelogs.com', [user_email])


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

<div style="margin:0;padding:0;min-width:100%;background-color:#fff">

    <center style="display:table;table-layout:fixed;width:100%;min-width:620px;background-color:#fff">
      <table style="border-collapse:collapse;border-spacing:0;font-size:1px;line-height:1px;width:100%;height:54px"><tbody><tr><td style="padding:0;vertical-align:top">&nbsp;</td></tr></tbody></table>


          <table style="border-collapse:collapse;border-spacing:0;Margin-left:auto;Margin-right:auto;width:600px;table-layout:fixed">
            <tbody><tr>
              <td style="padding:0;vertical-align:top;text-align:left">
                <div><div style="font-size:20px;line-height:20px">&nbsp;</div></div>
                  <table style="border-collapse:collapse;border-spacing:0;table-layout:fixed;width:100%">
                    <tbody><tr>
                      <td style="padding:0;vertical-align:top;padding-left:20px;padding-right:20px;word-break:break-word;word-wrap:break-word">

            <h1 style="font-style:normal;font-weight:400;Margin-bottom:24px;Margin-top:0;font-size:32px;line-height:40px;font-family:&quot;Open Sans&quot;,sans-serif;color:#404040;text-align:center">Why are you alone when you too have a team?</h1>

                      </td>
                    </tr>
                  </tbody></table>

                  <table style="border-collapse:collapse;border-spacing:0;table-layout:fixed;width:100%">
                    <tbody><tr>
                      <td style="padding:0;vertical-align:top;padding-left:20px;padding-right:20px;word-break:break-word;word-wrap:break-word">

            <div style="font-size:12px;font-style:normal;font-weight:400;Margin-bottom:27px;Margin-top:0;font-family:&quot;Open Sans&quot;,sans-serif;color:#8f8f8f" align="center">
              <a style="text-decoration:underline;color:#e45d6b" href="http://industrylogger.cmail20.com/t/i-i-ttlhsk-l-r/" target="_blank"><img style="border:0;display:block;max-width:400px" src="https://ci3.googleusercontent.com/proxy/SkT2gspldP2HuLQZt6fSJttXIiPBEUfBfiReLOS_3hXCvXgHYcrEGMLx4_yR4Yrh8QR3F-TeRiXELXhUBxTrcrQBUGVA44Uq34Fq32b9hp3pukA2NJXrERRxEpYRbeb3pMA=s0-d-e1-ft#http://i1.cmail20.com/ei/i/8D/923/04E/062312/csfinal/chessoneagainstmany.jpg" alt="CoreLogs" width="400" height="260" class="CToWUd"></a>
            </div>

                      </td>
                    </tr>
                  </tbody></table>

                  <table style="border-collapse:collapse;border-spacing:0;table-layout:fixed;width:100%">
                    <tbody><tr>
                      <td style="padding:0;vertical-align:top;padding-left:20px;padding-right:20px;word-break:break-word;word-wrap:break-word">

            <h2 style="font-style:normal;font-weight:700;Margin-bottom:0;Margin-top:0;font-size:22px;line-height:30px;font-family:Cabin,Avenir,sans-serif;color:#706f70;text-align:left">We <strong style="font-weight:bold">Invite</strong>
you to Invite your TeamMates to&nbsp;<a style="text-decoration:none;color:#e45d6b" href="http://industrylogger.cmail20.com/t/i-i-ttlhsk-l-y/" target="_blank">CoreLogs</a></h2><p style="font-style:normal;font-weight:400;Margin-bottom:27px;Margin-top:16px;font-size:17px;line-height:25px;font-family:&quot;Open Sans&quot;,sans-serif;color:#8f8f8f;text-align:left">CoreLogs is a platform for teams to ask and answer technical and event related questions. Make your mark on the internet by asking and answering. A good question and a good answer are timeless and stay forever on internet and serve as a reference to many depending upon the quality. Forward the mail to your teammates.</p>

                      </td>
                    </tr>
                  </tbody></table>

                  <table style="border-collapse:collapse;border-spacing:0;table-layout:fixed;width:100%">
                    <tbody><tr>
                      <td style="padding:0;vertical-align:top;padding-left:20px;padding-right:20px;word-break:break-word;word-wrap:break-word">

            <div style="Margin-bottom:0;Margin-top:0;text-align:center">
              <u></u><a style="border-radius:3px;display:inline-block;font-size:14px;font-weight:700;line-height:24px;padding:13px 35px 12px 35px;text-align:center;text-decoration:none!important;color:#fefefe;font-family:&quot;Open Sans&quot;,sans-serif;background-color:#e45d6b" href="http://industrylogger.cmail20.com/t/i-i-ttlhsk-l-j/" target="_blank">Visit CoreLogs</a><u></u>
            </div>

                      </td>
                    </tr>
                  </tbody></table>

                <div style="font-size:20px;line-height:20px">&nbsp;</div>
              </td>
            </tr>
          </tbody></table>

      <table style="border-collapse:collapse;border-spacing:0;Margin-left:auto;Margin-right:auto;width:560px;color:#bdb9bd">
        <tbody><tr>
          <td style="padding:0;vertical-align:top" align="center">
            <div style="font-size:11px;line-height:17px;font-weight:400;letter-spacing:0.01em;Margin-bottom:17px">&nbsp;</div>
            <center style="Margin-bottom:10px;Margin-top:0;font-size:4px;line-height:4px">
              <table style="border-collapse:collapse;border-spacing:0;Margin-bottom:27px;Margin-left:auto;Margin-right:auto">
                <tbody><tr>
                  <td style="padding:0;vertical-align:top"><span style="border-radius:2px;display:inline-block;font-size:4px;min-height:4px;line-height:4px;width:4px;background-color:#ccc">&nbsp;</span></td>
                  <td style="padding:0;vertical-align:top;font-size:1px;line-height:1px;width:8px">&nbsp;</td>
                  <td style="padding:0;vertical-align:top"><span style="border-radius:2px;display:inline-block;font-size:4px;min-height:4px;line-height:4px;width:4px;background-color:#ccc">&nbsp;</span></td>
                  <td style="padding:0;vertical-align:top;font-size:1px;line-height:1px;width:8px">&nbsp;</td>
                  <td style="padding:0;vertical-align:top"><span style="border-radius:2px;display:inline-block;font-size:4px;min-height:4px;line-height:4px;width:4px;background-color:#ccc">&nbsp;</span></td>
                </tr>
              </tbody></table>
            </center>

            <div style="font-family:Cabin,Avenir,sans-serif;font-size:11px;font-weight:400;letter-spacing:0.01em;line-height:17px;Margin-bottom:17px">
              <div style="font-size:11px;font-weight:400;letter-spacing:0.01em;line-height:17px;Margin-bottom:17px">You are receiving this email because you have registered on <a href="http://www.corelogs.com" target="_blank">www.corelogs.com</a></div>
            </div>
            <div style="font-family:Cabin,Avenir,sans-serif;font-size:11px;font-weight:400;letter-spacing:0.01em;line-height:17px;Margin-bottom:17px">
              <span>No Images? <a style="text-decoration:none;color:#bdb9bd;font-weight:700;letter-spacing:0.03em" href="http://industrylogger.cmail20.com/t/i-e-ttlhsk-l-d/" target="_blank">Click here</a></span>


              <span>&nbsp;&nbsp;·&nbsp;&nbsp;</span>
                <a style="text-decoration:none;color:#bdb9bd;font-weight:700;letter-spacing:0.03em" href="http://industrylogger.cmail20.com/t/i-u-ttlhsk-l-h/" target="_blank">Unsubscribe</a>
            </div>
            <div style="font-family:Cabin,Avenir,sans-serif;font-size:11px;font-weight:400;letter-spacing:0.01em;line-height:17px;Margin-bottom:17px">CoreLogs - The Platform for entire core segment of engineering</div>

          </td>
        </tr>
      </tbody></table>
      <table style="border-collapse:collapse;border-spacing:0;font-size:1px;line-height:1px;width:100%;height:54px"><tbody><tr><td style="padding:0;vertical-align:top">&nbsp;</td></tr></tbody></table>
    </center>
  <img style="border:0!important;display:block!important;min-height:1px!important;width:1px!important;margin:0!important;padding:0!important" src="https://ci3.googleusercontent.com/proxy/w_qniVtCSM2hSzmAd0hJL2PAhm0KjcqIuo0uAHvONoQZS3fUQOfzf-oihT7OgZm3rM3pb6Vaz5aWoQJNQUVmBEX5J_D4Nt60I6bsy5I=s0-d-e1-ft#https://industrylogger.cmail20.com/t/i-o-ttlhsk-l/o.gif" width="1" height="1" border="0" alt="" class="CToWUd"><div class="yj6qo"></div><div class="adL">
</div></div>
'''

Template16 = u'''Hi {0}

You have registered on CoreLogs as a member of {1} which participates in Baja/Supra events.
I would like to have your genuine feedback about our website www.corelogs.com.

1. How do you like www.corelogs.com as a platform for SAE teams and the entire core segment of engineering?
2. Did you find the Forum section helpful and did you find it upto the mark?
3. Would you like to use the profile page {2} of your team as a substitute for your website?

How do you think we should expand so as to cover all the teams and become more valuable to the people of the teams. Please reply to me directly.
Also, invite your teammates to the website so that we may together create a great community.

Thanks
Surya Prakash
Founder
CoreLogs
'''