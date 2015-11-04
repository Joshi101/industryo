from django.shortcuts import render, redirect, render_to_response, RequestContext
from nodes.models import Node
from nodes.forms import UploadImageForm
from userprofile.models import UserProfile
from workplace.models import Workplace
from forum.models import Question
from tags.models import Tags
from products.models import Products
from itertools import chain
from allauth.account.forms import AddEmailForm, ChangePasswordForm
from allauth.account.forms import LoginForm, ResetPasswordKeyForm
from allauth.account.forms import ResetPasswordForm, SetPasswordForm, SignupForm, UserTokenForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from operator import attrgetter
from activities.models import Notification
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from home import tasks
from django.core.mail import EmailMultiAlternatives


def home(request):
    if request.user.is_authenticated():
        user = request.user
        if user.userprofile.primary_workplace:
            profile = UserProfile.objects.select_related('primary_workplace__workplace_type').get(user=user)
            workplace = profile.primary_workplace
            t = workplace.workplace_type
            if t == 'A':
                related_node = Node.feed.filter(w_type__in=['A', 'B']).select_related('user__userprofile')
                question = Question.objects.filter(user__userprofile__primary_workplace__workplace_type=t).select_related('user__userprofile')
            elif t == 'B':
                related_node = Node.feed.filter(w_type__in=['A', 'B']).select_related('user__userprofile')
                question = Question.objects.filter(user__userprofile__primary_workplace__workplace_type=t).select_related('user__userprofile')
            elif t == 'C':
                related_node = Node.feed.filter(w_type__in=['C', 'O']).select_related('user__userprofile')
                question = Question.objects.filter(user__userprofile__primary_workplace__workplace_type=t).select_related('user__userprofile')
            else:  # t == 'O':
                related_node = Node.feed.filter(w_type__in=['C', 'O']).select_related('user__userprofile')
                question = Question.objects.filter(user__userprofile__primary_workplace__workplace_type=t).select_related('user__userprofile')
            all_result_list = sorted(
                chain(related_node, question),
                key=attrgetter('date'), reverse=True)
            paginator = Paginator(all_result_list, 5)
            page = request.GET.get('page')
            try:
                result_list = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                result_list = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                return
                # result_list = paginator.page(paginator.num_pages)
            if page:
                return render(request, 'nodes/five_nodes.html', {'result_list': result_list})
            else:
                return render(request, 'home.html', {'result_list': result_list, 'workplace': workplace, 'feed_img_form': UploadImageForm()})
        else:
            return redirect('/set/')
    else:
        return render(request, 'cover.html', {'form_signup': SignupForm(), 'form_login': LoginForm()})


def home_right(request):
    questions = Question.objects.all().order_by('?')[:5]

    if request.user.is_authenticated():

        if request.user.userprofile.primary_workplace:
            # profile = UserProfile.objects.select_related('primary_workplace__workplace_type').get(user=user)
            # workplace = profile.primary_workplace
            t = request.user.userprofile.primary_workplace.workplace_type
            workplaces = Workplace.objects.filter(workplace_type=t).order_by('?')[:5]           # change it soon
        else:
            workplaces = Workplace.objects.all().order_by('?')[:5]
    else:
        workplaces = Workplace.objects.all().order_by('?')[:5]
    return render(request, 'snippets/right/home_right.html', {'workplaces': workplaces, 'questions': questions})


def home_right_down(request):
    questions = Question.objects.all().order_by('-last_active')[:5]
    return render(request, 'snippets/right/home_right_down.html', {'questions': questions})


def people(request):
    all_user = UserProfile.objects.all()
    paginator = Paginator(all_user, 50)
    page = request.GET.get('page')
    try:
        people = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        people = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        people = paginator.page(paginator.num_pages)

    return render_to_response('sitemap/sitemap_user.html', {"list": people, "what": 'user'})


def workplaces(request):
    all_objects = Workplace.objects.all()
    paginator = Paginator(all_objects, 50)
    page = request.GET.get('page')
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        objects = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        objects = paginator.page(paginator.num_pages)

    return render_to_response('sitemap/sitemap_user.html', {"list": objects, "what": 'workplace'})


def questions(request):
    all_objects = Question.objects.all()
    paginator = Paginator(all_objects, 20)
    page = request.GET.get('page')
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        objects = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        objects = paginator.page(paginator.num_pages)

    return render_to_response('sitemap/sitemap_user.html', {"list": objects, "what": 'question'})


def tags(request):
    all_objects = Tags.objects.all()
    paginator = Paginator(all_objects, 50)
    page = request.GET.get('page')
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        objects = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        objects = paginator.page(paginator.num_pages)

    return render_to_response('sitemap/sitemap_user.html', {"list": objects, "what": 'tag'})


def articles(request):
    all_objects = Node.article.all()
    paginator = Paginator(all_objects, 50)
    page = request.GET.get('page')
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        objects = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        objects = paginator.page(paginator.num_pages)

    return render_to_response('sitemap/sitemap_user.html', {"list": objects, "what": 'article'})


def products(request):
    all_objects = Products.objects.all()
    paginator = Paginator(all_objects, 50)
    page = request.GET.get('page')
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        objects = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        objects = paginator.page(paginator.num_pages)

    return render_to_response('sitemap/sitemap_user.html', {"list": objects, "what": 'product'})


def about(request):
    return render_to_response('about.html')


