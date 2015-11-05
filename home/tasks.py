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
    content = template.format(name)
    send_mail('#CaptureYourTeam with CoreLogs & win Cash prizes', content, 'sp@corelogs.com', [user_email])

@background(schedule=60)
def test_mail(id, n):
    u = User.objects.get(id=id)
    user_email = 'sprksh.j@gmail.com'

    template = Template17
    html_content = template.format('Dude')
    subject, from_email, to = '#CaptureYourTeam with CoreLogs & Win Cash Prizes', 'sp@corelogs.com', user_email
    text_content = 'The Platform for Small scale Industries'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

@background(schedule=60)
def list_mail(id, n):

    user_email = id

    template = Template18
    html_content = template.format('Sir / Madam')
    subject, from_email, to = '#CaptureYourTeam with CoreLogs & Win Cash Prizes', 'sp@corelogs.com', user_email
    text_content = '#CaptureYourTeam with CoreLogs & Win Cash Prizes'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
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

<!doctype html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">
	<head>
		<!-- NAME: 1:2:1 COLUMN - BANDED -->
		<!--[if gte mso 15]>
		<xml>
			<o:OfficeDocumentSettings>
			<o:AllowPNG/>
			<o:PixelsPerInch>96</o:PixelsPerInch>
			</o:OfficeDocumentSettings>
		</xml>
		<![endif]-->
		<meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1">
		<title>*|#CaptureYourTeam with CoreLogs & win cash prizes|*</title>

    <style type="text/css">
		p{{
			margin:10px 0;
			padding:0;
		}}
		table{{
			border-collapse:collapse;
		}}
		h1,h2,h3,h4,h5,h6{{
			display:block;
			margin:0;
			padding:0;
		}}
		img,a img{{
			border:0;
			height:auto;
			outline:none;
			text-decoration:none;
		}}
		body,#bodyTable,#bodyCell{{
			height:100%;
			margin:0;
			padding:0;
			width:100%;
		}}
		#outlook a{{
			padding:0;
		}}
		img{{
			-ms-interpolation-mode:bicubic;
		}}
		table{{
			mso-table-lspace:0pt;
			mso-table-rspace:0pt;
		}}
		.ReadMsgBody{{
			width:100%;
		}}
		.ExternalClass{{
			width:100%;
		}}
		p,a,li,td,blockquote{{
			mso-line-height-rule:exactly;
		}}
		a[href^=tel],a[href^=sms]{{
			color:inherit;
			cursor:default;
			text-decoration:none;
		}}
		p,a,li,td,body,table,blockquote{{
			-ms-text-size-adjust:100%;
			-webkit-text-size-adjust:100%;
		}}
		.ExternalClass,.ExternalClass p,.ExternalClass td,.ExternalClass div,.ExternalClass span,.ExternalClass font{{
			line-height:100%;
		}}
		a[x-apple-data-detectors]{{
			color:inherit !important;
			text-decoration:none !important;
			font-size:inherit !important;
			font-family:inherit !important;
			font-weight:inherit !important;
			line-height:inherit !important;
		}}
		.templateContainer{{
			max-width:600px !important;
		}}
		a.mcnButton{{
			display:block;
		}}
		.mcnImage{{
			vertical-align:bottom;
		}}
		.mcnTextContent{{
			word-break:break-word;
		}}
		.mcnTextContent img{{
			height:auto !important;
		}}
		.mcnDividerBlock{{
			table-layout:fixed !important;
		}}
		body,#bodyTable{{
			background-color:#FAFAFA;
		}}
		#bodyCell{{
			border-top:0;
		}}
		h1{{
			color:#202020;
			font-family:Helvetica;
			font-size:26px;
			font-style:normal;
			font-weight:bold;
			line-height:125%;
			letter-spacing:normal;
			text-align:left;
		}}
		h2{{
			color:#202020;
			font-family:Helvetica;
			font-size:22px;
			font-style:normal;
			font-weight:bold;
			line-height:125%;
			letter-spacing:normal;
			text-align:left;
		}}
		h3{{
			color:#202020;
			font-family:Helvetica;
			font-size:20px;
			font-style:normal;
			font-weight:bold;
			line-height:125%;
			letter-spacing:normal;
			text-align:left;
		}}
		h4{{
			color:#202020;
			font-family:Helvetica;
			font-size:18px;
			font-style:normal;
			font-weight:bold;
			line-height:125%;
			letter-spacing:normal;
			text-align:left;
		}}
		#templatePreheader{{
			background-color:#FAFAFA;
			border-top:0;
			border-bottom:0;
			padding-top:9px;
			padding-bottom:9px;
		}}
		#templatePreheader .mcnTextContent,#templatePreheader .mcnTextContent p{{
			color:#656565;
			font-family:Helvetica;
			font-size:12px;
			line-height:150%;
			text-align:left;
		}}
		#templatePreheader .mcnTextContent a,#templatePreheader .mcnTextContent p a{{
			color:#656565;
			font-weight:normal;
			text-decoration:underline;
		}}
		#templateHeader{{
			background-color:#FFFFFF;
			border-top:0;
			border-bottom:0;
			padding-top:9px;
			padding-bottom:0;
		}}
		#templateHeader .mcnTextContent,#templateHeader .mcnTextContent p{{
			color:#202020;
			font-family:Helvetica;
			font-size:16px;
			line-height:150%;
			text-align:left;
		}}
		#templateHeader .mcnTextContent a,#templateHeader .mcnTextContent p a{{
			color:#2BAADF;
			font-weight:normal;
			text-decoration:underline;
		}}
		#templateUpperBody{{
			background-color:#FFFFFF;
			border-top:0;
			border-bottom:0;
			padding-top:0;
			padding-bottom:0;
		}}
		#templateUpperBody .mcnTextContent,#templateUpperBody .mcnTextContent p{{
			color:#202020;
			font-family:Helvetica;
			font-size:16px;
			line-height:150%;
			text-align:left;
		}}
		#templateUpperBody .mcnTextContent a,#templateUpperBody .mcnTextContent p a{{
			color:#2BAADF;
			font-weight:normal;
			text-decoration:underline;
		}}
		#templateColumns{{
			background-color:#FFFFFF;
			border-top:0;
			border-bottom:0;
			padding-top:0;
			padding-bottom:0;
		}}
		#templateColumns .columnContainer .mcnTextContent,#templateColumns .columnContainer .mcnTextContent p{{
			color:#202020;
			font-family:Helvetica;
			font-size:16px;
			line-height:150%;
			text-align:left;
		}}
		#templateColumns .columnContainer .mcnTextContent a,#templateColumns .columnContainer .mcnTextContent p a{{
			color:#2BAADF;
			font-weight:normal;
			text-decoration:underline;
		}}
		#templateLowerBody{{
			background-color:#FFFFFF;
			border-top:0;
			border-bottom:2px solid #EAEAEA;
			padding-top:0;
			padding-bottom:9px;
		}}
		#templateLowerBody .mcnTextContent,#templateLowerBody .mcnTextContent p{{
			color:#202020;
			font-family:Helvetica;
			font-size:16px;
			line-height:150%;
			text-align:left;
		}}
		#templateLowerBody .mcnTextContent a,#templateLowperBody .mcnTextContent p a{{
			color:#2BAADF;
			font-weight:normal;
			text-decoration:underline;
		}}
		#templateFooter{{
			background-color:#FAFAFA;
			border-top:0;
			border-bottom:0;
			padding-top:9px;
			padding-bottom:9px;
		}}
		#templateFooter .mcnTextContent,#templateFooter .mcnTextContent p{{
			color:#656565;
			font-family:Helvetica;
			font-size:12px;
			line-height:150%;
			text-align:center;
		}}
		#templateFooter .mcnTextContent a,#templateFooter .mcnTextContent p a{{
			color:#656565;
			font-weight:normal;
			text-decoration:underline;
		}}
	@media only screen and (min-width:768px){{
		.templateContainer{{
			width:600px !important;
		}}

}}	@media only screen and (max-width: 480px){{
		body,table,td,p,a,li,blockquote{{
			-webkit-text-size-adjust:none !important;
		}}

}}	@media only screen and (max-width: 480px){{
		body{{
			width:100% !important;
			min-width:100% !important;
		}}

}}	@media only screen and (max-width: 480px){{
		#bodyCell{{
			padding-top:10px !important;
		}}

}}	@media only screen and (max-width: 480px){{
		.columnWrapper{{
			max-width:100% !important;
			width:100% !important;
		}}

}}	@media only screen and (max-width: 480px){{
		.mcnImage{{
			width:100% !important;
		}}

}}	@media only screen and (max-width: 480px){{
		.mcnShareContent,.mcnCaptionTopContent,.mcnCaptionBottomContent,.mcnTextContentContainer,.mcnBoxedTextContentContainer,.mcnImageGroupContentContainer,.mcnCaptionLeftTextContentContainer,.mcnCaptionRightTextContentContainer,.mcnCaptionLeftImageContentContainer,.mcnCaptionRightImageContentContainer,.mcnImageCardLeftTextContentContainer,.mcnImageCardRightTextContentContainer{{
			max-width:100% !important;
			width:100% !important;
		}}

}}	@media only screen and (max-width: 480px){{
		.mcnBoxedTextContentContainer{{
			min-width:100% !important;
		}}

}}	@media only screen and (max-width: 480px){{
		.mcnImageGroupContent{{
			padding:9px !important;
		}}

}}	@media only screen and (max-width: 480px){{
		.mcnCaptionLeftContentOuter .mcnTextContent,.mcnCaptionRightContentOuter .mcnTextContent{{
			padding-top:9px !important;
		}}

}}	@media only screen and (max-width: 480px){{
		.mcnImageCardTopImageContent,.mcnCaptionBlockInner .mcnCaptionTopContent:last-child .mcnTextContent{{
			padding-top:18px !important;
		}}

}}	@media only screen and (max-width: 480px){{
		.mcnImageCardBottomImageContent{{
			padding-bottom:9px !important;
		}}

}}	@media only screen and (max-width: 480px){{
		.mcnImageGroupBlockInner{{
			padding-top:0 !important;
			padding-bottom:0 !important;
		}}

}}	@media only screen and (max-width: 480px){{
		.mcnImageGroupBlockOuter{{
			padding-top:9px !important;
			padding-bottom:9px !important;
		}}

}}	@media only screen and (max-width: 480px){{
		.mcnTextContent,.mcnBoxedTextContentColumn{{
			padding-right:18px !important;
			padding-left:18px !important;
		}}

}}	@media only screen and (max-width: 480px){{
		.mcnImageCardLeftImageContent,.mcnImageCardRightImageContent{{
			padding-right:18px !important;
			padding-bottom:0 !important;
			padding-left:18px !important;
		}}

}}	@media only screen and (max-width: 480px){{
		.mcpreview-image-uploader{{
			display:none !important;
			width:100% !important;
		}}

}}	@media only screen and (max-width: 480px){{
		h1{{
			font-size:22px !important;
			line-height:125% !important;
		}}

}}	@media only screen and (max-width: 480px){{
		h2{{
			font-size:20px !important;
			line-height:125% !important;
		}}

}}	@media only screen and (max-width: 480px){{
		h3{{
			font-size:18px !important;
			line-height:125% !important;
		}}

}}	@media only screen and (max-width: 480px){{
		h4{{
			font-size:16px !important;
			line-height:150% !important;
		}}

}}	@media only screen and (max-width: 480px){{
		.mcnBoxedTextContentContainer .mcnTextContent,.mcnBoxedTextContentContainer .mcnTextContent p{{
			font-size:14px !important;
			line-height:150% !important;
		}}

}}	@media only screen and (max-width: 480px){{
		#templatePreheader{{
			display:block !important;
		}}

}}	@media only screen and (max-width: 480px){{
		#templatePreheader .mcnTextContent,#templatePreheader .mcnTextContent p{{
			font-size:14px !important;
			line-height:150% !important;
		}}

}}	@media only screen and (max-width: 480px){{
		#templateHeader .mcnTextContent,#templateHeader .mcnTextContent p{{
			font-size:16px !important;
			line-height:150% !important;
		}}

}}	@media only screen and (max-width: 480px){{
		#templateUpperBody .mcnTextContent,#templateUpperBody .mcnTextContent p{{
			font-size:16px !important;
			line-height:150% !important;
		}}

}}	@media only screen and (max-width: 480px){{
		#templateColumns .columnContainer .mcnTextContent,#templateColumns .columnContainer .mcnTextContent p{{
			font-size:16px !important;
			line-height:150% !important;
		}}

}}	@media only screen and (max-width: 480px){{
		#templateLowerBody .mcnTextContent,#templateLowerBody .mcnTextContent p{{
			font-size:16px !important;
			line-height:150% !important;
		}}

}}	@media only screen and (max-width: 480px){{
		#templateFooter .mcnTextContent,#templateFooter .mcnTextContent p{{
			font-size:14px !important;
			line-height:150% !important;
		}}

}}</style></head>
    <body style="height: 100%;margin: 0;padding: 0;width: 100%;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;background-color: #FAFAFA;">
        <center>
            <table align="center" border="0" cellpadding="0" cellspacing="0" height="100%" width="100%" id="bodyTable" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;height: 100%;margin: 0;padding: 0;width: 100%;background-color: #FAFAFA;">
                <tr>
                    <td align="center" valign="top" id="bodyCell" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;height: 100%;margin: 0;padding: 0;width: 100%;border-top: 0;">
                        <!-- BEGIN TEMPLATE // -->
                        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
                            <tr>
								<td align="center" valign="top" id="templatePreheader" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;background-color: #FAFAFA;border-top: 0;border-bottom: 0;padding-top: 9px;padding-bottom: 9px;">
									<!--[if gte mso 9]>
									<table align="center" border="0" cellspacing="0" cellpadding="0" width="600" style="width:600px;">
									<tr>
									<td align="center" valign="top" width="600" style="width:600px;">
									<![endif]-->
									<table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" class="templateContainer" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;max-width: 600px !important;">
										<tr>
                                			<td valign="top" class="preheaderContainer" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;"><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnTextBlock" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
    <tbody class="mcnTextBlockOuter">
        <tr>
            <td valign="top" class="mcnTextBlockInner" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">

                <table align="left" border="0" cellpadding="0" cellspacing="0" width="366" class="mcnTextContentContainer" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
                    <tbody><tr>

                        <td valign="top" class="mcnTextContent" style="padding-top: 9px;padding-left: 18px;padding-bottom: 9px;padding-right: 0;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;word-break: break-word;color: #656565;font-family: Helvetica;font-size: 12px;line-height: 150%;text-align: left;">

                            #CaptureYourTeam & Win exciting prizes
                        </td>
                    </tr>
                </tbody></table>

                <table align="right" border="0" cellpadding="0" cellspacing="0" width="197" class="mcnTextContentContainer" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
                    <tbody><tr>

                        <td valign="top" class="mcnTextContent" style="padding-top: 9px;padding-right: 18px;padding-bottom: 9px;padding-left: 0;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;word-break: break-word;color: #656565;font-family: Helvetica;font-size: 12px;line-height: 150%;text-align: left;">

                            <a href="http://www.corelogs.com/" target="_blank" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;color: #656565;font-weight: normal;text-decoration: underline;">View this email in your browser</a>
                        </td>
                    </tr>
                </tbody></table>

            </td>
        </tr>
    </tbody>
