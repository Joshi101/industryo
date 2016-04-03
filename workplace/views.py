from django.shortcuts import render, redirect, HttpResponse, render_to_response
from django.template.loader import render_to_string
from workplace.forms import WorkplaceForm, SetWorkplaceForm, SetTeamTypeForm, SetSegmentForm
from workplace.models import *
from nodes.models import Node
from products.models import Products
from forum.models import Question, Answer
from nodes.forms import SetLogoForm
from userprofile.models import User, UserProfile, Workplaces
import json
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from home import tasks
from itertools import chain
from operator import attrgetter
import re

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
            if name:
                if len(name)>4:
                    workplace_type = form.cleaned_data.get('workplace_type')
            else:
                return HttpResponse('The name should have at least 5 characters')
            t, created = Workplace.objects.get_or_create(name=name, workplace_type=workplace_type)
            if created:
                r_elements = ['message']
                r_html['message'] = render_to_string('snippets/create_wp_alert.html', {'name': name})
            node = '''<a href="/workplace/{0}">{1}</a> is now registered on CoreLogs. Have a look at its profile and members.'''.format(t.slug, t)
            n = Node.objects.create(post=node, user=request.user, category='D', w_type=t.workplace_type)
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
        user = request.user
        userprofile = UserProfile.objects.get(user=user)
        workplace = request.POST.get('workplace')
        w_type = request.POST.get('type')
        pre_workplace = request.POST.get('pre_workplace')
        if len(pre_workplace)>3:
            primary_workplace, created = Workplace.objects.get_or_create(name=pre_workplace, workplace_type=w_type)
        else:
            return HttpResponse('The name should have at least 4 characters')
            # pass # (send this in display)
        user.userprofile.notify_also_joined(primary_workplace)
        job_position = request.POST.get('job_position')
        userprofile.primary_workplace = primary_workplace
        userprofile.job_position = job_position
        userprofile.save()
        o, created = Workplaces.objects.get_or_create(userprofile=userprofile, workplace=primary_workplace, job_position=job_position)

        t = userprofile.primary_workplace.workplace_type
        tasks.send_html_mail(user.id, n=88)
        node = '''<a href="/user/{0}">{1}</a> registered on CoreLogs and joined <a href="www.corelogs.com/workplace/{2}">{3}</a> as {4}'''.format(user.username, userprofile, primary_workplace.slug, primary_workplace, userprofile.job_position)
        n = Node.objects.create(post=node, user=request.user, category='D', w_type=t)
        # if user.first_name:
        return redirect('/workplace/'+primary_workplace.slug)
        # else:
        #     return redirect('/details/')
    else:
        return render(request, 'userprofile/set.html', {'form_set_workplace': SetWorkplaceForm(), 'form_create_workplace': WorkplaceForm()})


def search_workplace(request):                  # for searching the workplace
    w = request.GET['the_query']
    w_type = request.GET['the_type']
    q = None
    if len(w) >= 2:
        terms = w.split(' ')
    else:
        return HttpResponse('Keep Typing..')

    for term in terms:
        o = Workplace.objects.filter(name__icontains=term, workplace_type=w_type)
        if q is None:
            q = o
        else:
            q = q & o
    # if len(q)<4:      # for searcing indian institute of tech.. on typing iit
    #     if len(w)<4:
    #         for a in w:
    #             Workplace.objects.filter()
    #         print('WWWWWWWW')
    return render(request, 'tags/list_wp.html', {'objects': q, 'query': w})


@login_required
def set_tags(request):
    if request.method == 'POST':
        response = {}
        r_html = {}
        r_elements = []
        user = request.user
        up = user.userprofile
        wp = user.userprofile.primary_workplace
        operations = request.POST.get('operations')
        materials = request.POST.get('materials')
        assets = request.POST.get('assets')
        if operations:
            t = wp.set_operations(operations)
        if materials:
            t = wp.set_materials(materials)
        if assets:
            t = wp.set_assets(assets)
        return HttpResponse()
    else:
        return redirect('/user/'+request.user.username)


@login_required
def set_tags_short(request):
    if request.method == 'POST':
        response = {}
        r_html = {}
        r_elements = []
        user = request.user
        up = user.userprofile
        wp = user.userprofile.primary_workplace
        type = request.POST.get('type')
        value = request.POST.get('tag')
        if value:
            if type == 'A':
                t = wp.set_assets(value)
            if type == 'M':
                t = wp.set_materials(value)
            if type == 'O':
                t = wp.set_operations(value)
            if type == 'C':
                t = wp.set_city(value)
            if type == 'P':
                t = wp.set_institution(value)
            if type == 'E':
                t = wp.set_events(value)
            if type == 'S':
                t = wp.set_segments(value)
            new_interest = t
            r_elements = ['info_field_value']
            r_html['info_field_value'] = render_to_string('snippets/tag_short.html', {'tags': new_interest})
            response['html'] = r_html
            response['elements'] = r_elements
            response['prepend'] = False
            return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        return redirect('/user/'+request.user.username)