def search(request):
    if 'q' in request.GET:
        return redirect('/search/')
    else:
        return render(request, 'search/search.html')


@login_required
def send_test(request):
    tasks.test_mail(1, n=17)
    return redirect('/')

@login_required
def send_an_email(request):
    # userprofiles = UserProfile.objects.filter(primary_workplace__workplace_type='C')
    # for u in userprofiles:
    #     tasks.luck(u.id, n=16)
    # return redirect('/')


    subject, from_email, to = 'hello', 'sp@corelogs.com', 'sprksh.j@gmail.com'
    text_content = 'This is an important message.'
    content = '''
Hi {0},

<div id=":38" class="ii gt m150d38c55f7790a6 adP adO"><div id=":39" class="a3s" style="overflow: hidden;"><div dir="ltr"><div><div style="overflow:hidden"><u></u>










    <div style="min-height:100%;margin:0;padding:0;width:100%;background-color:#fafafa">
        <center>
            <table align="center" border="0" cellpadding="0" cellspacing="0" height="100%" width="100%" style="border-collapse:collapse;height:100%;margin:0;padding:0;width:100%;background-color:#fafafa">
                <tbody><tr>
                    <td align="center" valign="top" style="height:100%;margin:0;padding:0;width:100%;border-top:0">

                        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse:collapse">
                            <tbody><tr>
								<td align="center" valign="top" style="background-color:#fafafa;border-top:0;border-bottom:0;padding-top:9px;padding-bottom:9px">

									<table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse:collapse;max-width:600px!important">
										<tbody><tr>
                                			<td valign="top"><table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse:collapse">
    <tbody>
        <tr>
            <td valign="top">

                <table align="left" border="0" cellpadding="0" cellspacing="0" width="366" style="border-collapse:collapse">
                    <tbody><tr>

                        <td valign="top" style="padding-top:9px;padding-left:18px;padding-bottom:9px;padding-right:0;word-break:break-word;color:#656565;font-family:Helvetica;font-size:12px;line-height:150%;text-align:left">

                            #CaptureYourTeam &amp; Win exciting prizes
                        </td>
                    </tr>
                </tbody></table>

                <table align="right" border="0" cellpadding="0" cellspacing="0" width="197" style="border-collapse:collapse">
                    <tbody><tr>

                        <td valign="top" style="padding-top:9px;padding-right:18px;padding-bottom:9px;padding-left:0;word-break:break-word;color:#656565;font-family:Helvetica;font-size:12px;line-height:150%;text-align:left">

                            <a href="http://www.corelogs.com" style="color:#656565;font-weight:normal;text-decoration:underline" target="_blank">View this email in your browser</a>
                        </td>
                    </tr>
                </tbody></table>

            </td>
        </tr>
    </tbody>
</table></td>
										</tr>
									</tbody></table>

								</td>
                            </tr>
							<tr>
								<td align="center" valign="top" style="background-color:#ffffff;border-top:0;border-bottom:0;padding-top:9px;padding-bottom:0">

									<table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse:collapse;max-width:600px!important">
										<tbody><tr>
                                			<td valign="top"><table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse:collapse">
    <tbody>
        <tr>
            <td valign="top" style="padding:9px">




<table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse:collapse">
    <tbody><tr>
        <td valign="top" style="padding:0 9px">
            <table align="left" border="0" cellpadding="0" cellspacing="0" style="border-collapse:collapse">
                <tbody><tr>
                    <td valign="top">



                        <img alt="" src="https://ci3.googleusercontent.com/proxy/N7-TZc8O2w_5V9_jSOkNobIsx8k2fr_IqVmvYy3NOZLT5UUE_dmIwAssx3W7uDV7wcogNruJKAq9ZTLSqvdw5lD4JvwXzcEpIBdiNc7IsaAI=s0-d-e1-ft#http://www.corelogs.com/images/thumbnails/corelogs_logo.jpg" width="176" style="max-width:552px;border:0;min-height:auto;outline:none;text-decoration:none;vertical-align:bottom" class="CToWUd a6T" tabindex="0"><div class="a6S" dir="ltr" style="opacity: 0.01; left: 146px; top: 250px;"><div id=":ot" class="T-I J-J5-Ji aQv T-I-ax7 L3 a5q" role="button" tabindex="0" aria-label="Download attachment " data-tooltip-class="a1V" data-tooltip="Download"><div class="aSK J-J5-Ji aYr"></div></div></div><div dir="ltr"><div><div></div></div></div>



                    </td>
                </tr>
            </tbody></table>
            <table align="right" border="0" cellpadding="0" cellspacing="0" width="352" style="border-collapse:collapse">
                <tbody><tr>
                    <td valign="top" style="word-break:break-word;color:#202020;font-family:Helvetica;font-size:16px;line-height:150%;text-align:left">
                        <span style="font-size:22px">CoreLogs</span>.com is a platform for SAE related collegiate clubs to get connected to each other and the Engineers, experts &amp; Industrialists across the world. Visit <a href="http://www.corelogs.com/forum/" style="color:#2baadf;font-weight:normal;text-decoration:underline" target="_blank">The Engineer's Forum</a> to ask &amp; answer Technical questions.
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
									</tbody></table>

								</td>
                            </tr>
							<tr>
								<td align="center" valign="top" style="background-color:#ffffff;border-top:0;border-bottom:0;padding-top:0;padding-bottom:0">

									<table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse:collapse;max-width:600px!important">
										<tbody><tr>
                                			<td valign="top"><table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse:collapse">
    <tbody>
        <tr>
            <td valign="top">

                <table align="left" border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse:collapse">
                    <tbody><tr>

                        <td valign="top" style="padding-top:9px;padding-right:18px;padding-bottom:9px;padding-left:18px;word-break:break-word;color:#202020;font-family:Helvetica;font-size:16px;line-height:150%;text-align:left">

                            <h1 style="display:block;margin:0;padding:0;color:#202020;font-family:Helvetica;font-size:26px;font-style:normal;font-weight:bold;line-height:125%;letter-spacing:normal;text-align:left">Capture Your Team and win exciting prizes</h1>

<p style="margin:10px 0;padding:0;color:#202020;font-family:Helvetica;font-size:16px;line-height:150%;text-align:left"><span style="font-size:22px;line-height:20.8px">CoreLogs</span><span style="line-height:20.8px">.com brings a facebook event&nbsp;</span><a href="https://www.facebook.com/hashtag/captureyourteam" style="color:#3b5998;text-decoration:none;font-family:helvetica,arial,sans-serif;font-size:14px;line-height:19.32px;font-weight:normal" target="_blank"><span style="color:#627aad">#</span><span>CAPTUREYOURTEAM&#8236;</span></a><span style="color:#141823;font-family:helvetica,arial,sans-serif;font-size:14px;line-height:19.32px">&nbsp;for the SAE related Teams across India. You send us a pic of your car, we upload it from our facebook page. The teams with maximum likes win exciting prizes. Visit our <a href="https://www.facebook.com/corelogs.page" style="color:#2baadf;font-weight:normal;text-decoration:underline" target="_blank">facebook page</a> for <a href="https://www.facebook.com/notes/corelogs/rules-and-regulations-for-online-event/1635293750068276" style="color:#2baadf;font-weight:normal;text-decoration:underline" target="_blank">details and rules</a>.<br>
You can send us the image at <a href="mailto:info@corelogs.com?subject=Paticipation%20in%20%23captureyourteam" style="color:#2baadf;font-weight:normal;text-decoration:underline" target="_blank">info@corelogs.com</a>&nbsp;by <span><span><span class="aBn" data-term="goog_724187764" tabindex="0"><span class="aQJ">30th November</span></span></span></span>. <strong>The sooner the better.<br>
It is for Baja, Supra/ Formula student India, efficycle, supermileage Teams.</strong></span></p>

                        </td>
                    </tr>
                </tbody></table>

            </td>
        </tr>
    </tbody>
</table></td>
										</tr>
									</tbody></table>

								</td>
                            </tr>
							<tr>
								<td align="center" valign="top" style="background-color:#ffffff;border-top:0;border-bottom:0;padding-top:0;padding-bottom:0">
									<table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse:collapse;max-width:600px!important">
                                        <tbody><tr>
                                            <td align="center" valign="top">

												<table align="left" border="0" cellpadding="0" cellspacing="0" width="300" style="border-collapse:collapse">
													<tbody><tr>
														<td valign="top"><table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse:collapse">
    <tbody>
        <tr>
            <td valign="top" style="padding-top:9px;padding-right:18px;padding-bottom:9px;padding-left:18px">

<table align="right" border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color:#404040;border-collapse:collapse">
    <tbody><tr>
        <td align="left" valign="top" style="padding-top:0px;padding-right:0px;padding-bottom:0;padding-left:0px">



            <img alt="" src="https://ci6.googleusercontent.com/proxy/KHj0gpr85lkju1gNNrLXnM6T5u1ZVKhdlVyXXMxc53jEBzXQtGQGI80MrINtM37HNY_DjjfvhsO9ZtTUUryU_AZO5Any2d_N=s0-d-e1-ft#http://www.corelogs.com/images/thumbnails/baja.JPG" width="264" style="max-width:552px;border:0;min-height:auto;outline:none;text-decoration:none;vertical-align:bottom" class="CToWUd"><div dir="ltr"><div title="Download"><div></div></div></div>


        </td>
    </tr>
    <tr>
        <td valign="top" style="padding:9px 18px;color:#f2f2f2;font-family:Helvetica;font-size:14px;font-weight:normal;text-align:center;word-break:break-word;line-height:150%" width="246">
            BAja SAE India &amp; Baja Student India
        </td>
    </tr>
</tbody></table>




            </td>
        </tr>
    </tbody>
</table></td>
													</tr>
												</tbody></table>

												<table align="left" border="0" cellpadding="0" cellspacing="0" width="300" style="border-collapse:collapse">
													<tbody><tr>
														<td valign="top"><table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse:collapse">
    <tbody>
        <tr>
            <td valign="top" style="padding-top:9px;padding-right:18px;padding-bottom:9px;padding-left:18px">

<table align="left" border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color:#404040;border-collapse:collapse">
    <tbody><tr>
        <td align="left" valign="top" style="padding-top:0px;padding-right:0px;padding-bottom:0;padding-left:0px">



            <img alt="" src="https://ci3.googleusercontent.com/proxy/q12EOLFPRq7w7_OKaNMjZ8VeeWOUqOkuqODfmnlAUWJ-jeqnhG1qNoWXFplTKzDNWGKFwRYheWet6tRUK2BlH98TvSPX9oNI=s0-d-e1-ft#http://www.corelogs.com/images/thumbnails/fsae.JPG" width="264" style="max-width:552px;border:0;min-height:auto;outline:none;text-decoration:none;vertical-align:bottom" class="CToWUd"><div dir="ltr"><div title="Download"><div></div></div></div>


        </td>
    </tr>
    <tr>
        <td valign="top" style="padding:9px 18px;color:#f2f2f2;font-family:Helvetica;font-size:14px;font-weight:normal;text-align:center;word-break:break-word;line-height:150%" width="246">
            Supra SAE India &amp; Formula Student India
        </td>
    </tr>
</tbody></table>




            </td>
        </tr>
    </tbody>
</table></td>
													</tr>
												</tbody></table>

											</td>
										</tr>
									</tbody></table>
								</td>
                            </tr>
							<tr>
								<td align="center" valign="top" style="background-color:#ffffff;border-top:0;border-bottom:2px solid #eaeaea;padding-top:0;padding-bottom:9px">

									<table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse:collapse;max-width:600px!important">
										<tbody><tr>
                                			<td valign="top"><table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse:collapse">
    <tbody>
        <tr>
            <td valign="top">

                <table align="left" border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse:collapse">
                    <tbody><tr>

                        <td valign="top" style="padding-top:9px;padding-right:18px;padding-bottom:9px;padding-left:18px;word-break:break-word;color:#202020;font-family:Helvetica;font-size:16px;line-height:150%;text-align:left">

                            Through this event we want to emphasize how important it is to bring a culture of sharing and open source movement in Core Segment of Engineering. Let's Speed up the pace of development by following the principle of open source movement &amp; knowledge sharing.<br>
The IT industry &amp; the startup world learnt about <strong>Lean</strong>&nbsp;from the Core Segment of Engineering. Now Its our chance to learn about <strong>Open Source Technology </strong>from them<strong>.<br>
Ask, Answer &amp; Write on CoreLogs to help others and make your mark on internet.</strong>
                        </td>
                    </tr>
                </tbody></table>

            </td>
        </tr>
    </tbody>
</table><table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse:collapse">
    <tbody>
        <tr>
            <td style="padding-top:0;padding-right:18px;padding-bottom:18px;padding-left:18px" valign="top" align="center">
                <table border="0" cellpadding="0" cellspacing="0" style="border-collapse:separate!important;border-radius:3px;background-color:#2baadf">
                    <tbody>
                        <tr>
                            <td align="center" valign="middle" style="font-family:Arial;font-size:16px;padding:15px">
                                <a title="Visit CoreLogs" href="http://www.corelogs.com" style="font-weight:bold;letter-spacing:normal;line-height:100%;text-align:center;text-decoration:none;color:#ffffff;display:block" target="_blank">Visit CoreLogs</a>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </td>
        </tr>
    </tbody>
</table></td>
										</tr>
									</tbody></table>

								</td>
                            </tr>
                            <tr>
								<td align="center" valign="top" style="background-color:#fafafa;border-top:0;border-bottom:0;padding-top:9px;padding-bottom:9px">

									<table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse:collapse;max-width:600px!important">
										<tbody><tr>
                                			<td valign="top"><table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse:collapse">
    <tbody>
        <tr>
            <td align="center" valign="top" style="padding:9px">
                <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse:collapse">
    <tbody><tr>
        <td align="center" style="padding-left:9px;padding-right:9px">
            <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse:collapse">
                <tbody><tr>
                    <td align="center" valign="top" style="padding-top:9px;padding-right:9px;padding-left:9px">
                        <table border="0" cellpadding="0" cellspacing="0" style="border-collapse:collapse">
                            <tbody><tr>
                                <td valign="top">




                                            <table align="left" border="0" cellpadding="0" cellspacing="0" style="border-collapse:collapse">
                                                <tbody><tr>
                                                    <td valign="top" style="padding-right:10px;padding-bottom:9px">
                                                        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse:collapse">
                                                            <tbody><tr>
                                                                <td align="left" valign="middle" style="padding-top:5px;padding-right:10px;padding-bottom:5px;padding-left:9px">
                                                                    <table align="left" border="0" cellpadding="0" cellspacing="0" width="" style="border-collapse:collapse">
                                                                        <tbody><tr>

                                                                                <td align="center" valign="middle" width="24">
                                                                                    <a href="https://twitter.com/Corelogstwt" target="_blank"><img src="https://ci5.googleusercontent.com/proxy/-SgR5D3-bPp1julTBdSE5457JLji6LNVwzZc_IzhWv_glCJmaIYrbdmJKf7oglfkeHHhMOEnTfkjdEFyTdW4nZ7I9uQz-CPztcyuJwCec3wpBJjvTFOFzAkhm_xj1bBX=s0-d-e1-ft#http://cdn-images.mailchimp.com/icons/social-block-v2/color-twitter-48.png" style="display:block;border:0;min-height:auto;outline:none;text-decoration:none" height="24" width="24" class="CToWUd"></a>
                                                                                </td>


                                                                        </tr>
                                                                    </tbody></table>
                                                                </td>
                                                            </tr>
                                                        </tbody></table>
                                                    </td>
                                                </tr>
                                            </tbody></table>




                                            <table align="left" border="0" cellpadding="0" cellspacing="0" style="border-collapse:collapse">
                                                <tbody><tr>
                                                    <td valign="top" style="padding-right:10px;padding-bottom:9px">
                                                        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse:collapse">
                                                            <tbody><tr>
                                                                <td align="left" valign="middle" style="padding-top:5px;padding-right:10px;padding-bottom:5px;padding-left:9px">
                                                                    <table align="left" border="0" cellpadding="0" cellspacing="0" width="" style="border-collapse:collapse">
                                                                        <tbody><tr>

                                                                                <td align="center" valign="middle" width="24">
                                                                                    <a href="https://www.facebook.com/corelogs.page" target="_blank"><img src="https://ci4.googleusercontent.com/proxy/X9MqCnSCvb5f1PshSVntsSqqm9dNg_ie7HbGsGn_ezsyhoBi1KL0re94Q0I4KPY2mGVpcW3dKRZwm_0bekmhL_IFCF7C82_1xXG2ZkrezDWf6kPh_gik805bm8zRcbMSMw=s0-d-e1-ft#http://cdn-images.mailchimp.com/icons/social-block-v2/color-facebook-48.png" style="display:block;border:0;min-height:auto;outline:none;text-decoration:none" height="24" width="24" class="CToWUd"></a>
                                                                                </td>


                                                                        </tr>
                                                                    </tbody></table>
                                                                </td>
                                                            </tr>
                                                        </tbody></table>
                                                    </td>
                                                </tr>
                                            </tbody></table>




                                            <table align="left" border="0" cellpadding="0" cellspacing="0" style="border-collapse:collapse">
                                                <tbody><tr>
                                                    <td valign="top" style="padding-right:0;padding-bottom:9px">
                                                        <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse:collapse">
                                                            <tbody><tr>
                                                                <td align="left" valign="middle" style="padding-top:5px;padding-right:10px;padding-bottom:5px;padding-left:9px">
                                                                    <table align="left" border="0" cellpadding="0" cellspacing="0" width="" style="border-collapse:collapse">
                                                                        <tbody><tr>

                                                                                <td align="center" valign="middle" width="24">
                                                                                    <a href="http://www.corelogs.com" target="_blank"><img src="https://ci3.googleusercontent.com/proxy/_uFbA8j5252fdnk4T1_dJcIe3YicShHtrxPXTNzgU81-5pFJl2KE13IBBm4-vmLNjsIyoC7sNVtQSpq--CaF3PHuhb6igzEEPH4WYLOOxYKIPOBarWCqgaZCobMK=s0-d-e1-ft#http://cdn-images.mailchimp.com/icons/social-block-v2/color-link-48.png" style="display:block;border:0;min-height:auto;outline:none;text-decoration:none" height="24" width="24" class="CToWUd"></a>
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
</table><table border="0" cellpadding="0" cellspacing="0" width="100%" style="min-width:100%;border-collapse:collapse;table-layout:fixed!important">
    <tbody>
        <tr>
            <td style="min-width:100%;padding:10px 18px 25px">
                <table border="0" cellpadding="0" cellspacing="0" width="100%" style="min-width:100%;border-top-width:2px;border-top-style:solid;border-top-color:#eeeeee;border-collapse:collapse">
                    <tbody><tr>
                        <td>
                            <span></span>
                        </td>
                    </tr>
                </tbody></table>

            </td>
        </tr>
    </tbody>
</table><table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse:collapse">

</table></td>
										</tr>
									</tbody></table>

								</td>
                            </tr>
                        </tbody></table>

                    </td>
                </tr>
            </tbody></table>
        </center>
    <img src="https://ci4.googleusercontent.com/proxy/ct_zxr3LLMPnfSlsneOV1ereoYzjdduwA2RTmFMy9NTI7jm3w67yco9WgoF37MpqftUaztQuky3YwkQ5JQTeTs5ydXm0aosjZdqBXPae5kdelA8Al1shjP5iZ3wQa9o4uI0OjI_wfl6slMWH0lJvDeQmhVnph5SLNkuftui0zxg=s0-d-e1-ft#http://corelogs.us12.list-manage.com/track/open.php?u=f4abfd921eb96255e46134f8f&amp;id=e5d3fc15c2&amp;e=965faa2986" height="1" width="1" class="CToWUd"></div><div></div><div>
</div></div></div><br clear="all"><div><div><div dir="ltr"><div><b>--<br>Surya Prakash.<br>Founder</b></div><div><a href="http://www.corelogs.com" target="_blank"><b>CoreLogs</b></a><div class="yj6qo"></div><div class="adL"><br><br></div></div></div></div></div><div class="adL">
</div></div><div class="adL">
</div></div></div>
'''
    html_content = content.format('Ram')
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    return redirect('/')
    # send_mail('CoreLogs- Set your Workplace', '<p>This is an <strong>important</strong> message.</p>', 'sp@corelogs.com', ['sprksh.j@gmail.com'])
    # return redirect('/')
    # if request.user.is_authenticated():
    #     # userprofiles = UserProfile.objects.filter(primary_workplace__workplace_type='C')
    #     users = User.objects.filter(id__lte=2)
    #     for user in users:
    #         # user = userprofile.user
    #         tasks.bhakk(user.id, n=15)
    #
    #     return redirect('/sitemap')
    # else:
    #     return redirect('/')