</table></td>
										</tr>
									</table>
									<!--[if gte mso 9]>
									</td>
									</tr>
									</table>
									<![endif]-->
								</td>
                            </tr>
							<tr>
								<td align="center" valign="top" id="templateHeader" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;background-color: #FFFFFF;border-top: 0;border-bottom: 0;padding-top: 9px;padding-bottom: 0;">
									<!--[if gte mso 9]>
									<table align="center" border="0" cellspacing="0" cellpadding="0" width="600" style="width:600px;">
									<tr>
									<td align="center" valign="top" width="600" style="width:600px;">
									<![endif]-->
									<table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" class="templateContainer" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;max-width: 600px !important;">
										<tr>
                                			<td valign="top" class="headerContainer" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;"><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnCaptionBlock" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
    <tbody class="mcnCaptionBlockOuter">
        <tr>
            <td class="mcnCaptionBlockInner" valign="top" style="padding: 9px;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">




<table border="0" cellpadding="0" cellspacing="0" class="mcnCaptionRightContentOuter" width="100%" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
    <tbody><tr>
        <td valign="top" class="mcnCaptionRightContentInner" style="padding: 0 9px;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
            <table align="left" border="0" cellpadding="0" cellspacing="0" class="mcnCaptionRightImageContentContainer" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
                <tbody><tr>
                    <td class="mcnCaptionRightImageContent" valign="top" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">



                        <img alt="" src="http://www.corelogs.com/images/thumbnails/corelogs_logo.jpg" width="176" style="max-width: 552px;border: 0;height: auto;outline: none;text-decoration: none;-ms-interpolation-mode: bicubic;vertical-align: bottom;" class="mcnImage">



                    </td>
                </tr>
            </tbody></table>
            <table class="mcnCaptionRightTextContentContainer" align="right" border="0" cellpadding="0" cellspacing="0" width="352" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
                <tbody><tr>
                    <td valign="top" class="mcnTextContent" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;word-break: break-word;color: #202020;font-family: Helvetica;font-size: 16px;line-height: 150%;text-align: left;">
                        <span style="font-size:22px">CoreLogs</span>.com is a platform for SAE related collegiate clubs to get connected to each other and the Engineers, experts & Industrialists across the world. Visit <a href="http://www.corelogs.com/forum/" target="_blank" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;color: #2BAADF;font-weight: normal;text-decoration: underline;">The Engineer's Forum</a> to ask & answer Technical questions.
                    </td>
                </tr>
            </tbody></table>
        </td>
    </tr>
</tbody></table>




            </td>
        </tr>
    </tbody>
</table></td>
										</tr>
									</table>
									<!--[if gte mso 9]>
									</td>
									</tr>
									</table>
									<![endif]-->
								</td>
                            </tr>
							<tr>
								<td align="center" valign="top" id="templateUpperBody" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;background-color: #FFFFFF;border-top: 0;border-bottom: 0;padding-top: 0;padding-bottom: 0;">
									<!--[if gte mso 9]>
									<table align="center" border="0" cellspacing="0" cellpadding="0" width="600" style="width:600px;">
									<tr>
									<td align="center" valign="top" width="600" style="width:600px;">
									<![endif]-->
									<table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" class="templateContainer" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;max-width: 600px !important;">
										<tr>
                                			<td valign="top" class="bodyContainer" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;"><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnTextBlock" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
    <tbody class="mcnTextBlockOuter">
        <tr>
            <td valign="top" class="mcnTextBlockInner" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">

                <table align="left" border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnTextContentContainer" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
                    <tbody><tr>

                        <td valign="top" class="mcnTextContent" style="padding-top: 9px;padding-right: 18px;padding-bottom: 9px;padding-left: 18px;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;word-break: break-word;color: #202020;font-family: Helvetica;font-size: 16px;line-height: 150%;text-align: left;">

                            <h1 style="display: block;margin: 0;padding: 0;color: #202020;font-family: Helvetica;font-size: 26px;font-style: normal;font-weight: bold;line-height: 125%;letter-spacing: normal;text-align: left;">Capture Your Team and win exciting prizes</h1>

<p style="margin: 10px 0;padding: 0;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;color: #202020;font-family: Helvetica;font-size: 16px;line-height: 150%;text-align: left;"><span style="font-size:22px; line-height:20.8px">CoreLogs</span><span style="line-height:20.8px">.com brings a facebook event </span><a class="_58cn" data-ft="{{"tn":"*N","type":104}}" href="https://www.facebook.com/hashtag/captureyourteam?source=feed_text&story_id=1635510520046599" style="color: #3B5998;cursor: pointer;text-decoration: none;font-family: helvetica, arial, sans-serif;font-size: 14px;line-height: 19.32px;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;font-weight: normal;"><span aria-label="hashtag" class="_58cl" style="color: #627AAD;">#</span><span class="_58cm">CAPTUREYOURTEAM?</span></a><span style="color: #141823;font-family: helvetica,arial,sans-serif;font-size: 14px;line-height: 19.32px;"> for the SAE related Teams across India. You send us a pic of your car, we upload it from our facebook page. The teams with maximum likes win exciting prizes. Visit our <a href="https://www.facebook.com/corelogs.page" target="_blank" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;color: #2BAADF;font-weight: normal;text-decoration: underline;">facebook page</a> for <a href="https://www.facebook.com/notes/corelogs/rules-and-regulations-for-online-event/1635293750068276" target="_blank" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;color: #2BAADF;font-weight: normal;text-decoration: underline;">details and rules</a>.<br>
You can send us the image at <a href="mailto:info@corelogs.com?subject=Paticipation%20in%20%23captureyourteam" target="_blank" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;color: #2BAADF;font-weight: normal;text-decoration: underline;">info@corelogs.com</a> by 30th November. <strong>The sooner the better.<br>
It is for Baja, Supra/ Formula student India, efficycle, supermileage Teams.</strong></span></p>

                        </td>
                    </tr>
                </tbody></table>

            </td>
        </tr>
    </tbody>
</table></td>
										</tr>
									</table>
									<!--[if gte mso 9]>
									</td>
									</tr>
									</table>
									<![endif]-->
								</td>
                            </tr>
							<tr>
								<td align="center" valign="top" id="templateColumns" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;background-color: #FFFFFF;border-top: 0;border-bottom: 0;padding-top: 0;padding-bottom: 0;">
									<table border="0" cellpadding="0" cellspacing="0" width="100%" class="templateContainer" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;max-width: 600px !important;">
                                        <tr>
                                            <td align="center" valign="top" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
												<!--[if gte mso 9]>
												<table align="center" border="0" cellspacing="0" cellpadding="0" width="600" style="width:600px;">
												<tr>
												<td align="center" valign="top" width="300" style="width:300px;">
												<![endif]-->
												<table align="left" border="0" cellpadding="0" cellspacing="0" width="300" class="columnWrapper" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
													<tr>
														<td valign="top" class="columnContainer" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;"><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnImageCardBlock" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
    <tbody class="mcnImageCardBlockOuter">
        <tr>
            <td class="mcnImageCardBlockInner" valign="top" style="padding-top: 9px;padding-right: 18px;padding-bottom: 9px;padding-left: 18px;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">

<table align="right" border="0" cellpadding="0" cellspacing="0" class="mcnImageCardBottomContent" width="100%" style="background-color: #404040;border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
    <tbody><tr>
        <td class="mcnImageCardBottomImageContent" align="left" valign="top" style="padding-top: 0px;padding-right: 0px;padding-bottom: 0;padding-left: 0px;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">



            <img alt="" src="http://www.corelogs.com/images/thumbnails/baja.JPG" width="264" style="max-width: 552px;border: 0;height: auto;outline: none;text-decoration: none;-ms-interpolation-mode: bicubic;vertical-align: bottom;" class="mcnImage">


        </td>
    </tr>
    <tr>
        <td class="mcnTextContent" valign="top" style="padding: 9px 18px;color: #F2F2F2;font-family: Helvetica;font-size: 14px;font-weight: normal;text-align: center;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;word-break: break-word;line-height: 150%;" width="246">
            BAja SAE India & Baja Student India
        </td>
    </tr>
</tbody></table>




            </td>
        </tr>
    </tbody>
</table></td>
													</tr>
												</table>
												<!--[if gte mso 9]>
												</td>
												<td align="center" valign="top" width="300" style="width:300px;">
												<![endif]-->
												<table align="left" border="0" cellpadding="0" cellspacing="0" width="300" class="columnWrapper" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
													<tr>
														<td valign="top" class="columnContainer" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;"><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnImageCardBlock" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
    <tbody class="mcnImageCardBlockOuter">
        <tr>
            <td class="mcnImageCardBlockInner" valign="top" style="padding-top: 9px;padding-right: 18px;padding-bottom: 9px;padding-left: 18px;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">

<table align="left" border="0" cellpadding="0" cellspacing="0" class="mcnImageCardBottomContent" width="100%" style="background-color: #404040;border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
    <tbody><tr>
        <td class="mcnImageCardBottomImageContent" align="left" valign="top" style="padding-top: 0px;padding-right: 0px;padding-bottom: 0;padding-left: 0px;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">



            <img alt="" src="http://www.corelogs.com/images/thumbnails/fsae.JPG" width="264" style="max-width: 552px;border: 0;height: auto;outline: none;text-decoration: none;-ms-interpolation-mode: bicubic;vertical-align: bottom;" class="mcnImage">


        </td>
    </tr>
    <tr>
        <td class="mcnTextContent" valign="top" style="padding: 9px 18px;color: #F2F2F2;font-family: Helvetica;font-size: 14px;font-weight: normal;text-align: center;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;word-break: break-word;line-height: 150%;" width="246">
            Supra SAE India & Formula Student India
        </td>
    </tr>
