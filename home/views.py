from django.shortcuts import render, redirect, render_to_response, RequestContext
from nodes.models import Node
from nodes.forms import UploadImageForm
from userprofile.models import UserProfile
from workplace.models import Workplace
from forum.models import Question
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

# import tasks


def home(request):
    if request.user.is_authenticated():
        user = request.user
        if user.userprofile.primary_workplace:
            t = user.userprofile.primary_workplace.workplace_type

            workplaces = Workplace.objects.filter(workplace_type=t).order_by('?')[:5]           # change it soon
        else:
            workplaces = Workplace.objects.all().order_by('?')[:5]          # change it soon

        if request.user.userprofile.primary_workplace:
            profile = UserProfile.objects.select_related('primary_workplace__workplace_type').get(user=user)
            workplace = profile.primary_workplace
            t = workplace.workplace_type
            if t == 'A':
                related_node = Node.feed.filter(w_type=t).select_related('user__userprofile')
                question = Question.objects.filter(user__userprofile__primary_workplace__workplace_type=t).select_related('user__userprofile')
            elif t == 'B':
                related_node = Node.feed.filter(w_type=t).select_related('user__userprofile')
                question = Question.objects.filter(user__userprofile__primary_workplace__workplace_type=t).select_related('user__userprofile')
            elif t == 'C':
                related_node = Node.feed.filter(w_type=t).select_related('user__userprofile')
                question = Question.objects.filter(user__userprofile__primary_workplace__workplace_type=t).select_related('user__userprofile')
            else:  # t == 'O':
                related_node = Node.feed.filter(w_type=t).select_related('user__userprofile')
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
                return render(request, 'home.html', {'result_list': result_list, 'workplace':workplace, 'feed_img_form':UploadImageForm(), 'workplaces':workplaces})
        else:
            return redirect('/set/')
    else:
        return render(request, 'cover.html',{'form_signup':SignupForm(), 'form_login':LoginForm()})

def about(request):
    return render_to_response ('about.html')


def search(request):
    if 'q' in request.GET:
        return redirect('/search/')
    else:
        return render(request, 'search/search.html')


@login_required
def send_an_email(request):
    if request.user.id == 1:
        users = User.objects.filter(id__gte=90)
        for user in users:
            if user.email:
                user_email = user.email
            else:
                user_email = "rohit9gag@gmail.com"
            if user.first_name:
                name = user.get_full_name()
            else:
                name = user.username
            template = u'''Hi {0},

How did you like www.corelogs.com ?

The website is going at a great pace. Many scholars from various colleges, SAE Teams & Industries have registered and are actively participating in the discussions.

Visit the www.corelogs.com/forum/ and see if you can answer the questions.

Ask a question today and get it answered by the best out there.

Thanks & Regards

Surya Prakash
CoreLogs'''

            content = template.format(name)
            try:
                send_mail('CoreLogs Followup', content, 'surya@corelogs.com', [user_email])
            except Exception:
                pass
        return redirect('/sitemap')
    else:
        return redirect('/sitemap')


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