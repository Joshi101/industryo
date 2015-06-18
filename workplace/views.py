from django.shortcuts import render, redirect, HttpResponse
from django.template.loader import render_to_string
from workplace.forms import WorkplaceForm, SetWorkplaceForm, SetTeamTypeForm, SetSegmentForm
from workplace.models import *
from nodes.models import Node
from forum.models import Question, Answer
from nodes.forms import SetLogoForm
from userprofile.models import User, UserProfile
import json
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@login_required
def workplace_register(request):
    form = WorkplaceForm(request.POST)
    if request.method == 'POST':
        response = {}
        r_value = {}
        r_inputs = []
        r_html = {}
        r_elements = []
        if not form.is_valid():
            return HttpResponse(json.dumps(response), content_type="application/json")
        else:
            name = form.cleaned_data.get('name')
            workplace_type = form.cleaned_data.get('workplace_type')
            t, created = Workplace.objects.get_or_create(name=name, workplace_type=workplace_type)
            if created:
                welcome = u'{0} is now in the network, have a look at its profile.'.format(name)
                node = Node(user=User.objects.get(pk=1), post=welcome)
                node.save()
                r_elements = ['message']
                r_html['message'] = render_to_string('snippets/create_wp_alert.html', {'name':name})
            r_inputs = ['id_workplace']
            r_value['id_workplace'] = name
            response['html'] = r_html
            response['elements'] = r_elements
            response['value'] = r_value
            response['inputs'] = r_inputs
            return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        return redirect('/set/')

@login_required
def set_workplace(request):
    if request.method == 'POST':
        form = SetWorkplaceForm(request.POST)
        if not form.is_valid():
            return render(request, 'userprofile/set.html', {'form_set_workplace': form,'form_create_workplace':WorkplaceForm()})
        else:
            user = request.user
            workplace = form.cleaned_data.get('workplace')
            primary_workplace = Workplace.objects.get(name=workplace)
            job_position = form.cleaned_data.get('job_position')
            userprofile = UserProfile.objects.get(user=user)
            userprofile.primary_workplace = primary_workplace
            userprofile.job_position = job_position
            userprofile.save()
            t = userprofile.primary_workplace.workplace_type

            welcome = u'{0} has started working in {1}.'.format(user, primary_workplace)
            node = Node(user=User.objects.get(pk=1), post=welcome)   #, tags=t
            node.save()
            if user.first_name:
                return redirect('/')
            else:
                return redirect('/details/')
    else:
        return render(request, 'userprofile/set.html', {'form_set_workplace': SetWorkplaceForm(), 'form_create_workplace': WorkplaceForm()})


def search_workplace(request):                  # for searching the workplace
    if request.method == 'GET':
        w = request.GET['the_query']
        o = Workplace.objects.filter(name__icontains=w)
        create = request.GET['the_create']
        return render(request, 'tags/list.html', {'o': o, 'create': create})
    else:
        return render(request, 'tags/list.html')


@login_required
def set_tags(request):
    if request.method == 'POST':
        response = {}
        r_html = {}
        r_elements = []
        user = request.user
        up = user.userprofile
        wp = user.userprofile.primary_workplace
        type = request.POST.get('type')
        value = request.POST.get('value')

        if type == 'A':
            t = wp.set_assets(value)
        if type == 'M':
            t = wp.set_materials(value)
        if type == 'O':
            t = wp.set_operations(value)
        if type == 'I':
            t = wp.set_industrial_area(value)
        if type == 'C':
            t = wp.set_city(value)
        if type == 'P':
            t = wp.set_institution(value)
        if type == 'E':
            t = wp.set_events(value)
        new_interest = t
        r_elements = ['detail_body']
        r_html['detail_body'] = render_to_string('snippets/one_interest.html', {'interest': new_interest})
        response['html'] = r_html
        response['elements'] = r_elements
        response['prepend'] = True
        return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        return redirect('/user/'+request.user.username)


def workplace_profile(request, slug):
    workplace = Workplace.objects.get(slug=slug)
    members = UserProfile.objects.filter(primary_workplace=workplace.pk)
    member_count = members.count()
    workplace_logo_form = SetLogoForm()
    questions = Question.objects.filter(user__userprofile__primary_workplace=workplace).select_related('user')
    answers = Question.objects.filter(answer__user__userprofile__primary_workplace=workplace).select_related('user')
    feeds = Node.feed.filter(user__userprofile__primary_workplace=workplace).select_related('user')
    # articles = Node.article.filter(user__userprofile__primary_workplace=workplace).select_related('user')
    return render(request, 'workplace/profile.html', locals())


def workplace_questions(request, id):
    workplace = Workplace.objects.get(id=id)
    questions = Question.objects.filter(user__userprofile__primary_workplace=workplace).select_related('user')
    paginator = Paginator(questions, 5)
    page = request.GET.get('page')

    try:
        result_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        result_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        return

    return render(request, 'nodes/five_nodes.html', {'articles': result_list})


def workplace_answers(request, id):
    workplace = Workplace.objects.get(id=id)
    answers = Answer.objects.filter(question__user__userprofile__primary_workplace=workplace).select_related('user')
    paginator = Paginator(answers, 5)
    page = request.GET.get('page')

    try:
        result_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        result_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        return

    return render(request, 'nodes/five_nodes.html', {'articles': result_list})



def workplace_feeds(request, id):
    workplace = Workplace.objects.get(id=id)
    feeds = Node.feed.filter(user__userprofile__primary_workplace=workplace).select_related('user')
    paginator = Paginator(feeds, 5)
    page = request.GET.get('page')

    try:
        result_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        result_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        return

    return render(request, 'nodes/five_nodes.html', {'articles': result_list})



def workplace_articles(request, id):
    workplace = Workplace.objects.get(id=id)
    articles = Node.article.filter(user__userprofile__primary_workplace=workplace).select_related('user')
    paginator = Paginator(articles, 5)
    page = request.GET.get('page')

    try:
        result_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        result_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        return

    return render(request, 'nodes/five_nodes.html', {'articles': result_list})


def get_top_scorers(request, slug):
    workplace = Workplace.objects.get(slug=slug)
    members = UserProfile.objects.filter(primary_workplace=workplace.id).order_by('-points')[:3]
    return render(request, 'snippets/people_list.html', {'people': members})


@login_required
def set_about(request):
    user = request.user
    wp = user.userprofile.primary_workplace
    if request.method == 'POST':
        response = {}
        about = request.POST.get('about')
        wp.about = about
        wp.save()
        w = user.userprofile.primary_workplace
        return HttpResponse()
    else:
        return redirect('/workplace/'+wp.slug)

@login_required
def set_capabilities(request):
    user = request.user
    wp = user.userprofile.primary_workplace
    print('bournvita')
    if request.method == 'POST':
        print('bournvita')
        response = {}
        capabilities = request.POST.get('capabilities')
        wp.about = capabilities
        wp.save()
        print('bournvita')
        return HttpResponse()
    else:
        return redirect('/workplace/'+wp.slug)

@login_required
def set_product_details(request):
    user = request.user
    wp = user.userprofile.primary_workplace
    if request.method == 'POST':
        response = {}
        product_details = request.POST.get('product_details')
        wp.product_details = product_details
        wp.save()
        return HttpResponse()
    else:
        return redirect('/workplace/'+wp.slug)


        

# Create your views here.