</tbody></table>




            </td>
        </tr>
    </tbody>
</table></td>
													</tr>
												</table>
												<!--[if gte mso 9]>
												</td>
												</tr>
												</table>
												<![endif]-->
											</td>
										</tr>
									</table>
								</td>
                            </tr>
							<tr>
								<td align="center" valign="top" id="templateLowerBody" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;background-color: #FFFFFF;border-top: 0;border-bottom: 2px solid #EAEAEA;padding-top: 0;padding-bottom: 9px;">
									<!--[if gte mso 9]>
									<table align="center" border="0" cellspacing="0" cellpadding="0" width="600" style="width:600px;">
									<tr>
									<td align="center" valign="top" width="600" style="width:600px;">
									<![endif]-->
									<table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" class="templateContainer" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;max-width: 600px !important;">
										<tr>
                                			<td valign="top" class="bodyContainer" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;"><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnTextBlock" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
    <tbody class="mcnTextBlockOuter">
        <tr>
            <td valign="top" class="mcnTextBlockInner" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">

                <table align="left" border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnTextContentContainer" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
                    <tbody><tr>

                        <td valign="top" class="mcnTextContent" style="padding-top: 9px;padding-right: 18px;padding-bottom: 9px;padding-left: 18px;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;word-break: break-word;color: #202020;font-family: Helvetica;font-size: 16px;line-height: 150%;text-align: left;">

                            Through this event we want to emphasize how important it is to bring a culture of sharing and open source movement in Core Segment of Engineering. Let's Speed up the pace of development by following the principle of open source movement & knowledge sharing.<br>
The IT industry & the startup world learnt about <strong>Lean</strong> from the Core Segment of Engineering. Now Its our chance to learn about <strong>Open Source Technology </strong>from them<strong>.<br>
Ask, Answer & Write on CoreLogs to help others and make your mark on internet.</strong>
                        </td>
                    </tr>
                </tbody></table>

            </td>
        </tr>
    </tbody>
</table><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnButtonBlock" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
    <tbody class="mcnButtonBlockOuter">
        <tr>
            <td style="padding-top: 0;padding-right: 18px;padding-bottom: 18px;padding-left: 18px;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;" valign="top" align="center" class="mcnButtonBlockInner">
                <table border="0" cellpadding="0" cellspacing="0" class="mcnButtonContentContainer" style="border-collapse: separate !important;border-radius: 3px;background-color: #2BAADF;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
                    <tbody>
                        <tr>
                            <td align="center" valign="middle" class="mcnButtonContent" style="font-family: Arial;font-size: 16px;padding: 15px;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
                                <a class="mcnButton " title="Visit CoreLogs" href="http://www.corelogs.com" target="_blank" style="font-weight: bold;letter-spacing: normal;line-height: 100%;text-align: center;text-decoration: none;color: #FFFFFF;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;display: block;">Visit CoreLogs</a>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </td>
        </tr>
    </tbody>
</table></td>
										</tr>
									</table>
									<!--[if gte mso 9]>
									</td>
									</tr>
									</table>
									<![endif]-->
								</td>
                            </tr>
                            <tr>
								<td align="center" valign="top" id="templateFooter" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;background-color: #FAFAFA;border-top: 0;border-bottom: 0;padding-top: 9px;padding-bottom: 9px;">
									<!--[if gte mso 9]>
									<table align="center" border="0" cellspacing="0" cellpadding="0" width="600" style="width:600px;">
									<tr>
									<td align="center" valign="top" width="600" style="width:600px;">
									<![endif]-->
									<table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" class="templateContainer" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;max-width: 600px !important;">
										<tr>
                                			<td valign="top" class="footerContainer" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;"><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnFollowBlock" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
    <tbody class="mcnFollowBlockOuter">
        <tr>
            <td align="center" valign="top" style="padding: 9px;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;" class="mcnFollowBlockInner">
                <table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnFollowContentContainer" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
    <tbody><tr>
        <td align="center" style="padding-left: 9px;padding-right: 9px;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
            <table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnFollowContent" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
                <tbody><tr>
                    <td align="center" valign="top" style="padding-top: 9px;padding-right: 9px;padding-left: 9px;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
                        <table border="0" cellpadding="0" cellspacing="0" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
                            <tbody><tr>
                                <td valign="top" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
                                    <!--[if mso]>
                                    <table align="left" border="0" cellspacing="0" cellpadding="0" width="524">
                                    <tr>
                                    <td align="left" valign="top" width="524">
                                    <![endif]-->



                                            <table align="left" border="0" cellpadding="0" cellspacing="0" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
                                                <tbody><tr>
                                                    <td valign="top" style="padding-right: 10px;padding-bottom: 9px;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;" class="mcnFollowContentItemContainer">
                                                        <table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnFollowContentItem" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
                                                            <tbody><tr>
                                                                <td align="left" valign="middle" style="padding-top: 5px;padding-right: 10px;padding-bottom: 5px;padding-left: 9px;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
                                                                    <table align="left" border="0" cellpadding="0" cellspacing="0" width="" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
                                                                        <tbody><tr>

                                                                                <td align="center" valign="middle" width="24" class="mcnFollowIconContent" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
                                                                                    <a href="https://twitter.com/Corelogstwt" target="_blank" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;"><img src="http://cdn-images.mailchimp.com/icons/social-block-v2/color-twitter-48.png" style="display: block;border: 0;height: auto;outline: none;text-decoration: none;-ms-interpolation-mode: bicubic;" height="24" width="24" class=""></a>
                                                                                </td>


                                                                        </tr>
                                                                    </tbody></table>
                                                                </td>
                                                            </tr>
                                                        </tbody></table>
                                                    </td>
                                                </tr>
                                            </tbody></table>




                                            <table align="left" border="0" cellpadding="0" cellspacing="0" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
                                                <tbody><tr>
                                                    <td valign="top" style="padding-right: 10px;padding-bottom: 9px;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;" class="mcnFollowContentItemContainer">
                                                        <table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnFollowContentItem" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
                                                            <tbody><tr>
                                                                <td align="left" valign="middle" style="padding-top: 5px;padding-right: 10px;padding-bottom: 5px;padding-left: 9px;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
                                                                    <table align="left" border="0" cellpadding="0" cellspacing="0" width="" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
                                                                        <tbody><tr>

                                                                                <td align="center" valign="middle" width="24" class="mcnFollowIconContent" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
                                                                                    <a href="https://www.facebook.com/corelogs.page" target="_blank" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;"><img src="http://cdn-images.mailchimp.com/icons/social-block-v2/color-facebook-48.png" style="display: block;border: 0;height: auto;outline: none;text-decoration: none;-ms-interpolation-mode: bicubic;" height="24" width="24" class=""></a>
                                                                                </td>


                                                                        </tr>
                                                                    </tbody></table>
                                                                </td>
                                                            </tr>
                                                        </tbody></table>
                                                    </td>
                                                </tr>
                                            </tbody></table>




                                            <table align="left" border="0" cellpadding="0" cellspacing="0" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
                                                <tbody><tr>
                                                    <td valign="top" style="padding-right: 0;padding-bottom: 9px;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;" class="mcnFollowContentItemContainer">
                                                        <table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnFollowContentItem" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
                                                            <tbody><tr>
                                                                <td align="left" valign="middle" style="padding-top: 5px;padding-right: 10px;padding-bottom: 5px;padding-left: 9px;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
                                                                    <table align="left" border="0" cellpadding="0" cellspacing="0" width="" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
                                                                        <tbody><tr>

                                                                                <td align="center" valign="middle" width="24" class="mcnFollowIconContent" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
                                                                                    <a href="http://www.corelogs.com" target="_blank" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;"><img src="http://cdn-images.mailchimp.com/icons/social-block-v2/color-link-48.png" style="display: block;border: 0;height: auto;outline: none;text-decoration: none;-ms-interpolation-mode: bicubic;" height="24" width="24" class=""></a>
                                                                                </td>


                                                                        </tr>
                                                                    </tbody></table>
                                                                </td>
                                                            </tr>
                                                        </tbody></table>
                                                    </td>
                                                </tr>
                                            </tbody></table>


                                    <!--[if mso]>
                                    </td>
                                    </tr>
                                    </table>
                                    <![endif]-->
                                </td>
                            </tr>
                        </tbody></table>
                    </td>
                </tr>
            </tbody></table>
        </td>
    </tr>
</tbody></table>

            </td>
        </tr>
    </tbody>
</table></td>
										</tr>
									</table>
									<!--[if gte mso 9]>
									</td>
									</tr>
									</table>
									<![endif]-->
								</td>
                            </tr>
                        </table>
                        <!-- // END TEMPLATE -->
                    </td>
                </tr>
            </table>
        </center>
    </body>
</html>

Thanks
Surya Prakash
Founder
CoreLogs
'''

# test_mail
Template17 = u'''
Hi {0},

