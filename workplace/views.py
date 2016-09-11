from django.shortcuts import render, redirect, HttpResponse
from django.template.loader import render_to_string
from workplace.forms import WorkplaceForm, SetWorkplaceForm
from workplace.models import *
from nodes.models import Node
from products.models import Products
from tags.models import Tags, TagRelations
from forum.models import Question, Answer
from nodes.forms import SetLogoForm
from activities.models import Enquiry
from userprofile.models import User, UserProfile, Workplaces
import json
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import send_mail
from itertools import chain
from operator import attrgetter
from threading import Thread
from contacts.views import wp_email
from django.db.models import Q
from activities.views import create_notifications


@login_required
def set_workplace(request):
    if request.method == 'POST':
        user = request.user
        userprofile = UserProfile.objects.get(user=user)
        workplace = request.POST.get('workplace')
        w_type = request.POST.get('type')
        pre_workplace = request.POST.get('pre_workplace')
        if len(pre_workplace) > 3:
            primary_workplace, created = Workplace.objects.get_or_create(name=pre_workplace, workplace_type=w_type)
        else:
            return HttpResponse('The name should have at least 4 characters')
        if not created:
            us = User.objects.filter(userprofile__primary_workplace=primary_workplace)
            if us:
                create_notifications(from_user=user, to_users=us, typ='J')
        job_position = request.POST.get('job_position')
        userprofile.set_primary_workplace(primary_workplace, job_position)
        o, created = Workplaces.objects.get_or_create(userprofile=userprofile,
                                                      workplace=primary_workplace, job_position=job_position)
        t = userprofile.primary_workplace.workplace_type
        # node = '''<a href="/user/{0}">{1}</a> registered on CoreLogs and joined \
        # <a href="/workplace/{2}">{3}</a> as {4}'''.format(user.username, userprofile,
        #                                                   primary_workplace.slug, primary_workplace,
        #                                                   userprofile.job_position)
        # Node.objects.create(post=node, user=request.user, category='D', w_type=t)
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
        # node = '''<a href="/user/{0}">{1}</a> registered on CoreLogs and joined \
        # <a href="/workplace/{2}">{3}</a> as {4}'''.format(user.username, userprofile,
        #                                                   primary_workplace.slug, primary_workplace,
        #                                                   userprofile.job_position)

        # Send mail to the user instantly

        # Node.objects.create(post=node, user=request.user, category='D', w_type=t)
        if t in ['A', 'B']:
            return redirect('/workplace/edit/')
        else:
            return redirect('/workplace/'+primary_workplace.slug)
    else:
        return render(request, 'userprofile/set.html', {'form_set_workplace': SetWorkplaceForm(),
                                                        'form_create_workplace': WorkplaceForm()})


def change_type(request):
    id = request.GET.get('id')
    type = request.GET.get('t')
    wp = Workplace.objects.get(id=id)
    wp.workplace_type = type
    wp.save()
    members = wp.get_members()
    for m in members:
        m.workplace_type = type
        m.save()
    return HttpResponse()


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
    return render(request, 'tags/list_wp.html', {'objects': q, 'query': w})


def no_hits(id):
    q = Workplace.objects.get(id=id)
    q.hits +=1
    q.save()


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
        result_list = paginator.page(1)
    except EmptyPage:
        return
    if page:
        return render(request, 'workplace/20_workplaces.html', {'result_list': result_list})
    else:
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
            # print(key, request.POST[key])
            if key in direct:
                try:
                    dictionary[key] = request.POST[key]
                except:
                    tb = traceback.format_exc()
                    print(tb)
            else:
                interest = ''
                if key == 'segments':
                    wp.set_tags(tags=request.POST[key], typ='S')
                    interest = interest+request.POST[key]+','
                if key == 'operations':
                    wp.set_tags(tags=request.POST[key], typ='O')
                    interest = interest+request.POST[key]+','
                if key == 'machinery':
                    wp.set_tags(tags=request.POST[key], typ='A')
                    interest = interest+request.POST[key]+','
                if key == 'city':
                    wp.set_tags(tags=request.POST[key], typ='C')
                    interest = interest+request.POST[key]+','
                if key == 'events':
                    wp.set_tags(tags=request.POST[key], typ='E')
                    interest = interest + request.POST[key] + ','

                for u in workplace.get_members():
                    u.set_interests(interest)

            for key in dictionary:
                setattr(workplace, key, dictionary[key])
                if key == 'office_mail_id':
                    wp_email(workplace)
            workplace.save()

        response = {}
        response['info_score'] = workplace.get_info_score()
        return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        dict = workplace.__dict__
        dict['workplace'] = workplace
        dict['workplace_logo_form'] = SetLogoForm()
        if workplace.workplace_type in ['C', 'O']:
            return render(request, 'workplace/edit_team.html', dict)
        else:
            return render(request, 'workplace/edit.html', dict)


def set_interest_all():
    ws = Workplace.objects.all()
    for w in ws:
        tags = w.get_all_tags()
        if len(tags) > 2:
            for m in w.get_members():
                m.set_interests(tags)
                print(w.id)


def random_card(request):
    user = request.user
    up = request.user.userprofile
    workplace = up.primary_workplace
    if request.method == 'POST':
        if 'msg' in request.POST:
            return render(request, 'workplace/snippets/rc_com_email_msg.html', locals())
        else:
            data = request.POST.get('data')
            setattr(up, 'product_email', data)
            up.save()

            return HttpResponse()


import requests
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
    wp.set_tags(tags=city, typ='C')
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


import itertools

def relate_tags():
    wps = Workplace.objects.filter(id__lt=700)
    for w in wps:
        tagged = WpTags.objects.filter(workplace=w)
        uss = itertools.combinations(tagged, 2)
        for comb in uss:
            try:
                o = TagRelations.objects.filter(tag1=comb[0].tags, tag2=comb[1].tags).first()

                if o:
                    print('mila')
                    p = o.count
                    o.count = p+1
                    o.save()
                    print('count badha')
            except Exception:
                o = TagRelations.objects.filter(tag2=comb[0].tags, tag1=comb[1].tags).first()

                if o:
                    print('doosre me mila')
                    p = o.count
                    o.count = p+1
                    o.save()
                    print('count badha')
            finally:
                t, created = TagRelations.objects.get_or_create(tag1=comb[0].tags, tag2=comb[1].tags)
                if not created:
                    t.count +=1
                    t.save()




