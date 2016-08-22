from operator import attrgetter
from itertools import chain
from django.shortcuts import render, redirect, render_to_response, HttpResponse
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.sessions.models import Session
from allauth.account.forms import LoginForm, SignupForm
from nodes.models import Node
from nodes.forms import UploadImageForm
from userprofile.models import UserProfile
from workplace.models import Workplace, WpTags
from forum.models import Question
from tags.models import Tags
from leads.models import Leads
from products.models import Products, Category
from home import tasks
from tracking.models import Tracker


@login_required
@user_passes_test(lambda u: u.userprofile.workplace_type != 'N', login_url='/set')
def network(request):
    if user.userprofile.primary_workplace:
        workplace = request.user.userprofile.primary_workplace
        my_city = workplace.get_tags()['city']
        my_segments = workplace.get_tags()['segments']
        new_tags = request.GET.get('tags')
        if new_tags:
            pass
        if request.GET.get('v') == 'city':
            if my_city:
                if request.GET.get('q') == 'companies':

                    companies = Workplace.objects.filter(id=0)
                    for city in my_city:
                        wps = city.wptags.filter(workplace_type__in=['A', 'B'])
                        companies = companies | wps
                    return render(request, 'tags/tag.html', {'workplaces': companies})

                else:        #elif request.GET.get('q') == 'feeds':
                    # print(my_segments)
                    companies = Workplace.objects.filter(id=0)
                    for city in my_city:
                        wps = city.wptags.filter(workplace_type__in=['A', 'B'])
                        companies = companies | wps
                    related_node = Node.objects.filter(user__userprofile__primary_workplace__in=companies)\
                        .select_related('user__userprofile')
                    question = Question.objects.filter(user__userprofile__primary_workplace__in=companies)\
                        .select_related('user__userprofile')
                    all_result_list = sorted(
                        chain(related_node, question),
                        key=attrgetter('date'), reverse=True)
                    paginator = Paginator(all_result_list, 10)

                    page = request.GET.get('page')
                    try:
                        result_list = paginator.page(page)
                    except PageNotAnInteger:
                        result_list = paginator.page(1)
                    except EmptyPage:
                        return
                    if page:
                        return render(request, 'nodes/five_nodes.html', {'result_list': result_list})
                    else:
                        return render(request, 'home.html', {'result_list': result_list,
                                                             'workplace': workplace, 'feed_img_form': UploadImageForm()})
            else:
                tags_all = Tags.objects.filter(type__in=['C', 'I']).order_by('-count')
                paginator = Paginator(tags_all, 20)
                page = request.GET.get('page')
                try:
                    tags = paginator.page(page)
                except PageNotAnInteger:
                    tags = paginator.page(1)
                except EmptyPage:
                    tags = paginator.page(paginator.num_pages)
                if page:
                    return render_to_response('tags/20_tags.html', {"tags": tags})
                else:
                    return render(request, 'tags/all_tags.html', {"tags": tags})

        else:       # elif request.GET.get('v') == 'segments':
            if my_segments:
                if request.GET.get('q') == 'companies':
                    companies = Workplace.objects.filter(id=0)
                    for city in my_segments:
                        wps = city.wptags.filter(workplace_type__in=['A', 'B'])
                        companies = companies | wps
                    return render(request, 'tags/tag.html', {'workplaces': companies})

                else:        #elif request.GET.get('q') == 'feeds':
                    companies = Workplace.objects.filter(id=0)
                    for city in my_segments:
                        wps = city.wptags.filter(workplace_type__in=['A', 'B'])
                        companies = companies | wps
                    related_node = Node.objects.filter(user__userprofile__primary_workplace__in=companies)\
                        .select_related('user__userprofile')
                    question = Question.objects.filter(user__userprofile__primary_workplace__in=companies)\
                        .select_related('user__userprofile')
                    all_result_list = sorted(
                        chain(related_node, question),
                        key=attrgetter('date'), reverse=True)
                    paginator = Paginator(all_result_list, 10)

                    page = request.GET.get('page')
                    try:
                        result_list = paginator.page(page)
                    except PageNotAnInteger:
                        result_list = paginator.page(1)
                    except EmptyPage:
                        return
                    if page:
                        return render(request, 'nodes/five_nodes.html', {'result_list': result_list})
                    else:
                        return render(request, 'home.html', {'result_list': result_list,
                                                             'workplace': workplace, 'feed_img_form': UploadImageForm()})

            else:
                tags_all = Tags.objects.filter(type__in=['O', 'S']).order_by('-count')
                paginator = Paginator(tags_all, 20)
                page = request.GET.get('page')
                try:
                    tags = paginator.page(page)
                except PageNotAnInteger:
                    tags = paginator.page(1)
                except EmptyPage:
                    tags = paginator.page(paginator.num_pages)
                if page:
                    return render_to_response('tags/20_tags.html', {"tags": tags})
                else:
                    return render(request, 'tags/all_tags.html', {"tags": tags})
    else:
        return redirect('/set')


def network_stats(request):
    user = request.user
    up = user.userprofile
    wp = up.primary_workplace
    c = wp.get_tags()
    cities = c['city']
    # city1 = city[0]
    wsc = Workplace.objects.filter(id<0)
    wss = Workplace.objects.filter(id<0)
    for city in cities:
        wps = city.wptags.all()
        wsc = wsc | wps
    li = []
    for key in c:
        if key != 'city':
            li.append(c[key])
    for e in li:
        wps = e.wptags.all()
        wss = wss | wps
    return HttpResponse()       # wsc: workplaces in same cities, wss:workplaces in same segment,operations etc


def network_prod(request):
    user = request.user
    wp = user.userprofile.primary_workplace
    c = wp.get_tags()
    cities = c['city']
    # city1 = city[0]
    wsc = Workplace.objects.filter(id<0)
    wss = Workplace.objects.filter(id<0)
    for city in cities:
        wps = city.wptags.all()
        wsc = wsc | wps
    li = []
    for key in c:
        if key != 'city':
            li.append(c[key])
    for e in li:
        wps = e.wptags.all()
        wss = wss | wps
    services = Products.objects.filter(producer__in=wsc, product_type='C')[:3]
    products = Products.objects.filter(producer__in=wss, product_type__in=['A', 'B'])[:3]

    return HttpResponse()