<!doctype html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">
	<head>
		<!-- NAME: 1:2:1 COLUMN - BANDED -->
		<!--[if gte mso 15]>
		<xml>
			<o:OfficeDocumentSettings>
			<o:AllowPNG/>
			<o:PixelsPerInch>96</o:PixelsPerInch>
			</o:OfficeDocumentSettings>
		</xml>
		<![endif]-->
		<meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1">
		<title>*|#CaptureYourTeam with CoreLogs & win cash prizes|*</title>

    <style type="text/css">
		p{{
			margin:10px 0;
			padding:0;
		}}
		table{{
			border-collapse:collapse;
		}}
		h1,h2,h3,h4,h5,h6{{
			display:block;
			margin:0;
			padding:0;
		}}
		img,a img{{
			border:0;
			height:auto;
			outline:none;
			text-decoration:none;
		}}
		body,#bodyTable,#bodyCell{{
			height:100%;
			margin:0;
			padding:0;
			width:100%;
		}}
		#outlook a{{
			padding:0;
		}}
		img{{
			-ms-interpolation-mode:bicubic;
		}}
		table{{
			mso-table-lspace:0pt;
			mso-table-rspace:0pt;
		}}
		.ReadMsgBody{{
			width:100%;
		}}
		.ExternalClass{{
			width:100%;
		}}
		p,a,li,td,blockquote{{
			mso-line-height-rule:exactly;
		}}
		a[href^=tel],a[href^=sms]{{
			color:inherit;
			cursor:default;
			text-decoration:none;
		}}
		p,a,li,td,body,table,blockquote{{
			-ms-text-size-adjust:100%;
			-webkit-text-size-adjust:100%;
		}}
		.ExternalClass,.ExternalClass p,.ExternalClass td,.ExternalClass div,.ExternalClass span,.ExternalClass font{{
			line-height:100%;
		}}
		a[x-apple-data-detectors]{{
			color:inherit !important;
			text-decoration:none !important;
			font-size:inherit !important;
			font-family:inherit !important;
			font-weight:inherit !important;
			line-height:inherit !important;
		}}
		.templateContainer{{
			max-width:600px !important;
		}}
		a.mcnButton{{
			display:block;
		}}
		.mcnImage{{
			vertical-align:bottom;
		}}
		.mcnTextContent{{
			word-break:break-word;
		}}
		.mcnTextContent img{{
			height:auto !important;
		}}
		.mcnDividerBlock{{
			table-layout:fixed !important;
		}}
		body,#bodyTable{{
			background-color:#FAFAFA;
		}}
		#bodyCell{{
			border-top:0;
		}}
		h1{{
			color:#202020;
			font-family:Helvetica;
			font-size:26px;
			font-style:normal;
			font-weight:bold;
			line-height:125%;
			letter-spacing:normal;
			text-align:left;
		}}
		h2{{
			color:#202020;
			font-family:Helvetica;
			font-size:22px;
			font-style:normal;
			font-weight:bold;
			line-height:125%;
			letter-spacing:normal;
			text-align:left;
		}}
		h3{{
			color:#202020;
			font-family:Helvetica;
			font-size:20px;
			font-style:normal;
			font-weight:bold;
			line-height:125%;
			letter-spacing:normal;
			text-align:left;
		}}
		h4{{
			color:#202020;
			font-family:Helvetica;
			font-size:18px;
			font-style:normal;
			font-weight:bold;
			line-height:125%;
			letter-spacing:normal;
			text-align:left;
		}}
		#templatePreheader{{
			background-color:#FAFAFA;
			border-top:0;
			border-bottom:0;
			padding-top:9px;
			padding-bottom:9px;
		}}
		#templatePreheader .mcnTextContent,#templatePreheader .mcnTextContent p{{
			color:#656565;
			font-family:Helvetica;
			font-size:12px;
			line-height:150%;
			text-align:left;
		}}
		#templatePreheader .mcnTextContent a,#templatePreheader .mcnTextContent p a{{
			color:#656565;
			font-weight:normal;
			text-decoration:underline;
		}}
		#templateHeader{{
			background-color:#FFFFFF;
			border-top:0;
			border-bottom:0;
			padding-top:9px;
			padding-bottom:0;
		}}
		#templateHeader .mcnTextContent,#templateHeader .mcnTextContent p{{
			color:#202020;
			font-family:Helvetica;
			font-size:16px;
			line-height:150%;
			text-align:left;
		}}
		#templateHeader .mcnTextContent a,#templateHeader .mcnTextContent p a{{
			color:#2BAADF;
			font-weight:normal;
			text-decoration:underline;
		}}
		#templateUpperBody{{
			background-color:#FFFFFF;
			border-top:0;
			border-bottom:0;
			padding-top:0;
			padding-bottom:0;
		}}
		#templateUpperBody .mcnTextContent,#templateUpperBody .mcnTextContent p{{
			color:#202020;
			font-family:Helvetica;
			font-size:16px;
			line-height:150%;
			text-align:left;
		}}
		#templateUpperBody .mcnTextContent a,#templateUpperBody .mcnTextContent p a{{
			color:#2BAADF;
			font-weight:normal;
			text-decoration:underline;
		}}
		#templateColumns{{
			background-color:#FFFFFF;
			border-top:0;
			border-bottom:0;
			padding-top:0;
			padding-bottom:0;
		}}
		#templateColumns .columnContainer .mcnTextContent,#templateColumns .columnContainer .mcnTextContent p{{
			color:#202020;
			font-family:Helvetica;
			font-size:16px;
			line-height:150%;
			text-align:left;
		}}
		#templateColumns .columnContainer .mcnTextContent a,#templateColumns .columnContainer .mcnTextContent p a{{
			color:#2BAADF;
			font-weight:normal;
			text-decoration:underline;
		}}
		#templateLowerBody{{
			background-color:#FFFFFF;
			border-top:0;
			border-bottom:2px solid #EAEAEA;
			padding-top:0;
			padding-bottom:9px;
		}}
		#templateLowerBody .mcnTextContent,#templateLowerBody .mcnTextContent p{{
			color:#202020;
			font-family:Helvetica;
			font-size:16px;
			line-height:150%;
			text-align:left;
		}}
		#templateLowerBody .mcnTextContent a,#templateLowperBody .mcnTextContent p a{{
			color:#2BAADF;
			font-weight:normal;
			text-decoration:underline;
		}}
		#templateFooter{{
			background-color:#FAFAFA;
			border-top:0;
			border-bottom:0;
			padding-top:9px;
			padding-bottom:9px;
		}}
		#templateFooter .mcnTextContent,#templateFooter .mcnTextContent p{{
			color:#656565;
			font-family:Helvetica;
			font-size:12px;
			line-height:150%;
			text-align:center;
		}}
		#templateFooter .mcnTextContent a,#templateFooter .mcnTextContent p a{{
			color:#656565;
			font-weight:normal;
			text-decoration:underline;
		}}
	@media only screen and (min-width:768px){{
		.templateContainer{{
			width:600px !important;
		}}

}}	@media only screen and (max-width: 480px){{
		body,table,td,p,a,li,blockquote{{
			-webkit-text-size-adjust:none !important;
		}}

}}	@media only screen and (max-width: 480px){{
		body{{
			width:100% !important;
			min-width:100% !important;
		}}

}}	@media only screen and (max-width: 480px){{
		#bodyCell{{
			padding-top:10px !important;
		}}

}}	@media only screen and (max-width: 480px){{
		.columnWrapper{{
			max-width:100% !important;
			width:100% !important;
		}}

}}	@media only screen and (max-width: 480px){{
		.mcnImage{{
			width:100% !important;
		}}

}}	@media only screen and (max-width: 480px){{
		.mcnShareContent,.mcnCaptionTopContent,.mcnCaptionBottomContent,.mcnTextContentContainer,.mcnBoxedTextContentContainer,.mcnImageGroupContentContainer,.mcnCaptionLeftTextContentContainer,.mcnCaptionRightTextContentContainer,.mcnCaptionLeftImageContentContainer,.mcnCaptionRightImageContentContainer,.mcnImageCardLeftTextContentContainer,.mcnImageCardRightTextContentContainer{{
			max-width:100% !important;
			width:100% !important;
		}}

}}	@media only screen and (max-width: 480px){{
		.mcnBoxedTextContentContainer{{
			min-width:100% !important;
		}}

}}	@media only screen and (max-width: 480px){{
		.mcnImageGroupContent{{
			padding:9px !important;
		}}

}}	@media only screen and (max-width: 480px){{
		.mcnCaptionLeftContentOuter .mcnTextContent,.mcnCaptionRightContentOuter .mcnTextContent{{
			padding-top:9px !important;
		}}

}}	@media only screen and (max-width: 480px){{
		.mcnImageCardTopImageContent,.mcnCaptionBlockInner .mcnCaptionTopContent:last-child .mcnTextContent{{
			padding-top:18px !important;
		}}

}}	@media only screen and (max-width: 480px){{
		.mcnImageCardBottomImageContent{{
			padding-bottom:9px !important;
		}}

}}	@media only screen and (max-width: 480px){{
		.mcnImageGroupBlockInner{{
			padding-top:0 !important;
			padding-bottom:0 !important;
		}}

}}	@media only screen and (max-width: 480px){{
		.mcnImageGroupBlockOuter{{
			padding-top:9px !important;
			padding-bottom:9px !important;
		}}

}}	@media only screen and (max-width: 480px){{
		.mcnTextContent,.mcnBoxedTextContentColumn{{
			padding-right:18px !important;
			padding-left:18px !important;
		}}

}}	@media only screen and (max-width: 480px){{
		.mcnImageCardLeftImageContent,.mcnImageCardRightImageContent{{
			padding-right:18px !important;
			padding-bottom:0 !important;
			padding-left:18px !important;
		}}

}}	@media only screen and (max-width: 480px){{
		.mcpreview-image-uploader{{
			display:none !important;
			width:100% !important;
		}}

}}	@media only screen and (max-width: 480px){{
		h1{{
			font-size:22px !important;
			line-height:125% !important;
		}}

}}	@media only screen and (max-width: 480px){{
		h2{{
			font-size:20px !important;
			line-height:125% !important;
		}}

}}	@media only screen and (max-width: 480px){{
		h3{{
			font-size:18px !important;
			line-height:125% !important;
		}}

}}	@media only screen and (max-width: 480px){{
		h4{{
			font-size:16px !important;
			line-height:150% !important;
		}}

}}	@media only screen and (max-width: 480px){{
		.mcnBoxedTextContentContainer .mcnTextContent,.mcnBoxedTextContentContainer .mcnTextContent p{{
			font-size:14px !important;
			line-height:150% !important;
		}}

}}	@media only screen and (max-width: 480px){{
		#templatePreheader{{
			display:block !important;
		}}

}}	@media only screen and (max-width: 480px){{
		#templatePreheader .mcnTextContent,#templatePreheader .mcnTextContent p{{
			font-size:14px !important;
			line-height:150% !important;
		}}

}}	@media only screen and (max-width: 480px){{
		#templateHeader .mcnTextContent,#templateHeader .mcnTextContent p{{
			font-size:16px !important;
			line-height:150% !important;
		}}

}}	@media only screen and (max-width: 480px){{
		#templateUpperBody .mcnTextContent,#templateUpperBody .mcnTextContent p{{
			font-size:16px !important;
			line-height:150% !important;
		}}

}}	@media only screen and (max-width: 480px){{
		#templateColumns .columnContainer .mcnTextContent,#templateColumns .columnContainer .mcnTextContent p{{
			font-size:16px !important;
			line-height:150% !important;
		}}

}}	@media only screen and (max-width: 480px){{
		#templateLowerBody .mcnTextContent,#templateLowerBody .mcnTextContent p{{
			font-size:16px !important;
			line-height:150% !important;
		}}

}}	@media only screen and (max-width: 480px){{
		#templateFooter .mcnTextContent,#templateFooter .mcnTextContent p{{
			font-size:14px !important;
			line-height:150% !important;
		}}

}}</style></head>
    <body style="height: 100%;margin: 0;padding: 0;width: 100%;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;background-color: #FAFAFA;">
        <center>
            <table align="center" border="0" cellpadding="0" cellspacing="0" height="100%" width="100%" id="bodyTable" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;height: 100%;margin: 0;padding: 0;width: 100%;background-color: #FAFAFA;">
                <tr>
                    <td align="center" valign="top" id="bodyCell" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;height: 100%;margin: 0;padding: 0;width: 100%;border-top: 0;">
                        <!-- BEGIN TEMPLATE // -->
                        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
                            <tr>
								<td align="center" valign="top" id="templatePreheader" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;background-color: #FAFAFA;border-top: 0;border-bottom: 0;padding-top: 9px;padding-bottom: 9px;">
									<!--[if gte mso 9]>
									<table align="center" border="0" cellspacing="0" cellpadding="0" width="600" style="width:600px;">
									<tr>
									<td align="center" valign="top" width="600" style="width:600px;">
									<![endif]-->
									<table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" class="templateContainer" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;max-width: 600px !important;">
										<tr>
                                			<td valign="top" class="preheaderContainer" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;"><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnTextBlock" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
    <tbody class="mcnTextBlockOuter">
        <tr>
            <td valign="top" class="mcnTextBlockInner" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">

                <table align="left" border="0" cellpadding="0" cellspacing="0" width="366" class="mcnTextContentContainer" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
                    <tbody><tr>

                        <td valign="top" class="mcnTextContent" style="padding-top: 9px;padding-left: 18px;padding-bottom: 9px;padding-right: 0;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;word-break: break-word;color: #656565;font-family: Helvetica;font-size: 12px;line-height: 150%;text-align: left;">

                            #CaptureYourTeam & Win exciting prizes
                        </td>
                    </tr>
                </tbody></table>

                <table align="right" border="0" cellpadding="0" cellspacing="0" width="197" class="mcnTextContentContainer" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
                    <tbody><tr>

                        <td valign="top" class="mcnTextContent" style="padding-top: 9px;padding-right: 18px;padding-bottom: 9px;padding-left: 0;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;word-break: break-word;color: #656565;font-family: Helvetica;font-size: 12px;line-height: 150%;text-align: left;">

                            <a href="http://www.corelogs.com/" target="_blank" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;color: #656565;font-weight: normal;text-decoration: underline;">View this email in your browser</a>
                        </td>
                    </tr>
                </tbody></table>

            </td>
        </tr>
    </tbody>
</table></td>
										</tr>
									</table>
									<!--[if gte mso 9]>
									</td>
									</tr>
									</table>
									<![endif]-->
								</td>
                            </tr>
							<tr>
								<td align="center" valign="top" id="templateHeader" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;background-color: #FFFFFF;border-top: 0;border-bottom: 0;padding-top: 9px;padding-bottom: 0;">
									<!--[if gte mso 9]>
									<table align="center" border="0" cellspacing="0" cellpadding="0" width="600" style="width:600px;">
									<tr>
									<td align="center" valign="top" width="600" style="width:600px;">
									<![endif]-->
									<table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" class="templateContainer" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;max-width: 600px !important;">
										<tr>
                                			<td valign="top" class="headerContainer" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;"><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnCaptionBlock" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
    <tbody class="mcnCaptionBlockOuter">
        <tr>
            <td class="mcnCaptionBlockInner" valign="top" style="padding: 9px;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">




