from django.shortcuts import render, redirect, HttpResponse, render_to_response
from django.template.loader import render_to_string
from workplace.forms import WorkplaceForm, SetWorkplaceForm, SetTeamTypeForm, SetSegmentForm
from workplace.models import *
from nodes.models import Node
from products.models import Products
from tags.models import Tags
from forum.models import Question, Answer
from nodes.forms import SetLogoForm
from activities.models import Enquiry
from userprofile.models import User, UserProfile, Workplaces
import json
from django.core import serializers
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from home import tasks
from itertools import chain
from operator import attrgetter
from threading import Thread


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
        user.userprofile.notify_also_joined(primary_workplace)
        job_position = request.POST.get('job_position')
        userprofile.set_primary_workplace(primary_workplace, job_position)
        o, created = Workplaces.objects.get_or_create(userprofile=userprofile,
                                                      workplace=primary_workplace, job_position=job_position)
        t = userprofile.primary_workplace.workplace_type
        # tasks.send_html_mail(user.id, n=88) # Moved to contacts
        node = '''<a href="/user/{0}">{1}</a> registered on CoreLogs and joined \
        <a href="/workplace/{2}">{3}</a> as {4}'''.format(user.username, userprofile,
                                                                          primary_workplace.slug, primary_workplace,
                                                                          userprofile.job_position)
        Node.objects.create(post=node, user=request.user, category='D', w_type=t)
        if t in ['A', 'B']:
            return redirect('/workplace/edit/')
        else:
            return redirect('/workplace/'+primary_workplace.slug)
    else:
        return render(request, 'userprofile/set.html', {'form_set_workplace': SetWorkplaceForm(),
                                                        'form_create_workplace': WorkplaceForm()})

@login_required
def set_others_wp(request, username):
    if request.method == 'POST':
        user = User.objects.get(username=username)
        userprofile = UserProfile.objects.get(user=user)
        workplace = request.POST.get('workplace')
        w_type = request.POST.get('type')
        pre_workplace = request.POST.get('pre_workplace')
        if len(pre_workplace)>3:
            primary_workplace, created = Workplace.objects.get_or_create(name=pre_workplace, workplace_type=w_type)
        else:
            return HttpResponse('The name should have at least 4 characters')
        user.userprofile.notify_also_joined(primary_workplace)
        job_position = request.POST.get('job_position')
        userprofile.set_primary_workplace(primary_workplace, job_position)
        o, created = Workplaces.objects.get_or_create(userprofile=userprofile,
                                                      workplace=primary_workplace, job_position=job_position)
        t = userprofile.primary_workplace.workplace_type
        # tasks.send_html_mail(user.id, n=88) # Moved to contacts
        node = '''<a href="/user/{0}">{1}</a> registered on CoreLogs and joined \
        <a href="/workplace/{2}">{3}</a> as {4}'''.format(user.username, userprofile,
                                                                          primary_workplace.slug, primary_workplace,
                                                                          userprofile.job_position)
        Node.objects.create(post=node, user=request.user, category='D', w_type=t)
        if t in ['A', 'B']:
            return redirect('/workplace/edit/')
        else:
            return redirect('/workplace/'+primary_workplace.slug)
    else:
        return render(request, 'userprofile/set.html', {'form_set_workplace': SetWorkplaceForm(),
                                                        'form_create_workplace': WorkplaceForm()})



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
        city = request.POST.get('çity')
        segment = request.POST.get('segment')
        if operations:
            t = wp.set_operations(operations)
        if materials:
            t = wp.set_materials(materials)
        if assets:
            t = wp.set_assets(assets)
        if city:
            t = wp.set_city(city)
        if segment:
            t = wp.set_segments(segment)
        response = {}
        response['tag'] = render_to_string('snippets/tags.html', {'tags': t})

        return HttpResponse(json.dumps(response), content_type="application/json")
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
    products = Products.objects.filter(producer=workplace.pk)
    product_count = products.count()
    workplace_logo_form = SetLogoForm()
    member_count = members.count()

    inquiry_count = Enquiry.objects.filter(product__in=products).count()
    new_inq_count = Enquiry.objects.filter(product__in=products, seen=False).count()
    node_count = Node.objects.filter(user__userprofile__primary_workplace=workplace).count()
    q_count = Question.objects.filter(user__userprofile__primary_workplace=workplace).count()
    a_count = Answer.objects.filter(user__userprofile__primary_workplace=workplace).count()
    if member_count > 0:
        completion_score = int(round((workplace.get_tags_score() + workplace.get_product_score() + workplace.get_info_score() +
                               workplace.points/(10*member_count) + workplace.get_member_score())/5))
    else:
        completion_score = 0
    products = Products.objects.filter(producer=workplace.pk)
    r_assets = Tags.objects.filter(type='A').order_by('?')[:5]
    inq_count = Enquiry.objects.filter(workplace=workplace).count()

    t = Thread(target=no_hits, args=(workplace.id,))
    t.start()

    return render(request, 'workplace/profile.html', locals())


