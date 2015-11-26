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
def send_list(request):
    li = ['sprksh.j@gmail.com', 'dmce.torridracing@gmail.com', 'autorangers2016@gmail.com', 'baja@kiit.ac.in', 'info@teamaerosouls.com',
          'acrostreakbaja@gmail.com', 'sae.sati@gmail.com', 'sae@bitmesra.ac.in', 'saenitrr@gmail.com', 'saeindiacpu@gmail.com',
          'forza.racing.baja@gmail.com', 'blitzpvpit@gmail.com', 'teamarvan2.0@gmail.com', 'info@teamvulcans.com',
          'umkcbaja@umkc.edu', 'scoe.baja@gmail.com', 'teamunwired@nitc.ac.in', 'rohit.kher619@gmail.com', 'sachiname@live.com',
          'ignitorracing107@gmail.com', 'race@9T9racing.com', 'vssutsae@gmail.com', 'emanation.ksit@gmail.com', 'info@teamaudacious.com',
          'fssparkracing@gmail.com', 'raftarformularacing@gmail.com', 'info@stesracing.in', 'banduriarijit16@gmail.com', 'sid04sid@gmail.com',
          'sbjitmr.sae@gmail.com', 'knocksoniacs@gmail.com', 'vayuputrasupra@gmail.com', 'redlineracing.supra@gmail.com',
          'newautomachen@gmail.com', 'supermileage@dce.ac.in', 'racing.pioneers@gmail.com', 'stallionmotorsport@gmail.com',
          'sachiname@live.com', 'info@areionmotorsports.com']
    for m in li:
        tasks.list_mail(m, n=18)
    return redirect('/')

@login_required
def send_test(request):
    tasks.test_mail(1, n=17)
    return redirect('/')

@login_required
def send_an_email(request):
    userprofiles = UserProfile.objects.filter(primary_workplace__workplace_type='C')
    # userprofiles = UserProfile.objects.filter(id__lte=1)
    for u in userprofiles:
        tasks.text_mail(u.id, n=16)
    return redirect('/')

    # content = '''
    # hi {0}
    # '''
    # html_content = content.format('Ram')
    # msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    # msg.attach_alternative(html_content, "text/html")
    # msg.send()
    # return redirect('/')

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