def send_set_wp_email(request):

    if request.user.is_authenticated():
        users = User.objects.all()
        for user in users:
            if not user.userprofile.primary_workplace:
                user_email = user.email
                if user.first_name:
                    name = user.get_full_name()
                else:
                    name = user.username
                template = u'''Hi {0},

Did you check www.corelogs.com ? We are getting great questions and answers on our forum. and we need people who can answer.

You have still not set your workplace till now.
To see optimized content, you should tell us where do you work or study.

Thanks & Regards

Surya Prakash
CoreLogs
'''
                content = template.format(name)
                try:
                    send_mail('CoreLogs- Set your Workplace', content, 'site.corelogs@gmail.com', [user_email])
                except Exception:
                    pass
        return redirect('/kabira')
    else:
        return redirect('/rahima')

from django.shortcuts import render_to_response
from django.template import RequestContext


def handler404(request):
    response = render_to_response('404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response


def handler500(request):
    response = render_to_response('500.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response


template2 = '''
<div style="margin:0;padding:0;min-width:100%;background-color:#e7f5f8">

    <center style="display:table;table-layout:fixed;width:100%;min-width:620px;background-color:#e7f5f8">
      <table style="border-collapse:collapse;border-spacing:0;font-size:11px;line-height:17px;width:100%">
        <tbody><tr>
          <td style="padding:9px;vertical-align:top;font-family:Cabin,Avenir,sans-serif;color:#93a6ad;text-align:left;width:50%;background-color:#d8eaee">
            <div>CoreLogs Invites all the people from various Baja &amp; Formula Teams to the biggest platform for them</div>
          </td>
          <td style="padding:9px;vertical-align:top;font-family:Cabin,Avenir,sans-serif;color:#93a6ad;text-align:right;width:50%;background-color:#cfe5ea">
            No Images? <a style="font-weight:700;letter-spacing:0.01em;text-decoration:none;color:#93a6ad" href="http://industrylogger.cmail2.com/t/i-e-tjuhill-l-k/" target="_blank">Click here</a>
          </td>
        </tr>
      </tbody></table>


          <table style="border-collapse:collapse;border-spacing:0;width:100%">
            <tbody><tr>
              <td style="padding:0;vertical-align:top" align="center">
                <table style="border-collapse:collapse;border-spacing:0;Margin-left:auto;Margin-right:auto;background-color:#ffffff;width:600px;table-layout:fixed">
                  <tbody><tr>
                    <td style="padding:0;vertical-align:top;text-align:left">

            <div style="font-size:12px;font-style:normal;font-weight:400;Margin-bottom:0;Margin-top:0;font-family:Cabin,Avenir,sans-serif;color:#8e8e8e" align="center">
              <a href="http://industrylogger.cmail2.com/t/i-i-tjuhill-l-r/" target="_blank"><img style="border:0;display:block;max-width:900px" src="https://ci3.googleusercontent.com/proxy/1wNFNZKlIknsi5MuGQ4_TWto5I5-FnYthlDIsNc7JMFeaa3sqT5LU5V6J5q7VO9nOIg5YJJyYzPBnJWP3iS_jmKICWCYpokPK1qYaHLb8vcaC1aBe9fs6scPe6TmFV5_=s0-d-e1-ft#http://i1.cmail2.com/ei/i/B5/D04/AE4/044542/csfinal/cover_back_default.jpg" alt="CoreLogs" width="600" height="337" class="CToWUd"></a>
            </div>

                        <table style="border-collapse:collapse;border-spacing:0;table-layout:fixed;width:100%">
                          <tbody><tr>
                            <td style="padding:0;vertical-align:top;padding-left:32px;padding-right:32px;word-break:break-word;word-wrap:break-word">
                              <p style="font-style:normal;font-weight:400;Margin-bottom:25px;Margin-top:25px;font-size:16px;line-height:25px;font-family:Cabin,Avenir,sans-serif;color:#8e8e8e;text-align:center">With <a style="color:#3da7bf" href="http://industrylogger.cmail2.com/t/i-i-tjuhill-l-y/" target="_blank">CoreLogs</a>&nbsp;get connected to your own world of Baja &amp; Formula teams, Engineers, Small scale industries along with the event organizers and judges.</p>
                            </td>
                          </tr>
                        </tbody></table>

                        <table style="border-collapse:collapse;border-spacing:0;table-layout:fixed;width:100%">
                          <tbody><tr>
                            <td style="padding:0;vertical-align:top;padding-left:32px;padding-right:32px;word-break:break-word;word-wrap:break-word">

            <div style="Margin-bottom:0;Margin-top:0;text-align:center">
              <u></u><a style="border-radius:3px;display:inline-block;font-size:14px;font-weight:700;line-height:24px;padding:13px 35px 12px 35px;text-align:center;text-decoration:none!important;font-family:Cabin,Avenir,sans-serif;background-color:#3e8018;color:#fff" href="http://industrylogger.cmail2.com/t/i-i-tjuhill-l-j/" target="_blank">Register Now</a><u></u>
            </div>

                            </td>
                          </tr>
                        </tbody></table>

                      <div style="font-size:34px;line-height:34px">&nbsp;</div>
                    </td>
                  </tr>
                </tbody></table>
              </td>
            </tr>
          </tbody></table>

          <table style="border-collapse:collapse;border-spacing:0;width:100%">
            <tbody><tr>
              <td style="padding:0;vertical-align:top" align="center">
                <table style="border-collapse:collapse;border-spacing:0;Margin-left:auto;Margin-right:auto;background-color:#ffffff;width:600px;table-layout:fixed">
                  <tbody><tr>
                    <td style="padding:0;vertical-align:top;text-align:left;width:300px">

            <div style="font-size:12px;font-style:normal;font-weight:400;Margin-bottom:0;Margin-top:0;font-family:Cabin,Avenir,sans-serif;color:#8e8e8e" align="center">
              <a href="http://industrylogger.cmail2.com/t/i-i-tjuhill-l-t/" target="_blank"><img style="border:0;display:block;max-width:480px" src="https://ci3.googleusercontent.com/proxy/w3Ptd9esTKq5LMIoqR2F8qn3S3z_5h1ZWnslIGwkEXPZ_XUv2Nq_PNjtfgysODfWSWMJBqUDTTkV3O0jk3fwUuwBUg-Ds4NSLh-BCrOPRt6Ae_w=s0-d-e1-ft#http://i2.cmail2.com/ei/i/B5/D04/AE4/044542/csfinal/core1.JPG" alt="CoreLogs" width="300" height="185" class="CToWUd"></a>
            </div>

                        <table style="border-collapse:collapse;border-spacing:0;table-layout:fixed;width:100%">
                          <tbody><tr>
                            <td style="padding:0;vertical-align:top;padding-left:32px;padding-right:16px;word-break:break-word;word-wrap:break-word">
                              <h2 style="font-style:normal;font-weight:500;Margin-bottom:0;Margin-top:28px;font-size:24px;line-height:32px;font-family:&quot;Open Sans&quot;,sans-serif;color:#4badd1">The Engineer's Forum</h2><p style="font-style:normal;font-weight:400;Margin-bottom:28px;Margin-top:12px;font-size:16px;line-height:25px;font-family:Cabin,Avenir,sans-serif;color:#8e8e8e"><strong style="font-weight:bold">Get all your questions answered. </strong><br>
Checkout the Forum on CoreLogs and start asking and answering technical and event related questions.</p>
                            </td>
                          </tr>
                        </tbody></table>

                        <table style="border-collapse:collapse;border-spacing:0;table-layout:fixed;width:100%">
                          <tbody><tr>
                            <td style="padding:0;vertical-align:top;padding-left:32px;padding-right:16px;word-break:break-word;word-wrap:break-word">

            <div style="Margin-bottom:0;Margin-top:0;text-align:left">
              <u></u><a style="border-radius:3px;display:inline-block;font-size:12px;font-weight:700;line-height:22px;padding:10px 28px;text-align:center;text-decoration:none!important;font-family:Cabin,Avenir,sans-serif;background-color:#3da7bf;color:#fff" href="http://industrylogger.cmail2.com/t/i-i-tjuhill-l-i/" target="_blank">Visit the Forum</a><u></u>
            </div>

                            </td>
                          </tr>
                        </tbody></table>

                      <div style="font-size:34px;line-height:34px">&nbsp;</div>
                    </td>
                    <td style="padding:0;vertical-align:top;text-align:left;width:300px">

            <div style="font-size:12px;font-style:normal;font-weight:400;Margin-bottom:0;Margin-top:0;font-family:Cabin,Avenir,sans-serif;color:#8e8e8e" align="center">
              <a href="http://industrylogger.cmail2.com/t/i-i-tjuhill-l-d/" target="_blank"><img style="border:0;display:block;max-width:480px" src="https://ci4.googleusercontent.com/proxy/21Q1uvPpAdHADsznqpWYRuuYGIchGBj2E0-yNz6lBHkifna40YWk_Xn6Af6XZCOPek7rRioe4_ULu1RjtuOi0xarhBDOxwnwUheBretTy2A1_sI=s0-d-e1-ft#http://i3.cmail2.com/ei/i/B5/D04/AE4/044542/csfinal/core3.JPG" alt="CoreLogs" width="300" height="180" class="CToWUd"></a>
            </div>

                        <table style="border-collapse:collapse;border-spacing:0;table-layout:fixed;width:100%">
                          <tbody><tr>
                            <td style="padding:0;vertical-align:top;padding-left:16px;padding-right:32px;word-break:break-word;word-wrap:break-word">
                              <h2 style="font-style:normal;font-weight:500;Margin-bottom:0;Margin-top:28px;font-size:24px;line-height:32px;font-family:&quot;Open Sans&quot;,sans-serif;color:#4badd1">Team Profile</h2><p style="font-style:normal;font-weight:400;Margin-bottom:28px;Margin-top:12px;font-size:16px;line-height:25px;font-family:Cabin,Avenir,sans-serif;color:#8e8e8e"><strong style="font-weight:bold">Now no need for a team website.&nbsp;</strong><br>
On CoreLogs, you get a team profile where you can upload all the info related to your team along with individual user profiles.</p>
                            </td>
                          </tr>
                        </tbody></table>

                        <table style="border-collapse:collapse;border-spacing:0;table-layout:fixed;width:100%">
                          <tbody><tr>
                            <td style="padding:0;vertical-align:top;padding-left:16px;padding-right:32px;word-break:break-word;word-wrap:break-word">

            <div style="Margin-bottom:0;Margin-top:0;text-align:left">
              <u></u><a style="border-radius:3px;display:inline-block;font-size:12px;font-weight:700;line-height:22px;padding:10px 28px;text-align:center;text-decoration:none!important;font-family:Cabin,Avenir,sans-serif;background-color:#3da7bf;color:#fff" href="http://industrylogger.cmail2.com/t/i-i-tjuhill-l-h/" target="_blank">Register Now</a><u></u>
            </div>

                            </td>
                          </tr>
                        </tbody></table>

                      <div style="font-size:34px;line-height:34px">&nbsp;</div>
                    </td>
                  </tr>
                </tbody></table>
              </td>
            </tr>
          </tbody></table>

          <div style="font-size:1px;line-height:34px;width:100%">&nbsp;</div>

      <table style="border-collapse:collapse;border-spacing:0;width:100%;background-color:#d5e9ed">
        <tbody><tr>
          <td style="padding:0;vertical-align:top">&nbsp;</td>
          <td style="padding:0;vertical-align:top;width:600px">
            <table style="border-collapse:collapse;border-spacing:0" width="100%">
              <tbody><tr>
                <td style="padding:0;vertical-align:top;font-family:Cabin,Avenir,sans-serif;padding-top:40px;padding-bottom:75px;text-align:left;font-size:11px;line-height:17px;color:#93a6ad">
                  <div style="padding-left:32px;padding-right:32px;word-break:break-word;word-wrap:break-word;padding:0;Margin-left:20px;Margin-right:20px">
                    <div style="font-family:Cabin,Avenir,sans-serif;color:#93a6ad">CoreLogs - A Platform for entire core segment of engineering</div>
                    <div style="line-height:17px;font-size:17px">&nbsp;</div>
                    <div style="font-family:Cabin,Avenir,sans-serif">You are receiving this email because you belong to some baja/formula team</div>
                    <div>
                      <span>
                        <span>
                          <a style="font-weight:700;letter-spacing:0.01em;text-decoration:none;color:#93a6ad" href="http://industrylogger.updatemyprofile.com/i-l-2AD73FFF-l-p" lang="en" target="_blank">
                            Preferences
                          </a>
                          <span>&nbsp;&nbsp;|&nbsp;&nbsp;</span>
                        </span>
                      </span>
                      <span>
                        <a style="font-weight:700;letter-spacing:0.01em;text-decoration:none;color:#93a6ad" href="http://industrylogger.cmail2.com/t/i-u-tjuhill-l-x/" target="_blank">
                          Unsubscribe
                        </a>
                      </span>
                    </div>
                  </div>
                </td>
                <td style="padding:0;vertical-align:top;font-family:Cabin,Avenir,sans-serif;padding-top:40px;padding-bottom:75px;text-align:left;font-size:10px;text-transform:uppercase;width:170px">
                  <div style="padding-left:32px;padding-right:32px;word-break:break-word;word-wrap:break-word;padding:0;Margin-left:20px;Margin-right:20px">
                    <div style="Margin-bottom:10px">
                      <a style="font-weight:700;letter-spacing:0.01em;text-decoration:none;line-height:12px;color:#93a6ad" href="http://industrylogger.cmail2.com/t/i-fb-tjuhill-l-m/" rel="cs_facebox" target="_blank"><img style="border:0;vertical-align:middle" src="https://ci3.googleusercontent.com/proxy/UuoRcToYyCuV9vWmVxujHZnr-4BRnVFSnV4d1u9b4dWcpZM8L3tizNhC6sv7ffCRduU1N4OBGg2s5RF7UMw8_zycQ46uyWDJ-cpPuV8vFsixtLw7uiDPCVfYofM=s0-d-e1-ft#http://i4.cmail2.com/static/eb/master/08-tint/images/facebook-dark.png" alt="" width="38" height="30" class="CToWUd"><span>Like</span></a>
                    </div>

                    <div style="Margin-bottom:10px">
                      <a style="font-weight:700;letter-spacing:0.01em;text-decoration:none;line-height:12px;color:#93a6ad" href="http://industrylogger.forwardtomyfriend.com/i-l-2AD73FFF-tjuhill-l-c" lang="en" target="_blank"><img style="border:0;vertical-align:middle" src="https://ci4.googleusercontent.com/proxy/N9hDDGgs_sSKCCrmkevJBiEQu2yilosLmztydssRO991MI-CgVV7uUXvfjDjS6dOsxtocpDvL1iCNZ9KEqDmFWfKT7ijh7j5EGlaoxoHqnfpx9hOzqsuWtHheQ=s0-d-e1-ft#http://i6.cmail2.com/static/eb/master/08-tint/images/forward-dark.png" alt="" width="38" height="30" class="CToWUd"><span>Forward</span></a>
                    </div>
                  </div>
                </td>
              </tr>
            </tbody></table>
          </td>
          <td style="padding:0;vertical-align:top">&nbsp;</td>
        </tr>
      </tbody></table>
    </center>
  <img style="border:0!important;display:block!important;min-height:1px!important;width:1px!important;margin:0!important;padding:0!important" src="https://ci5.googleusercontent.com/proxy/KDRq0pv2QV0C9rFqkXGq0NYp2arBZu771M-cf9IUiYz48zOMxQQs8itA7DMWZPr2xvt50VZ4NRoXvuAxiajsoyZtbgC9xMWhwihY9sY=s0-d-e1-ft#https://industrylogger.cmail2.com/t/i-o-tjuhill-l/o.gif" width="1" height="1" border="0" alt="" class="CToWUd"><div class="yj6qo"></div><div class="adL">
</div></div>
'''

template4 = '''
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
