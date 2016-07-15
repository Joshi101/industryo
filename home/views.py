from django.shortcuts import render, redirect, render_to_response, RequestContext, HttpResponse
from nodes.models import Node
from nodes.forms import UploadImageForm
from userprofile.models import UserProfile
from workplace.models import Workplace
from forum.models import Question
from tags.models import Tags
from leads.models import Leads
from products.models import Products, Category
from itertools import chain
from allauth.account.forms import AddEmailForm, ChangePasswordForm
from allauth.account.forms import LoginForm, ResetPasswordKeyForm
from allauth.account.forms import ResetPasswordForm, SetPasswordForm, SignupForm, UserTokenForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from operator import attrgetter
from django.contrib.auth.decorators import login_required
from home import tasks
from django.core.mail import send_mail


def feedback(request):
    user =request.user
    userprofile = user.userprofile
    user_email = request.GET.get('email')
    feedback = request.GET.get('feedback')

    template = u'''Hi Dude,

{0} has sent a Feedback.
:
{1}

If you solve it, kindly mail back on {2}
'''
    content = template.format(userprofile, feedback, user_email)
    subject = u'''{0} sent a feedback'''.format(userprofile)
    try:
        send_mail(subject, content, 'sp@corelogs.com', ['sprksh.j@gmail.com'])
    except Exception:
        pass

    return HttpResponse()


def home(request):
    if request.user.is_authenticated():
        a =request.GET.get('a')
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
                # return redirect('/tags/nirman-mechjunction/')
                related_node = Node.feed.filter(w_type__in=['C', 'O']).select_related('user__userprofile')
                question = Question.objects.filter(user__userprofile__primary_workplace__workplace_type=t).select_related('user__userprofile')
            else:  # t == 'O':
                related_node = Node.feed.filter(w_type__in=['C', 'O']).select_related('user__userprofile')
                question = Question.objects.filter(user__userprofile__primary_workplace__workplace_type=t).select_related('user__userprofile')
            all_result_list = sorted(
                chain(related_node, question),
                key=attrgetter('date'), reverse=True)
            act = Node.objects.filter(category='D')
            if a:
                paginator = Paginator(act, 5)
            else:
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

    return render(request, 'sitemap/sitemap_user.html', {"list": people, "what": 'user'})


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

    return render(request, 'sitemap/sitemap_user.html', {"list": objects, "what": 'workplace'})


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

    return render(request, 'sitemap/sitemap_user.html', {"list": objects, "what": 'question'})


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

    return render(request, 'sitemap/sitemap_user.html', {"list": objects, "what": 'tag'})


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

    return render(request, 'sitemap/sitemap_user.html', {"list": objects, "what": 'article'})


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

    return render(request, 'sitemap/sitemap_user.html', {"list": objects, "what": 'product'})


def categories(request):
    all_objects = Category.objects.all()
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

    return render(request, 'sitemap/sitemap_user.html', {"list": objects, "what": 'category'})


def categories_wp(request):
    all_objects = Category.objects.all()
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

    return render(request, 'sitemap/sitemap_user.html', {"list": objects, "what": 'category_wp'})


def nodes(request):
    all_objects = Node.objects.filter(category__in=['F', 'D'])
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

    return render(request, 'sitemap/sitemap_user.html', {"list": objects, "what": 'nodes'})


def leads(request):
    all_objects = Leads.objects.all()
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

    return render(request, 'sitemap/sitemap_user.html', {"list": objects, "what": 'leads'})


def about(request):
    return render_to_response(request, 'about.html')


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