def workplace_profile(request, slug):
    workplace = Workplace.objects.get(slug=slug)
    tags = workplace.get_tags()
    type = workplace.workplace_type
    if type == 'C':
        tags1 = tags['city']
        tags2 = tags['segments']
        tags3 = tags['institution']
        b_type = 'P'
    elif type == 'B':
        tags1 = tags['city']
        tags2 = tags['segments']
        b_type = 'S'
    elif type == 'A':
        tags1 = tags['city']
        tags2 = tags['segments']
        b_type = 'S'
    elif type == 'O':
        tags1 = tags['city']
    members = UserProfile.objects.filter(primary_workplace=workplace.pk)
    member_count = members.count()
    workplace_logo_form = SetLogoForm()

    return render(request, 'workplace/profile.html', locals())


def workplace_about(request, slug):
    workplace = Workplace.objects.get(slug=slug)
    members = UserProfile.objects.filter(primary_workplace=workplace.pk)
    tags = workplace.get_tags()
    type = workplace.workplace_type
    if type == 'C':
        tags1 = tags['city']
        tags2 = tags['institution']
        b_type = 'P'
    elif type == 'B':
        tags1 = tags['city']
        tags2 = tags['segments']
        b_type = 'S'
    elif type == 'A':
        tags1 = tags['city']
        tags2 = tags['segments']
        b_type = 'S'
    elif type == 'O':
        tags1 = tags['city']
    # member_count = members.count()
    # workplace_logo_form = SetLogoForm()
    return render(request, 'workplace/snip_about.html', locals())


def workplace_dash(request, slug):
    workplace = Workplace.objects.get(slug=slug)
    members = UserProfile.objects.filter(primary_workplace=workplace.pk)
    member_count = members.count()
    products = Products.objects.filter(producer=workplace.pk)
    product_count = products.count()
    workplace_logo_form = SetLogoForm()
    return render(request, 'workplace/snip_dashboard.html', locals())