<table border="0" cellpadding="0" cellspacing="0" class="mcnCaptionRightContentOuter" width="100%" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
    <tbody><tr>
        <td valign="top" class="mcnCaptionRightContentInner" style="padding: 0 9px;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
            <table align="left" border="0" cellpadding="0" cellspacing="0" class="mcnCaptionRightImageContentContainer" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
                <tbody><tr>
                    <td class="mcnCaptionRightImageContent" valign="top" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">



                        <img alt="" src="http://www.corelogs.com/images/thumbnails/corelogs_logo.jpg" width="176" style="max-width: 552px;border: 0;height: auto;outline: none;text-decoration: none;-ms-interpolation-mode: bicubic;vertical-align: bottom;" class="mcnImage">



                    </td>
                </tr>
            </tbody></table>
            <table class="mcnCaptionRightTextContentContainer" align="right" border="0" cellpadding="0" cellspacing="0" width="352" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
                <tbody><tr>
                    <td valign="top" class="mcnTextContent" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;word-break: break-word;color: #202020;font-family: Helvetica;font-size: 16px;line-height: 150%;text-align: left;">
                        <span style="font-size:22px">CoreLogs</span>.com is a platform for SAE related collegiate clubs to get connected to each other and the Engineers, experts & Industrialists across the world. Visit <a href="http://www.corelogs.com/forum/" target="_blank" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;color: #2BAADF;font-weight: normal;text-decoration: underline;">The Engineer's Forum</a> to ask & answer Technical questions.
                    </td>
                </tr>
            </tbody></table>
        </td>
    </tr>
</tbody></table>




            </td>
        </tr>
    </tbody>
</table></td>
										</tr>
									</table>
									<!--[if gte mso 9]>
									</td>
									</tr>
									</table>
									<![endif]-->
								</td>
                            </tr>
							<tr>
								<td align="center" valign="top" id="templateUpperBody" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;background-color: #FFFFFF;border-top: 0;border-bottom: 0;padding-top: 0;padding-bottom: 0;">
									<!--[if gte mso 9]>
									<table align="center" border="0" cellspacing="0" cellpadding="0" width="600" style="width:600px;">
									<tr>
									<td align="center" valign="top" width="600" style="width:600px;">
									<![endif]-->
									<table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" class="templateContainer" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;max-width: 600px !important;">
										<tr>
                                			<td valign="top" class="bodyContainer" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;"><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnTextBlock" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
    <tbody class="mcnTextBlockOuter">
        <tr>
            <td valign="top" class="mcnTextBlockInner" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">

                <table align="left" border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnTextContentContainer" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
                    <tbody><tr>

                        <td valign="top" class="mcnTextContent" style="padding-top: 9px;padding-right: 18px;padding-bottom: 9px;padding-left: 18px;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;word-break: break-word;color: #202020;font-family: Helvetica;font-size: 16px;line-height: 150%;text-align: left;">

                            <h1 style="display: block;margin: 0;padding: 0;color: #202020;font-family: Helvetica;font-size: 26px;font-style: normal;font-weight: bold;line-height: 125%;letter-spacing: normal;text-align: left;">Capture Your Team and win exciting prizes</h1>

<p style="margin: 10px 0;padding: 0;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;color: #202020;font-family: Helvetica;font-size: 16px;line-height: 150%;text-align: left;"><span style="font-size:22px; line-height:20.8px">CoreLogs</span><span style="line-height:20.8px">.com brings a facebook event </span><a class="_58cn" data-ft="{{"tn":"*N","type":104}}" href="https://www.facebook.com/hashtag/captureyourteam?source=feed_text&story_id=1635510520046599" style="color: #3B5998;cursor: pointer;text-decoration: none;font-family: helvetica, arial, sans-serif;font-size: 14px;line-height: 19.32px;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;font-weight: normal;"><span aria-label="hashtag" class="_58cl" style="color: #627AAD;">#</span><span class="_58cm">CAPTUREYOURTEAM?</span></a><span style="color: #141823;font-family: helvetica,arial,sans-serif;font-size: 14px;line-height: 19.32px;"> for the SAE related Teams across India. You send us a pic of your car, we upload it from our facebook page. The teams with maximum likes win exciting prizes. Visit our <a href="https://www.facebook.com/corelogs.page" target="_blank" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;color: #2BAADF;font-weight: normal;text-decoration: underline;">facebook page</a> for <a href="https://www.facebook.com/notes/corelogs/rules-and-regulations-for-online-event/1635293750068276" target="_blank" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;color: #2BAADF;font-weight: normal;text-decoration: underline;">details and rules</a>.<br>
You can send us the image at <a href="mailto:info@corelogs.com?subject=Paticipation%20in%20%23captureyourteam" target="_blank" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;color: #2BAADF;font-weight: normal;text-decoration: underline;">info@corelogs.com</a> by 30th November. <strong>The sooner the better.<br>
It is for Baja, Supra/ Formula student India, efficycle, supermileage Teams.</strong></span></p>

                        </td>
                    </tr>
                </tbody></table>

            </td>
        </tr>
    </tbody>
</table></td>
										</tr>
									</table>
									<!--[if gte mso 9]>
									</td>
									</tr>
									</table>
									<![endif]-->
								</td>
                            </tr>
							<tr>
								<td align="center" valign="top" id="templateColumns" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;background-color: #FFFFFF;border-top: 0;border-bottom: 0;padding-top: 0;padding-bottom: 0;">
									<table border="0" cellpadding="0" cellspacing="0" width="100%" class="templateContainer" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;max-width: 600px !important;">
                                        <tr>
                                            <td align="center" valign="top" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
												<!--[if gte mso 9]>
												<table align="center" border="0" cellspacing="0" cellpadding="0" width="600" style="width:600px;">
												<tr>
												<td align="center" valign="top" width="300" style="width:300px;">
												<![endif]-->
												<table align="left" border="0" cellpadding="0" cellspacing="0" width="300" class="columnWrapper" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
													<tr>
														<td valign="top" class="columnContainer" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;"><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnImageCardBlock" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
    <tbody class="mcnImageCardBlockOuter">
        <tr>
            <td class="mcnImageCardBlockInner" valign="top" style="padding-top: 9px;padding-right: 18px;padding-bottom: 9px;padding-left: 18px;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">

<table align="right" border="0" cellpadding="0" cellspacing="0" class="mcnImageCardBottomContent" width="100%" style="background-color: #404040;border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
    <tbody><tr>
        <td class="mcnImageCardBottomImageContent" align="left" valign="top" style="padding-top: 0px;padding-right: 0px;padding-bottom: 0;padding-left: 0px;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">



            <img alt="" src="http://www.corelogs.com/images/thumbnails/baja.JPG" width="264" style="max-width: 552px;border: 0;height: auto;outline: none;text-decoration: none;-ms-interpolation-mode: bicubic;vertical-align: bottom;" class="mcnImage">


        </td>
    </tr>
    <tr>
        <td class="mcnTextContent" valign="top" style="padding: 9px 18px;color: #F2F2F2;font-family: Helvetica;font-size: 14px;font-weight: normal;text-align: center;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;word-break: break-word;line-height: 150%;" width="246">
            BAja SAE India & Baja Student India
        </td>
    </tr>
</tbody></table>




            </td>
        </tr>
    </tbody>
</table></td>
													</tr>
												</table>
												<!--[if gte mso 9]>
												</td>
												<td align="center" valign="top" width="300" style="width:300px;">
												<![endif]-->
												<table align="left" border="0" cellpadding="0" cellspacing="0" width="300" class="columnWrapper" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
													<tr>
														<td valign="top" class="columnContainer" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;"><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnImageCardBlock" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
    <tbody class="mcnImageCardBlockOuter">
        <tr>
            <td class="mcnImageCardBlockInner" valign="top" style="padding-top: 9px;padding-right: 18px;padding-bottom: 9px;padding-left: 18px;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">

<table align="left" border="0" cellpadding="0" cellspacing="0" class="mcnImageCardBottomContent" width="100%" style="background-color: #404040;border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
    <tbody><tr>
        <td class="mcnImageCardBottomImageContent" align="left" valign="top" style="padding-top: 0px;padding-right: 0px;padding-bottom: 0;padding-left: 0px;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">



            <img alt="" src="http://www.corelogs.com/images/thumbnails/fsae.JPG" width="264" style="max-width: 552px;border: 0;height: auto;outline: none;text-decoration: none;-ms-interpolation-mode: bicubic;vertical-align: bottom;" class="mcnImage">


        </td>
    </tr>
    <tr>
        <td class="mcnTextContent" valign="top" style="padding: 9px 18px;color: #F2F2F2;font-family: Helvetica;font-size: 14px;font-weight: normal;text-align: center;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;word-break: break-word;line-height: 150%;" width="246">
            Supra SAE India & Formula Student India
        </td>
    </tr>
</tbody></table>




            </td>
        </tr>
    </tbody>
</table></td>
													</tr>
												</table>
												<!--[if gte mso 9]>
												</td>
												</tr>
												</table>
												<![endif]-->
											</td>
										</tr>
									</table>
								</td>
                            </tr>
							<tr>
								<td align="center" valign="top" id="templateLowerBody" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;background-color: #FFFFFF;border-top: 0;border-bottom: 2px solid #EAEAEA;padding-top: 0;padding-bottom: 9px;">
									<!--[if gte mso 9]>
									<table align="center" border="0" cellspacing="0" cellpadding="0" width="600" style="width:600px;">
									<tr>
									<td align="center" valign="top" width="600" style="width:600px;">
									<![endif]-->
									<table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" class="templateContainer" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;max-width: 600px !important;">
										<tr>
                                			<td valign="top" class="bodyContainer" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;"><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnTextBlock" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
    <tbody class="mcnTextBlockOuter">
        <tr>
            <td valign="top" class="mcnTextBlockInner" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">

                <table align="left" border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnTextContentContainer" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
                    <tbody><tr>

                        <td valign="top" class="mcnTextContent" style="padding-top: 9px;padding-right: 18px;padding-bottom: 9px;padding-left: 18px;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;word-break: break-word;color: #202020;font-family: Helvetica;font-size: 16px;line-height: 150%;text-align: left;">

                            Through this event we want to emphasize how important it is to bring a culture of sharing and open source movement in Core Segment of Engineering. Let's Speed up the pace of development by following the principle of open source movement & knowledge sharing.<br>
The IT industry & the startup world learnt about <strong>Lean</strong> from the Core Segment of Engineering. Now Its our chance to learn about <strong>Open Source Technology </strong>from them<strong>.<br>
Ask, Answer & Write on CoreLogs to help others and make your mark on internet.</strong>
                        </td>
                    </tr>
                </tbody></table>

            </td>
        </tr>
    </tbody>
</table><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnButtonBlock" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
    <tbody class="mcnButtonBlockOuter">
        <tr>
            <td style="padding-top: 0;padding-right: 18px;padding-bottom: 18px;padding-left: 18px;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;" valign="top" align="center" class="mcnButtonBlockInner">
                <table border="0" cellpadding="0" cellspacing="0" class="mcnButtonContentContainer" style="border-collapse: separate !important;border-radius: 3px;background-color: #2BAADF;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
                    <tbody>
                        <tr>
                            <td align="center" valign="middle" class="mcnButtonContent" style="font-family: Arial;font-size: 16px;padding: 15px;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
                                <a class="mcnButton " title="Visit CoreLogs" href="http://www.corelogs.com" target="_blank" style="font-weight: bold;letter-spacing: normal;line-height: 100%;text-align: center;text-decoration: none;color: #FFFFFF;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;display: block;">Visit CoreLogs</a>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </td>
        </tr>
    </tbody>
