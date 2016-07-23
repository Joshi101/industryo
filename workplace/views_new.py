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


def workplace_profile(request, slug):
    workplace = Workplace.objects.get(slug=slug)
    workplace_logo_form = SetLogoForm()
    if request.user.userprofile in workplace.userprofile_set.all():
        member = True
    content_url = "workplace/snip_about.html"
    content_head_url = "workplace/snip_about_head.html"
    if request.is_ajax():
        return render(request, content_url, locals())
    else:
        meta = True
        return render(request, 'workplace/profile.html', locals())

def dashboard(request, slug):
    workplace = Workplace.objects.get(slug=slug)
    workplace_logo_form = SetLogoForm()
    if request.user.userprofile in workplace.userprofile_set.all():
        member = True
    content_url = "workplace/snip_dashboard.html"
    content_head_url = "workplace/snip_dashboard_head.html"
    member_count = members.count()
    products = Products.objects.filter(producer=workplace.pk)
    inquiry_count = Enquiry.objects.filter(product__in=products).count()
    new_inq_count = Enquiry.objects.filter(product__in=products, seen=False).count()
    com_mail = request.user.userprofile.product_email

    node_count = Node.objects.filter(user__userprofile__primary_workplace=workplace).count()

    completion_score = (workplace.get_tags_score() + workplace.get_product_score() + workplace.get_info_score() +
                        (workplace.points)/(10*member_count) + workplace.get_member_score())/5
    if request.is_ajax():
        return render(request, content_url, locals())
    else:
        meta = True
        return render(request, 'workplace/profile.html', locals())

def activity(request, slug):
    workplace = Workplace.objects.get(slug=slug)
    workplace_logo_form = SetLogoForm()
    if request.user.userprofile in workplace.userprofile_set.all():
        member = True
    content_url = "workplace/snip_activity.html"
    content_head_url = "workplace/snip_activity_head.html"
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
        if request.is_ajax():
            return render(request, content_url, locals())
        else:
            meta = True
            return render(request, 'workplace/profile.html', locals())

def products(request, slug):
    workplace = Workplace.objects.get(slug=slug)
    workplace_logo_form = SetLogoForm()
    if request.user.userprofile in workplace.userprofile_set.all():
        member = True
    content_url = "workplace/snip_products.html"
    content_head_url = "workplace/snip_products_head.html"
    if request.is_ajax():
        return render(request, content_url, locals())
    else:
        meta = True
        return render(request, 'workplace/profile.html', locals())

def members(request, slug):
    workplace = Workplace.objects.get(slug=slug)
    workplace_logo_form = SetLogoForm()
    if request.user.userprofile in workplace.userprofile_set.all():
        member = True
    content_url = "workplace/snip_members.html"
    content_head_url = "workplace/snip_members_head.html"
    if request.is_ajax():
        return render(request, content_url, locals())
    else:
        meta = True
        return render(request, 'workplace/profile.html', locals())