def workplace_activity(request, slug):
    workplace = Workplace.objects.get(slug=slug)
    members = UserProfile.objects.filter(primary_workplace=workplace.pk)
    member_count = members.count()
    workplace_logo_form = SetLogoForm()
    questions = Question.objects.filter(user__userprofile__primary_workplace=workplace).select_related('user')
    answers = Question.objects.filter(answer__user__userprofile__primary_workplace=workplace).select_related('user')
    feeds = Node.feed.filter(user__userprofile__primary_workplace=workplace).select_related('user')[:10]
    articles = Node.objects.filter(user__userprofile__primary_workplace=workplace, category='A').select_related('user')
    # return render(request, 'workplace/snip_dashboard.html', locals())
    all_result_list = sorted(
        chain(feeds, questions, answers, articles),
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
        return render(request, 'workplace/snip_dashboard.html', locals())


def workplace_capabilities(request, slug):
    workplace = Workplace.objects.get(slug=slug)
    members = UserProfile.objects.filter(primary_workplace=workplace.pk)
    member_count = members.count()
    workplace_logo_form = SetLogoForm()
    return render(request, 'workplace/snip_capabilities.html', locals())


def workplace_members(request, slug):
    workplace = Workplace.objects.get(slug=slug)
    members = UserProfile.objects.filter(primary_workplace=workplace.pk)
    member_count = members.count()
    workplace_logo_form = SetLogoForm()
    products = Products.objects.filter(producer=workplace.pk)
    return render(request, 'workplace/snip_members.html', locals())


def workplace_products(request, slug):
    workplace = Workplace.objects.get(slug=slug)
    members = UserProfile.objects.filter(primary_workplace=workplace.pk)
    member_count = members.count()
    workplace_logo_form = SetLogoForm()
    products = Products.objects.filter(producer=workplace.pk)
    return render(request, 'workplace/snip_products.html', locals())


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
    members = UserProfile.objects.filter(primary_workplace=workplace.id).order_by('?')[:3]
    return render(request, 'workplace/snippets/wp_right.html', {'people': members})


@login_required
def set_about(request):
    user = request.user
    wp = user.userprofile.primary_workplace
    if request.method == 'POST':
        about = request.POST.get('about')
        wp.about = about
        wp.save()
        return HttpResponse()
    else:
        return redirect('/workplace/'+wp.slug)


@login_required
def set_details(request):
    user = request.user
    wp = user.userprofile.primary_workplace
    if request.method == 'POST':
        response = {}
        website = request.POST.get('website')
        address = request.POST.get('address')
        contact = request.POST.get('contact')
        contact1 = request.POST.get('contact1')
        email = request.POST.get('email')
        linkedin = request.POST.get('linkedin')
        fb = request.POST.get('fb')
        city = request.POST.get('city')
        segement = request.POST.get('segement')

        if city:
            t1 = wp.set_city(city)
        if segement:
            t2 = wp.set_segments(segement)
        wp.website = website
        wp.address = address
        wp.contact = contact
        wp.contact1 = contact1
        wp.office_mail_id = email
        wp.linkedin_page = linkedin
        wp.fb_page = fb
        wp.save()
        return HttpResponse()
    else:
        return redirect('/workplace/'+wp.slug)

@login_required
def edit_links(request):
    user = request.user
    wp = user.userprofile.primary_workplace
    if request.method == 'POST':
        response = {}
        website = request.POST.get('website')
        fb_page = request.POST.get('fb_page')
        linkedin_page = request.POST.get('linkedin_page')
        wp.website = website
        wp.fb_page = fb_page
        wp.linkedin_page = linkedin_page
        wp.save()
        w = user.userprofile.primary_workplace
        return HttpResponse()
    else:
        return redirect('/workplace/'+wp.slug)


@login_required
def edit_contacts(request):
    user = request.user
    wp = user.userprofile.primary_workplace
    if request.method == 'POST':
        response = {}
        office_mail = request.POST.get('office_mail')
        contact = request.POST.get('contact')
        mobile_1 = request.POST.get('mobile_1')
        mobile_2 = request.POST.get('mobile_2')
        address = request.POST.get('address')
        wp.office_mail_id = office_mail
        wp.contact = contact
        wp.mobile_contact1 = mobile_1
        wp.mobile_contact2 = mobile_2
        wp.address = address
        wp.save()
        w = user.userprofile.primary_workplace
        return HttpResponse()
    else:
        return redirect('/workplace/'+wp.slug)


@login_required
def set_capabilities(request):
    user = request.user
    wp = user.userprofile.primary_workplace
    if request.method == 'POST':
        response = {}
        capabilities = request.POST.get('capabilities')
        wp.capabilities = capabilities
        wp.save()
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


@login_required
def delete_tag(request):
    if request.method == 'POST':
        print('tag to be deleted')
        user = request.user
        up = user.userprofile
        wp = user.userprofile.primary_workplace
        delete = request.POST.get('delete')
        t = Tags.objects.get(tag=delete)
        try:
            WpTags.objects.get(tags=t, workplace=wp).delete()
        except:
            up.interests.remove(t)
        return HttpResponse()
# def delete_tags


def side_panel(request):
    user = request.user
    t = user.userprofile.primary_workplace.workplace_type

    workplaces = Workplace.objects.filter(workplace_type=t).order_by('?')[:4]           # change it soon
    return render(request, 'snippets/workplace_list.html', locals())


def fodder(request):
    ob = Workplace.objects.all()

    for o in ob:
        m = o.get_members()
        s =0
        for i in m:
            p = i.points
            s +=p

        o.points = s
        o.save()
    return redirect('/')


def todder(request):
    workplaces = Workplace.objects.all().order_by('?')
    paginator = Paginator(workplaces, 30)
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
        return render(request, 'workplace/20_workplaces.html', {'result_list': result_list})
    else:
        # return render(request, 'home.html', {'result_list': result_list})
        return render(request, 'workplace/workplace_tag.html', {'result_list': result_list})
# Create your views here.


def change_workplace(request):
    if 'q' in request.GET:
        querystring = request.GET.get('q')
        usp = request.user.userprofile
        workplace = Workplace.objects.get(id=querystring)
        usp.primary_workplace = workplace
        usp.save()
        return redirect('/')


def workplace_data(request):
    workplaces = Workplace.objects.filter(workplace_type='C')
    # li = []
    # for w in workplaces:
    #     u = UserProfile.objects.filter(primary_workplace=w.id)
    #     c = u.count()
    #     li.append(c)
    return render(request, 'activities/workplace_data.html', locals())


# @background(schedule=60)
def invite_colleague(request):
    user =request.user
    userprofile = user.userprofile
    workplace = user.userprofile.primary_workplace
    user_email = request.POST.get('email')
    name = request.POST.get('name')

    template = u'''Hi {0},

{1} has personally asked you to join www.corelogs.com as a member of {2}.

We look forward to see you on CoreLogs shortly and hope that you like the website as well as {3} did.

For your curiosity, www.corelogs.com is a website for engineers and people working in small, medium & large scale
industries to get connected to each other and build a community of like minded people to help each other.

Admin
CoreLogs
'''
    content = template.format(name, userprofile, workplace, userprofile)
    subject = u'''{0} invites you to CoreLogs.'''.format(userprofile)
    try:
        send_mail(subject, content, 'sp@corelogs.com', [user_email])
    except Exception:
        pass

    return HttpResponse()


@login_required
def join_wp(request, slug):
    workplace = Workplace.objects.get(id=slug)
    # a page with workplace =workplace asking whether you are sure or want to change
    user = request.user
    user.userprofile.primary_workplace = workplace
    user.userprofile.save()
    return redirect('/workplace/'+workplace.slug)

@login_required
def add_tag(request):
    user = request.user
    tid = request.GET.get('t')
    if user.userprofile.primary_workplace:
        w = user.userprofile.primary_workplace
        tag = Tags.objects.get(id=tid)
        w.set_event(tag)
        return redirect('/tags/'+tag.slug)

    else:
        return redirect('/set/')