</table></td>
										</tr>
									</table>
									<!--[if gte mso 9]>
									</td>
									</tr>
									</table>
									<![endif]-->
								</td>
                            </tr>
                            <tr>
								<td align="center" valign="top" id="templateFooter" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;background-color: #FAFAFA;border-top: 0;border-bottom: 0;padding-top: 9px;padding-bottom: 9px;">
									<!--[if gte mso 9]>
									<table align="center" border="0" cellspacing="0" cellpadding="0" width="600" style="width:600px;">
									<tr>
									<td align="center" valign="top" width="600" style="width:600px;">
									<![endif]-->
									<table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" class="templateContainer" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;max-width: 600px !important;">
										<tr>
                                			<td valign="top" class="footerContainer" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;"><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnFollowBlock" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
    <tbody class="mcnFollowBlockOuter">
        <tr>
            <td align="center" valign="top" style="padding: 9px;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;" class="mcnFollowBlockInner">
                <table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnFollowContentContainer" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
    <tbody><tr>
        <td align="center" style="padding-left: 9px;padding-right: 9px;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
            <table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnFollowContent" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
                <tbody><tr>
                    <td align="center" valign="top" style="padding-top: 9px;padding-right: 9px;padding-left: 9px;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
                        <table border="0" cellpadding="0" cellspacing="0" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
                            <tbody><tr>
                                <td valign="top" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
                                    <!--[if mso]>
                                    <table align="left" border="0" cellspacing="0" cellpadding="0" width="524">
                                    <tr>
                                    <td align="left" valign="top" width="524">
                                    <![endif]-->



                                            <table align="left" border="0" cellpadding="0" cellspacing="0" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
                                                <tbody><tr>
                                                    <td valign="top" style="padding-right: 10px;padding-bottom: 9px;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;" class="mcnFollowContentItemContainer">
                                                        <table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnFollowContentItem" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
                                                            <tbody><tr>
                                                                <td align="left" valign="middle" style="padding-top: 5px;padding-right: 10px;padding-bottom: 5px;padding-left: 9px;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
                                                                    <table align="left" border="0" cellpadding="0" cellspacing="0" width="" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
                                                                        <tbody><tr>

                                                                                <td align="center" valign="middle" width="24" class="mcnFollowIconContent" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
                                                                                    <a href="https://twitter.com/Corelogstwt" target="_blank" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;"><img src="http://cdn-images.mailchimp.com/icons/social-block-v2/color-twitter-48.png" style="display: block;border: 0;height: auto;outline: none;text-decoration: none;-ms-interpolation-mode: bicubic;" height="24" width="24" class=""></a>
                                                                                </td>


                                                                        </tr>
                                                                    </tbody></table>
                                                                </td>
                                                            </tr>
                                                        </tbody></table>
                                                    </td>
                                                </tr>
                                            </tbody></table>




                                            <table align="left" border="0" cellpadding="0" cellspacing="0" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
                                                <tbody><tr>
                                                    <td valign="top" style="padding-right: 10px;padding-bottom: 9px;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;" class="mcnFollowContentItemContainer">
                                                        <table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnFollowContentItem" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
                                                            <tbody><tr>
                                                                <td align="left" valign="middle" style="padding-top: 5px;padding-right: 10px;padding-bottom: 5px;padding-left: 9px;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
                                                                    <table align="left" border="0" cellpadding="0" cellspacing="0" width="" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
                                                                        <tbody><tr>

                                                                                <td align="center" valign="middle" width="24" class="mcnFollowIconContent" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
                                                                                    <a href="https://www.facebook.com/corelogs.page" target="_blank" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;"><img src="http://cdn-images.mailchimp.com/icons/social-block-v2/color-facebook-48.png" style="display: block;border: 0;height: auto;outline: none;text-decoration: none;-ms-interpolation-mode: bicubic;" height="24" width="24" class=""></a>
                                                                                </td>


                                                                        </tr>
                                                                    </tbody></table>
                                                                </td>
                                                            </tr>
                                                        </tbody></table>
                                                    </td>
                                                </tr>
                                            </tbody></table>




                                            <table align="left" border="0" cellpadding="0" cellspacing="0" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
                                                <tbody><tr>
                                                    <td valign="top" style="padding-right: 0;padding-bottom: 9px;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;" class="mcnFollowContentItemContainer">
                                                        <table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnFollowContentItem" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
                                                            <tbody><tr>
                                                                <td align="left" valign="middle" style="padding-top: 5px;padding-right: 10px;padding-bottom: 5px;padding-left: 9px;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
                                                                    <table align="left" border="0" cellpadding="0" cellspacing="0" width="" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
                                                                        <tbody><tr>

                                                                                <td align="center" valign="middle" width="24" class="mcnFollowIconContent" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
                                                                                    <a href="http://www.corelogs.com" target="_blank" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;"><img src="http://cdn-images.mailchimp.com/icons/social-block-v2/color-link-48.png" style="display: block;border: 0;height: auto;outline: none;text-decoration: none;-ms-interpolation-mode: bicubic;" height="24" width="24" class=""></a>
                                                                                </td>


                                                                        </tr>
                                                                    </tbody></table>
                                                                </td>
                                                            </tr>
                                                        </tbody></table>
                                                    </td>
                                                </tr>
                                            </tbody></table>


                                    <!--[if mso]>
                                    </td>
                                    </tr>
                                    </table>
                                    <![endif]-->
                                </td>
                            </tr>
                        </tbody></table>
                    </td>
                </tr>
            </tbody></table>
        </td>
    </tr>
</tbody></table>

            </td>
        </tr>
    </tbody>
</table></td>
										</tr>
									</table>
									<!--[if gte mso 9]>
									</td>
									</tr>
									</table>
									<![endif]-->
								</td>
                            </tr>
                        </table>
                        <!-- // END TEMPLATE -->
                    </td>
                </tr>
            </table>
        </center>
    </body>
</html>

Thanks
Surya Prakash
'''

# list_mail
Template18 = u'''
Hi {0},

<!doctype html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">
	<head>
		<!-- NAME: 1:2:1 COLUMN - BANDED -->
		<!--[if gte mso 15]>
		<xml>
			<o:OfficeDocumentSettings>
			<o:AllowPNG/>
			<o:PixelsPerInch>96</o:PixelsPerInch>
			</o:OfficeDocumentSettings>
		</xml>
		<![endif]-->
		<meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1">
		<title>*|#CaptureYourTeam with CoreLogs & win cash prizes|*</title>

    <style type="text/css">
		p{{
			margin:10px 0;
			padding:0;
		}}
		table{{
			border-collapse:collapse;
		}}
		h1,h2,h3,h4,h5,h6{{
			display:block;
			margin:0;
			padding:0;
		}}
		img,a img{{
			border:0;
			height:auto;
			outline:none;
			text-decoration:none;
		}}
		body,#bodyTable,#bodyCell{{
			height:100%;
			margin:0;
			padding:0;
			width:100%;
		}}
		#outlook a{{
			padding:0;
		}}
		img{{
			-ms-interpolation-mode:bicubic;
		}}
		table{{
			mso-table-lspace:0pt;
			mso-table-rspace:0pt;
		}}
		.ReadMsgBody{{
			width:100%;
		}}
		.ExternalClass{{
			width:100%;
		}}
		p,a,li,td,blockquote{{
			mso-line-height-rule:exactly;
		}}
		a[href^=tel],a[href^=sms]{{
			color:inherit;
			cursor:default;
			text-decoration:none;
		}}
		p,a,li,td,body,table,blockquote{{
			-ms-text-size-adjust:100%;
			-webkit-text-size-adjust:100%;
		}}
		.ExternalClass,.ExternalClass p,.ExternalClass td,.ExternalClass div,.ExternalClass span,.ExternalClass font{{
			line-height:100%;
		}}
		a[x-apple-data-detectors]{{
			color:inherit !important;
			text-decoration:none !important;
			font-size:inherit !important;
			font-family:inherit !important;
			font-weight:inherit !important;
			line-height:inherit !important;
		}}
		.templateContainer{{
			max-width:600px !important;
		}}
		a.mcnButton{{
			display:block;
		}}
		.mcnImage{{
			vertical-align:bottom;
		}}
		.mcnTextContent{{
			word-break:break-word;
		}}
		.mcnTextContent img{{
			height:auto !important;
		}}
		.mcnDividerBlock{{
			table-layout:fixed !important;
		}}
		body,#bodyTable{{
			background-color:#FAFAFA;
		}}
		#bodyCell{{
			border-top:0;
		}}
		h1{{
			color:#202020;
			font-family:Helvetica;
			font-size:26px;
			font-style:normal;
			font-weight:bold;
			line-height:125%;
			letter-spacing:normal;
			text-align:left;
		}}
		h2{{
			color:#202020;
			font-family:Helvetica;
			font-size:22px;
			font-style:normal;
			font-weight:bold;
			line-height:125%;
			letter-spacing:normal;
			text-align:left;
		}}
		h3{{
			color:#202020;
			font-family:Helvetica;
			font-size:20px;
			font-style:normal;
			font-weight:bold;
			line-height:125%;
			letter-spacing:normal;
			text-align:left;
		}}
		h4{{
			color:#202020;
			font-family:Helvetica;
			font-size:18px;
			font-style:normal;
			font-weight:bold;
			line-height:125%;
			letter-spacing:normal;
			text-align:left;
		}}
		#templatePreheader{{
			background-color:#FAFAFA;
			border-top:0;
			border-bottom:0;
			padding-top:9px;
			padding-bottom:9px;
		}}
		#templatePreheader .mcnTextContent,#templatePreheader .mcnTextContent p{{
			color:#656565;
			font-family:Helvetica;
			font-size:12px;
			line-height:150%;
			text-align:left;
		}}
		#templatePreheader .mcnTextContent a,#templatePreheader .mcnTextContent p a{{
			color:#656565;
			font-weight:normal;
			text-decoration:underline;
		}}
		#templateHeader{{
			background-color:#FFFFFF;
			border-top:0;
			border-bottom:0;
			padding-top:9px;
			padding-bottom:0;
		}}
		#templateHeader .mcnTextContent,#templateHeader .mcnTextContent p{{
			color:#202020;
			font-family:Helvetica;
			font-size:16px;
			line-height:150%;
			text-align:left;
		}}
		#templateHeader .mcnTextContent a,#templateHeader .mcnTextContent p a{{
			color:#2BAADF;
			font-weight:normal;
			text-decoration:underline;
		}}
		#templateUpperBody{{
			background-color:#FFFFFF;
			border-top:0;
			border-bottom:0;
			padding-top:0;
			padding-bottom:0;
		}}
		#templateUpperBody .mcnTextContent,#templateUpperBody .mcnTextContent p{{
			color:#202020;
			font-family:Helvetica;
			font-size:16px;
			line-height:150%;
			text-align:left;
		}}
		#templateUpperBody .mcnTextContent a,#templateUpperBody .mcnTextContent p a{{
			color:#2BAADF;
			font-weight:normal;
			text-decoration:underline;
		}}
		#templateColumns{{
			background-color:#FFFFFF;
			border-top:0;
			border-bottom:0;
			padding-top:0;
			padding-bottom:0;
		}}
		#templateColumns .columnContainer .mcnTextContent,#templateColumns .columnContainer .mcnTextContent p{{
			color:#202020;
			font-family:Helvetica;
			font-size:16px;
			line-height:150%;
			text-align:left;
		}}
		#templateColumns .columnContainer .mcnTextContent a,#templateColumns .columnContainer .mcnTextContent p a{{
			color:#2BAADF;
			font-weight:normal;
			text-decoration:underline;
		}}
		#templateLowerBody{{
			background-color:#FFFFFF;
			border-top:0;
			border-bottom:2px solid #EAEAEA;
			padding-top:0;
			padding-bottom:9px;
		}}
		#templateLowerBody .mcnTextContent,#templateLowerBody .mcnTextContent p{{
			color:#202020;
			font-family:Helvetica;
			font-size:16px;
			line-height:150%;
			text-align:left;
		}}
		#templateLowerBody .mcnTextContent a,#templateLowperBody .mcnTextContent p a{{
			color:#2BAADF;
			font-weight:normal;
			text-decoration:underline;
		}}
		#templateFooter{{
			background-color:#FAFAFA;
			border-top:0;
			border-bottom:0;
			padding-top:9px;
			padding-bottom:9px;
		}}
		#templateFooter .mcnTextContent,#templateFooter .mcnTextContent p{{
			color:#656565;
			font-family:Helvetica;
			font-size:12px;
			line-height:150%;
			text-align:center;
		}}
		#templateFooter .mcnTextContent a,#templateFooter .mcnTextContent p a{{
			color:#656565;
			font-weight:normal;
			text-decoration:underline;
		}}
	@media only screen and (min-width:768px){{
		.templateContainer{{
			width:600px !important;
		}}

}}	@media only screen and (max-width: 480px){{
		body,table,td,p,a,li,blockquote{{
			-webkit-text-size-adjust:none !important;
		}}

}}	@media only screen and (max-width: 480px){{
		body{{
			width:100% !important;
			min-width:100% !important;
		}}

}}	@media only screen and (max-width: 480px){{
		#bodyCell{{
			padding-top:10px !important;
		}}

}}	@media only screen and (max-width: 480px){{
		.columnWrapper{{
			max-width:100% !important;
			width:100% !important;
		}}

}}	@media only screen and (max-width: 480px){{
		.mcnImage{{
			width:100% !important;
		}}

}}	@media only screen and (max-width: 480px){{
		.mcnShareContent,.mcnCaptionTopContent,.mcnCaptionBottomContent,.mcnTextContentContainer,.mcnBoxedTextContentContainer,.mcnImageGroupContentContainer,.mcnCaptionLeftTextContentContainer,.mcnCaptionRightTextContentContainer,.mcnCaptionLeftImageContentContainer,.mcnCaptionRightImageContentContainer,.mcnImageCardLeftTextContentContainer,.mcnImageCardRightTextContentContainer{{
			max-width:100% !important;
			width:100% !important;
		}}

}}	@media only screen and (max-width: 480px){{
		.mcnBoxedTextContentContainer{{
			min-width:100% !important;
		}}

}}	@media only screen and (max-width: 480px){{
		.mcnImageGroupContent{{
			padding:9px !important;
		}}

}}	@media only screen and (max-width: 480px){{
		.mcnCaptionLeftContentOuter .mcnTextContent,.mcnCaptionRightContentOuter .mcnTextContent{{
			padding-top:9px !important;
		}}

}}	@media only screen and (max-width: 480px){{
		.mcnImageCardTopImageContent,.mcnCaptionBlockInner .mcnCaptionTopContent:last-child .mcnTextContent{{
			padding-top:18px !important;
		}}

}}	@media only screen and (max-width: 480px){{
		.mcnImageCardBottomImageContent{{
			padding-bottom:9px !important;
		}}

}}	@media only screen and (max-width: 480px){{
		.mcnImageGroupBlockInner{{
			padding-top:0 !important;
			padding-bottom:0 !important;
		}}

}}	@media only screen and (max-width: 480px){{
		.mcnImageGroupBlockOuter{{
			padding-top:9px !important;
			padding-bottom:9px !important;
		}}

}}	@media only screen and (max-width: 480px){{
		.mcnTextContent,.mcnBoxedTextContentColumn{{
			padding-right:18px !important;
			padding-left:18px !important;
		}}

}}	@media only screen and (max-width: 480px){{
		.mcnImageCardLeftImageContent,.mcnImageCardRightImageContent{{
			padding-right:18px !important;
			padding-bottom:0 !important;
			padding-left:18px !important;
		}}

}}	@media only screen and (max-width: 480px){{
		.mcpreview-image-uploader{{
			display:none !important;
			width:100% !important;
		}}

}}	@media only screen and (max-width: 480px){{
		h1{{
			font-size:22px !important;
			line-height:125% !important;
		}}

}}	@media only screen and (max-width: 480px){{
		h2{{
			font-size:20px !important;
			line-height:125% !important;
		}}

}}	@media only screen and (max-width: 480px){{
		h3{{
			font-size:18px !important;
			line-height:125% !important;
		}}

}}	@media only screen and (max-width: 480px){{
		h4{{
			font-size:16px !important;
			line-height:150% !important;
		}}

}}	@media only screen and (max-width: 480px){{
		.mcnBoxedTextContentContainer .mcnTextContent,.mcnBoxedTextContentContainer .mcnTextContent p{{
			font-size:14px !important;
			line-height:150% !important;
		}}

}}	@media only screen and (max-width: 480px){{
		#templatePreheader{{
			display:block !important;
		}}

}}	@media only screen and (max-width: 480px){{
		#templatePreheader .mcnTextContent,#templatePreheader .mcnTextContent p{{
			font-size:14px !important;
			line-height:150% !important;
		}}

}}	@media only screen and (max-width: 480px){{
		#templateHeader .mcnTextContent,#templateHeader .mcnTextContent p{{
			font-size:16px !important;
			line-height:150% !important;
		}}

}}	@media only screen and (max-width: 480px){{
		#templateUpperBody .mcnTextContent,#templateUpperBody .mcnTextContent p{{
			font-size:16px !important;
			line-height:150% !important;
		}}

}}	@media only screen and (max-width: 480px){{
		#templateColumns .columnContainer .mcnTextContent,#templateColumns .columnContainer .mcnTextContent p{{
			font-size:16px !important;
			line-height:150% !important;
		}}

}}	@media only screen and (max-width: 480px){{
		#templateLowerBody .mcnTextContent,#templateLowerBody .mcnTextContent p{{
			font-size:16px !important;
			line-height:150% !important;
		}}

}}	@media only screen and (max-width: 480px){{
		#templateFooter .mcnTextContent,#templateFooter .mcnTextContent p{{
			font-size:14px !important;
			line-height:150% !important;
		}}

}}</style></head>
    <body style="height: 100%;margin: 0;padding: 0;width: 100%;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;background-color: #FAFAFA;">
        <center>
            <table align="center" border="0" cellpadding="0" cellspacing="0" height="100%" width="100%" id="bodyTable" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;height: 100%;margin: 0;padding: 0;width: 100%;background-color: #FAFAFA;">
                <tr>
                    <td align="center" valign="top" id="bodyCell" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;height: 100%;margin: 0;padding: 0;width: 100%;border-top: 0;">
                        <!-- BEGIN TEMPLATE // -->
                        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
                            <tr>
								<td align="center" valign="top" id="templatePreheader" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;background-color: #FAFAFA;border-top: 0;border-bottom: 0;padding-top: 9px;padding-bottom: 9px;">
									<!--[if gte mso 9]>
									<table align="center" border="0" cellspacing="0" cellpadding="0" width="600" style="width:600px;">
									<tr>
									<td align="center" valign="top" width="600" style="width:600px;">
									<![endif]-->
									<table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" class="templateContainer" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;max-width: 600px !important;">
										<tr>
                                			<td valign="top" class="preheaderContainer" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;"><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnTextBlock" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
    <tbody class="mcnTextBlockOuter">
        <tr>
            <td valign="top" class="mcnTextBlockInner" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">

                <table align="left" border="0" cellpadding="0" cellspacing="0" width="366" class="mcnTextContentContainer" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
                    <tbody><tr>

                        <td valign="top" class="mcnTextContent" style="padding-top: 9px;padding-left: 18px;padding-bottom: 9px;padding-right: 0;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;word-break: break-word;color: #656565;font-family: Helvetica;font-size: 12px;line-height: 150%;text-align: left;">

                            #CaptureYourTeam & Win exciting prizes
                        </td>
                    </tr>
                </tbody></table>

                <table align="right" border="0" cellpadding="0" cellspacing="0" width="197" class="mcnTextContentContainer" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
                    <tbody><tr>

                        <td valign="top" class="mcnTextContent" style="padding-top: 9px;padding-right: 18px;padding-bottom: 9px;padding-left: 0;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;word-break: break-word;color: #656565;font-family: Helvetica;font-size: 12px;line-height: 150%;text-align: left;">

                            <a href="http://www.corelogs.com/" target="_blank" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;color: #656565;font-weight: normal;text-decoration: underline;">View this email in your browser</a>
                        </td>
                    </tr>
                </tbody></table>

            </td>
        </tr>
    </tbody>