def no_hits(id):
    q = Workplace.objects.get(id=id)
    q.hits +=1
    q.save()


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
    return render(request, 'workplace/snip_about.html', locals())


def workplace_dash(request, slug):
    workplace = Workplace.objects.get(slug=slug)
    members = UserProfile.objects.filter(primary_workplace=workplace.pk)
    workplace_logo_form = SetLogoForm()
    member_count = members.count()
    products = Products.objects.filter(producer=workplace.pk)
    inquiry_count = Enquiry.objects.filter(product__in=products).count()
    new_inq_count = Enquiry.objects.filter(product__in=products, seen=False).count()
    com_mail = request.user.userprofile.product_email

    node_count = Node.objects.filter(user__userprofile__primary_workplace=workplace).count()

    completion_score = (workplace.get_tags_score() + workplace.get_product_score() + workplace.get_info_score() +
                        (workplace.points)/(10*member_count) + workplace.get_member_score())/5

    return render(request, 'workplace/snip_dashboard.html', locals())


def workplace_activity(request, slug):
    workplace = Workplace.objects.get(slug=slug)
    members = UserProfile.objects.filter(primary_workplace=workplace.pk)
    member_count = members.count()
    workplace_logo_form = SetLogoForm()

    if member_count < 2:
        n=1
    elif member_count in range(2,5):
        n = 2
    elif member_count in range(5,10):
        n=3
    elif member_count in range(10, 20):
        n=4
    else:
        n=5

    li = [workplace.contact, workplace.mobile_contact1, workplace.website, workplace.fb_page,
          workplace.linkedin_page, workplace.address, workplace.office_mail_id]
    a = list(filter(lambda x: x!='None', li))
    b = list(filter(lambda x: x!=None, a))
    m = len(b)

    o = workplace.get_tags.operations
    return render(request, 'workplace/snip_dashboard.html', locals())


def activity(request, slug):                             # In Place of dashboard
    workplace = Workplace.objects.get(slug=slug)
    members = UserProfile.objects.filter(primary_workplace=workplace.pk)
    member_count = members.count()
    workplace_logo_form = SetLogoForm()
    questions = Question.objects.filter(user__userprofile__primary_workplace=workplace).select_related('user')
    answers = Question.objects.filter(answer__user__userprofile__primary_workplace=workplace).select_related('user')
    feeds = Node.objects.filter(user__userprofile__primary_workplace=workplace, category__in=['F', 'D']).select_related('user')
    articles = Node.objects.filter(user__userprofile__primary_workplace=workplace, category='A').select_related('user')
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
        return render(request, 'workplace/snip_activity.html', locals())


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
        wp.mobile_contact1 = contact1
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

import traceback

@login_required
def edit_workplace(request):
    user = request.user
    wp = user.userprofile.primary_workplace
    workplace = wp
    dictionary = {}
    direct = ['about', 'history', 'year_established', 'revenue', 'turnover', 'sme_type', 'wp_type', 'mobile_contact1',
              'mobile_contact2', 'fb_page', 'linkedin_page', 'address', 'contact', 'office_mail_id', 'legal_status',
              'number_of_employees', 'website', 'product_details']
    if request.method == 'POST':
        for key in request.POST:
            print(key, request.POST[key])
            if key in direct:
                try:
                    dictionary[key] = request.POST[key]
                except:
                    tb = traceback.format_exc()
                    print(tb)
            else:
                interest = ''
                if key == 'segments':
                    wp.set_segments(request.POST[key])
                    interest = interest+request.POST[key]+','
                if key == 'operations':
                    wp.set_operations(request.POST[key])
                    interest = interest+request.POST[key]+','
                if key == 'machinery':
                    wp.set_assets(request.POST[key])
                    interest = interest+request.POST[key]+','
                if key == 'city':
                    wp.set_city(request.POST[key])
                    interest = interest+request.POST[key]+','

                for u in workplace.get_members():
                    u.set_interests(interest)

            for key in dictionary:
                setattr(workplace, key, dictionary[key])
            workplace.save()

        response = []
        return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        dict = workplace.__dict__
        dict['workplace'] = workplace
        dict['workplace_logo_form'] = SetLogoForm()
        return render(request, 'workplace/edit.html', dict)