</table></td>
										</tr>
									</table>
									<!--[if gte mso 9]>
									</td>
									</tr>
									</table>
									<![endif]-->
								</td>
                            </tr>
							<tr>
								<td align="center" valign="top" id="templateHeader" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;background-color: #FFFFFF;border-top: 0;border-bottom: 0;padding-top: 9px;padding-bottom: 0;">
									<!--[if gte mso 9]>
									<table align="center" border="0" cellspacing="0" cellpadding="0" width="600" style="width:600px;">
									<tr>
									<td align="center" valign="top" width="600" style="width:600px;">
									<![endif]-->
									<table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" class="templateContainer" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;max-width: 600px !important;">
										<tr>
                                			<td valign="top" class="headerContainer" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;"><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnCaptionBlock" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
    <tbody class="mcnCaptionBlockOuter">
        <tr>
            <td class="mcnCaptionBlockInner" valign="top" style="padding: 9px;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">




<table border="0" cellpadding="0" cellspacing="0" class="mcnCaptionRightContentOuter" width="100%" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
    <tbody><tr>
        <td valign="top" class="mcnCaptionRightContentInner" style="padding: 0 9px;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
            <table align="left" border="0" cellpadding="0" cellspacing="0" class="mcnCaptionRightImageContentContainer" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
                <tbody><tr>
                    <td class="mcnCaptionRightImageContent" valign="top" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">



                        <img alt="" src="http://www.corelogs.com/images/thumbnails/corelogs_logo.jpg" width="176" style="max-width: 552px;border: 0;height: auto;outline: none;text-decoration: none;-ms-interpolation-mode: bicubic;vertical-align: bottom;" class="mcnImage">



                    </td>
                </tr>
            </tbody></table>
            <table class="mcnCaptionRightTextContentContainer" align="right" border="0" cellpadding="0" cellspacing="0" width="352" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
                <tbody><tr>
                    <td valign="top" class="mcnTextContent" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;word-break: break-word;color: #202020;font-family: Helvetica;font-size: 16px;line-height: 150%;text-align: left;">
                        <span style="font-size:22px">CoreLogs</span>.com is a platform for SAE related collegiate clubs to get connected to each other and the Engineers, experts & Industrialists across the world. Visit <a href="http://www.corelogs.com/forum/" target="_blank" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;color: #2BAADF;font-weight: normal;text-decoration: underline;">The Engineer's Forum</a> to ask & answer Technical questions.
                    </td>
                </tr>
            </tbody></table>
        </td>
    </tr>
</tbody></table>




            </td>
        </tr>
    </tbody>
</table></td>
										</tr>
									</table>
									<!--[if gte mso 9]>
									</td>
									</tr>
									</table>
									<![endif]-->
								</td>
                            </tr>
							<tr>
								<td align="center" valign="top" id="templateUpperBody" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;background-color: #FFFFFF;border-top: 0;border-bottom: 0;padding-top: 0;padding-bottom: 0;">
									<!--[if gte mso 9]>
									<table align="center" border="0" cellspacing="0" cellpadding="0" width="600" style="width:600px;">
									<tr>
									<td align="center" valign="top" width="600" style="width:600px;">
									<![endif]-->
									<table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" class="templateContainer" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;max-width: 600px !important;">
										<tr>
                                			<td valign="top" class="bodyContainer" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;"><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnTextBlock" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
    <tbody class="mcnTextBlockOuter">
        <tr>
            <td valign="top" class="mcnTextBlockInner" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">

                <table align="left" border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnTextContentContainer" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
                    <tbody><tr>

                        <td valign="top" class="mcnTextContent" style="padding-top: 9px;padding-right: 18px;padding-bottom: 9px;padding-left: 18px;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;word-break: break-word;color: #202020;font-family: Helvetica;font-size: 16px;line-height: 150%;text-align: left;">

                            <h1 style="display: block;margin: 0;padding: 0;color: #202020;font-family: Helvetica;font-size: 26px;font-style: normal;font-weight: bold;line-height: 125%;letter-spacing: normal;text-align: left;">Capture Your Team and win exciting prizes</h1>

<p style="margin: 10px 0;padding: 0;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;color: #202020;font-family: Helvetica;font-size: 16px;line-height: 150%;text-align: left;"><span style="font-size:22px; line-height:20.8px">CoreLogs</span><span style="line-height:20.8px">.com brings a facebook event </span><a class="_58cn" data-ft="{{"tn":"*N","type":104}}" href="https://www.facebook.com/hashtag/captureyourteam?source=feed_text&story_id=1635510520046599" style="color: #3B5998;cursor: pointer;text-decoration: none;font-family: helvetica, arial, sans-serif;font-size: 14px;line-height: 19.32px;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;font-weight: normal;"><span aria-label="hashtag" class="_58cl" style="color: #627AAD;">#</span><span class="_58cm">CAPTUREYOURTEAM?</span></a><span style="color: #141823;font-family: helvetica,arial,sans-serif;font-size: 14px;line-height: 19.32px;"> for the SAE related Teams across India. You send us a pic of your car, we upload it from our facebook page. The teams with maximum likes win exciting prizes. Visit our <a href="https://www.facebook.com/corelogs.page" target="_blank" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;color: #2BAADF;font-weight: normal;text-decoration: underline;">facebook page</a> for <a href="https://www.facebook.com/notes/corelogs/rules-and-regulations-for-online-event/1635293750068276" target="_blank" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;color: #2BAADF;font-weight: normal;text-decoration: underline;">details and rules</a>.<br>
You can send us the image at <a href="mailto:info@corelogs.com?subject=Paticipation%20in%20%23captureyourteam" target="_blank" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;color: #2BAADF;font-weight: normal;text-decoration: underline;">info@corelogs.com</a> by 30th November. <strong>The sooner the better.<br>
It is for Baja, Supra/ Formula student India, efficycle, supermileage Teams.</strong></span></p>

                        </td>
                    </tr>
                </tbody></table>

            </td>
        </tr>
    </tbody>
</table></td>
										</tr>
									</table>
									<!--[if gte mso 9]>
									</td>
									</tr>
									</table>
									<![endif]-->
								</td>
                            </tr>
							<tr>
								<td align="center" valign="top" id="templateColumns" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;background-color: #FFFFFF;border-top: 0;border-bottom: 0;padding-top: 0;padding-bottom: 0;">
									<table border="0" cellpadding="0" cellspacing="0" width="100%" class="templateContainer" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;max-width: 600px !important;">
                                        <tr>
                                            <td align="center" valign="top" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
												<!--[if gte mso 9]>
												<table align="center" border="0" cellspacing="0" cellpadding="0" width="600" style="width:600px;">
												<tr>
												<td align="center" valign="top" width="300" style="width:300px;">
												<![endif]-->
												<table align="left" border="0" cellpadding="0" cellspacing="0" width="300" class="columnWrapper" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
													<tr>
														<td valign="top" class="columnContainer" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;"><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnImageCardBlock" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
    <tbody class="mcnImageCardBlockOuter">
        <tr>
            <td class="mcnImageCardBlockInner" valign="top" style="padding-top: 9px;padding-right: 18px;padding-bottom: 9px;padding-left: 18px;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">

<table align="right" border="0" cellpadding="0" cellspacing="0" class="mcnImageCardBottomContent" width="100%" style="background-color: #404040;border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
    <tbody><tr>
        <td class="mcnImageCardBottomImageContent" align="left" valign="top" style="padding-top: 0px;padding-right: 0px;padding-bottom: 0;padding-left: 0px;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">



            <img alt="" src="http://www.corelogs.com/images/thumbnails/baja.JPG" width="264" style="max-width: 552px;border: 0;height: auto;outline: none;text-decoration: none;-ms-interpolation-mode: bicubic;vertical-align: bottom;" class="mcnImage">


        </td>
    </tr>
    <tr>
        <td class="mcnTextContent" valign="top" style="padding: 9px 18px;color: #F2F2F2;font-family: Helvetica;font-size: 14px;font-weight: normal;text-align: center;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;word-break: break-word;line-height: 150%;" width="246">
            BAja SAE India & Baja Student India
        </td>
    </tr>
</tbody></table>




            </td>
        </tr>
    </tbody>
</table></td>
													</tr>
												</table>
												<!--[if gte mso 9]>
												</td>
												<td align="center" valign="top" width="300" style="width:300px;">
												<![endif]-->
												<table align="left" border="0" cellpadding="0" cellspacing="0" width="300" class="columnWrapper" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
													<tr>
														<td valign="top" class="columnContainer" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;"><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnImageCardBlock" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
    <tbody class="mcnImageCardBlockOuter">
        <tr>
            <td class="mcnImageCardBlockInner" valign="top" style="padding-top: 9px;padding-right: 18px;padding-bottom: 9px;padding-left: 18px;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">

<table align="left" border="0" cellpadding="0" cellspacing="0" class="mcnImageCardBottomContent" width="100%" style="background-color: #404040;border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
    <tbody><tr>
        <td class="mcnImageCardBottomImageContent" align="left" valign="top" style="padding-top: 0px;padding-right: 0px;padding-bottom: 0;padding-left: 0px;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">



            <img alt="" src="http://www.corelogs.com/images/thumbnails/fsae.JPG" width="264" style="max-width: 552px;border: 0;height: auto;outline: none;text-decoration: none;-ms-interpolation-mode: bicubic;vertical-align: bottom;" class="mcnImage">


        </td>
    </tr>
    <tr>
        <td class="mcnTextContent" valign="top" style="padding: 9px 18px;color: #F2F2F2;font-family: Helvetica;font-size: 14px;font-weight: normal;text-align: center;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;word-break: break-word;line-height: 150%;" width="246">
            Supra SAE India & Formula Student India
        </td>
    </tr>
</tbody></table>




            </td>
        </tr>
    </tbody>
</table></td>
													</tr>
												</table>
												<!--[if gte mso 9]>
												</td>
												</tr>
												</table>
												<![endif]-->
											</td>
										</tr>
									</table>
								</td>
                            </tr>
							<tr>
								<td align="center" valign="top" id="templateLowerBody" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;background-color: #FFFFFF;border-top: 0;border-bottom: 2px solid #EAEAEA;padding-top: 0;padding-bottom: 9px;">
									<!--[if gte mso 9]>
									<table align="center" border="0" cellspacing="0" cellpadding="0" width="600" style="width:600px;">
									<tr>
									<td align="center" valign="top" width="600" style="width:600px;">
									<![endif]-->
									<table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" class="templateContainer" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;max-width: 600px !important;">
										<tr>
                                			<td valign="top" class="bodyContainer" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;"><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnTextBlock" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
    <tbody class="mcnTextBlockOuter">
        <tr>
            <td valign="top" class="mcnTextBlockInner" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">

                <table align="left" border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnTextContentContainer" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
                    <tbody><tr>

                        <td valign="top" class="mcnTextContent" style="padding-top: 9px;padding-right: 18px;padding-bottom: 9px;padding-left: 18px;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;word-break: break-word;color: #202020;font-family: Helvetica;font-size: 16px;line-height: 150%;text-align: left;">

                            Through this event we want to emphasize how important it is to bring a culture of sharing and open source movement in Core Segment of Engineering. Let's Speed up the pace of development by following the principle of open source movement & knowledge sharing.<br>
The IT industry & the startup world learnt about <strong>Lean</strong> from the Core Segment of Engineering. Now Its our chance to learn about <strong>Open Source Technology </strong>from them<strong>.<br>
Ask, Answer & Write on CoreLogs to help others and make your mark on internet.</strong>
                        </td>
                    </tr>
                </tbody></table>

            </td>
        </tr>
    </tbody>
</table><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnButtonBlock" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
    <tbody class="mcnButtonBlockOuter">
        <tr>
            <td style="padding-top: 0;padding-right: 18px;padding-bottom: 18px;padding-left: 18px;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;" valign="top" align="center" class="mcnButtonBlockInner">
                <table border="0" cellpadding="0" cellspacing="0" class="mcnButtonContentContainer" style="border-collapse: separate !important;border-radius: 3px;background-color: #2BAADF;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
                    <tbody>
                        <tr>
                            <td align="center" valign="middle" class="mcnButtonContent" style="font-family: Arial;font-size: 16px;padding: 15px;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
                                <a class="mcnButton " title="Visit CoreLogs" href="http://www.corelogs.com" target="_blank" style="font-weight: bold;letter-spacing: normal;line-height: 100%;text-align: center;text-decoration: none;color: #FFFFFF;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;display: block;">Visit CoreLogs</a>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </td>
        </tr>
    </tbody>
</table></td>
										</tr>
									</table>
									<!--[if gte mso 9]>
									</td>
									</tr>
									</table>
									<![endif]-->
								</td>
                            </tr>
                            <tr>
								<td align="center" valign="top" id="templateFooter" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;background-color: #FAFAFA;border-top: 0;border-bottom: 0;padding-top: 9px;padding-bottom: 9px;">
									<!--[if gte mso 9]>
									<table align="center" border="0" cellspacing="0" cellpadding="0" width="600" style="width:600px;">
									<tr>
									<td align="center" valign="top" width="600" style="width:600px;">
									<![endif]-->
									<table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" class="templateContainer" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;max-width: 600px !important;">
										<tr>
                                			<td valign="top" class="footerContainer" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;"><table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnFollowBlock" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
    <tbody class="mcnFollowBlockOuter">
        <tr>
            <td align="center" valign="top" style="padding: 9px;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;" class="mcnFollowBlockInner">
                <table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnFollowContentContainer" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
    <tbody><tr>
        <td align="center" style="padding-left: 9px;padding-right: 9px;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
            <table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnFollowContent" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
                <tbody><tr>
                    <td align="center" valign="top" style="padding-top: 9px;padding-right: 9px;padding-left: 9px;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
                        <table border="0" cellpadding="0" cellspacing="0" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
                            <tbody><tr>
                                <td valign="top" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
                                    <!--[if mso]>
                                    <table align="left" border="0" cellspacing="0" cellpadding="0" width="524">
                                    <tr>
                                    <td align="left" valign="top" width="524">
                                    <![endif]-->



                                            <table align="left" border="0" cellpadding="0" cellspacing="0" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
                                                <tbody><tr>
                                                    <td valign="top" style="padding-right: 10px;padding-bottom: 9px;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;" class="mcnFollowContentItemContainer">
                                                        <table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnFollowContentItem" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
                                                            <tbody><tr>
                                                                <td align="left" valign="middle" style="padding-top: 5px;padding-right: 10px;padding-bottom: 5px;padding-left: 9px;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
                                                                    <table align="left" border="0" cellpadding="0" cellspacing="0" width="" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
                                                                        <tbody><tr>

                                                                                <td align="center" valign="middle" width="24" class="mcnFollowIconContent" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
                                                                                    <a href="https://twitter.com/Corelogstwt" target="_blank" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;"><img src="http://cdn-images.mailchimp.com/icons/social-block-v2/color-twitter-48.png" style="display: block;border: 0;height: auto;outline: none;text-decoration: none;-ms-interpolation-mode: bicubic;" height="24" width="24" class=""></a>
                                                                                </td>


                                                                        </tr>
                                                                    </tbody></table>
                                                                </td>
                                                            </tr>
                                                        </tbody></table>
                                                    </td>
                                                </tr>
                                            </tbody></table>




                                            <table align="left" border="0" cellpadding="0" cellspacing="0" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
                                                <tbody><tr>
                                                    <td valign="top" style="padding-right: 10px;padding-bottom: 9px;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;" class="mcnFollowContentItemContainer">
                                                        <table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnFollowContentItem" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
                                                            <tbody><tr>
                                                                <td align="left" valign="middle" style="padding-top: 5px;padding-right: 10px;padding-bottom: 5px;padding-left: 9px;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
                                                                    <table align="left" border="0" cellpadding="0" cellspacing="0" width="" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
                                                                        <tbody><tr>

                                                                                <td align="center" valign="middle" width="24" class="mcnFollowIconContent" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
                                                                                    <a href="https://www.facebook.com/corelogs.page" target="_blank" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;"><img src="http://cdn-images.mailchimp.com/icons/social-block-v2/color-facebook-48.png" style="display: block;border: 0;height: auto;outline: none;text-decoration: none;-ms-interpolation-mode: bicubic;" height="24" width="24" class=""></a>
                                                                                </td>


                                                                        </tr>
                                                                    </tbody></table>
                                                                </td>
                                                            </tr>
                                                        </tbody></table>
                                                    </td>
                                                </tr>
                                            </tbody></table>




                                            <table align="left" border="0" cellpadding="0" cellspacing="0" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
                                                <tbody><tr>
                                                    <td valign="top" style="padding-right: 0;padding-bottom: 9px;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;" class="mcnFollowContentItemContainer">
                                                        <table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnFollowContentItem" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
                                                            <tbody><tr>
                                                                <td align="left" valign="middle" style="padding-top: 5px;padding-right: 10px;padding-bottom: 5px;padding-left: 9px;mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
                                                                    <table align="left" border="0" cellpadding="0" cellspacing="0" width="" style="border-collapse: collapse;mso-table-lspace: 0pt;mso-table-rspace: 0pt;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
                                                                        <tbody><tr>

                                                                                <td align="center" valign="middle" width="24" class="mcnFollowIconContent" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;">
                                                                                    <a href="http://www.corelogs.com" target="_blank" style="mso-line-height-rule: exactly;-ms-text-size-adjust: 100%;-webkit-text-size-adjust: 100%;"><img src="http://cdn-images.mailchimp.com/icons/social-block-v2/color-link-48.png" style="display: block;border: 0;height: auto;outline: none;text-decoration: none;-ms-interpolation-mode: bicubic;" height="24" width="24" class=""></a>
                                                                                </td>


                                                                        </tr>
                                                                    </tbody></table>
                                                                </td>
                                                            </tr>
                                                        </tbody></table>
                                                    </td>
                                                </tr>
                                            </tbody></table>


                                    <!--[if mso]>
                                    </td>
                                    </tr>
                                    </table>
                                    <![endif]-->
                                </td>
                            </tr>
                        </tbody></table>
                    </td>
                </tr>
            </tbody></table>
        </td>
    </tr>
</tbody></table>

            </td>
        </tr>
    </tbody>
</table></td>
										</tr>
									</table>
									<!--[if gte mso 9]>
									</td>
									</tr>
									</table>
									<![endif]-->
								</td>
                            </tr>
                        </table>
                        <!-- // END TEMPLATE -->
                    </td>
                </tr>
            </table>
        </center>
    </body>
</html>
Thanks
SP
'''