def set_interest_all():
    ws = Workplace.objects.all()
    for w in ws:
        tags = w.get_all_tags()
        if len(tags)>2:
            for m in w.get_members():
                m.set_interests(tags)
                print(w.id)


def random_card(request):
    print('randomao')
    user = request.user
    up = request.user.userprofile
    workplace = up.primary_workplace
    print(user, workplace)
    if request.method == 'POST':
        if 'msg' in request.POST:
            return render(request, 'workplace/snippets/rc_com_email_msg.html', locals())
        else:
            data = request.POST.get('data')
            setattr(up, 'product_email', data)
            up.save()
            return HttpResponse()


import requests

# url = 'http://www.corelogs.com/accounts/signup'
# values = {'name': name, 'email': email,'password1': 'Password', 'password2': 'Password'}
# data = urllib.urlencode(values)
# req = urllib2.Request(url, data)
# response = urllib2.urlopen(req)
# result = response.read()
# print result

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def create_api(request):
    email = request.POST.get('email1')
    # print(email)
    name = request.POST.get('name')
    contact = request.POST.get('phone')

    workplace = request.POST.get('workplace')
    about = request.POST.get('about')
    city = request.POST.get('city')
    website = request.POST.get('website')
    address = request.POST.get('address')

    wp, created = Workplace.objects.get_or_create(name=workplace, workplace_type='B')
    wp.about = about
    wp.address = address
    wp.website = website
    wp.contact = contact
    wp.save()
    wp.set_city(city)
    wp.set_segments('Manufacturing,Plastic')

    url = 'http://www.corelogs.com/accounts/signup/'

    if len(email)>4:
        payload = {'name': name, 'email': email, 'password1': 'Password', 'password2': 'Password'}
        r = requests.post(url, data=payload, headers={'User-Agent': 'Mozilla/5.0'})
        user = User.objects.get(email=email)
        up = user.userprofile
        up.dummy = True
        up.mobile_contact = contact
        up.save()
        up.set_primary_workplace(wp, 'Member')
        o, created = Workplaces.objects.get_or_create(userprofile=up,
                                                      workplace=wp, job_position='Member')


@csrf_exempt
def create_api2(request):
    email = request.POST.get('email1')
    name = request.POST.get('name')
    contact = request.POST.get('phone')
    workplace = request.POST.get('workplace')
    about = request.POST.get('about')
    city = request.POST.get('city')
    website = request.POST.get('website')
    address = request.POST.get('address')

    url = 'http://www.corelogs.com/accounts/signup/'
    wp = Workplace.objects.get(name=workplace)
    if len(email) > 4:
        payload = {'name': name, 'email': email, 'password1': 'Password', 'password2': 'Password'}
        r = requests.post(url, data=payload, headers={'User-Agent': 'Mozilla/5.0'})
        user = User.objects.get(email=email)
        up = user.userprofile
        up.dummy = True
        up.mobile_contact = contact
        up.save()
        up.set_primary_workplace(wp, 'Member')
        o, created = Workplaces.objects.get_or_create(userprofile=up,
                                                      workplace=wp, job_position='Member')


@csrf_exempt
def create_api3(request):
    workplace = request.POST.get('workplace')
    # print(workplace)
    product = request.POST.get('product')[:100]
    # print(product)
    description = request.POST.get('description')[:10000]
    wp = Workplace.objects.get(name=workplace)
    if len(wp.get_members()) > 0:
        # print('cool')
        up1 = wp.get_members()
        up = up1[0]
        u = up.user
        p = Products.objects.create(producer=wp, product=product, description=description, user=u)
        image0 = request.FILES.get('image0', None)
        if image0:
            i = Images()
            x = i.upload_image(image=image0, user=u)
            p.image = x
            p.save()
            # print('Image add hua')
        return
    else:
        # print('uncool')
        return




