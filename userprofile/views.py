from django.shortcuts import render, redirect, HttpResponse
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from userprofile.models import UserProfile
from userprofile.forms import EditProfileForm, SetInterestsForm, UserDetailsForm
from nodes.forms import *
from forum.models import Question, Answer
from nodes.models import Node
from django.contrib.auth.decorators import login_required
from tags.models import Tags
import json
from django.db.models import Q
from itertools import chain
from operator import attrgetter
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from allauth.socialaccount.models import SocialAccount


def profile(request, username):
    page_user = User.objects.get(username=username)
    name = page_user.get_full_name()
    userprofile = UserProfile.objects.get(user=page_user)
    profile_image_form = SetProfileImageForm()
    questions = Question.objects.filter(user=page_user)
    answers = Question.objects.filter(answer__question__user=page_user)
    feeds = Node.objects.filter(user=page_user, category__in=['F', 'D'])
    articles = Node.article.filter(user=page_user)
    interests = userprofile.get_interests()
    # return render(request, 'userprofile/profile.html', locals())
    all_result_list = sorted(
        chain(feeds, questions, answers, articles),
        key=attrgetter('date'), reverse=True)
    accounts = SocialAccount.objects.filter(user=request.user)
    acc = []
    for a in accounts:
        acc.append(a.get_provider)
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
        return render(request, 'userprofile/profile.html', locals())


def set_details(request):
    form = UserDetailsForm(request.POST)
    user = request.user
    up = user.userprofile
    if request.method == 'POST':
        if not form.is_valid():
            return render(request, 'userprofile/details.html', {'form': form})
        else:
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            mobile_contact = form.cleaned_data.get('phone_no')
            email = form.cleaned_data.get('email')
            user.first_name = first_name
            user.last_name = last_name
            up.mobile_contact = mobile_contact
            up.email = email
            up.save()
            user.save()
            return redirect('/workplace/'+user.userprofile.primary_workplace.slug)
    else:
        form = UserDetailsForm(instance=user, initial={
            'first_name': user.first_name,
            'last_name': user.last_name,
            'phone_no': up.mobile_contact,
            'email': up.email,
            })
        return render(request, 'userprofile/details.html', {'form': form})


def edit(request):
    form = EditProfileForm(request.POST)
    user = request.user
    up = user.userprofile
    if request.method == 'POST':
        if not form.is_valid():
            return render(request, 'userprofile/edit.html', {'form': form})
        else:

            gender = form.cleaned_data.get('gender')
            experience = form.cleaned_data.get('experience')

            up.gender = gender
            up.experience = experience
            up.save()
            return redirect("/user/"+user.username)
    else:
        form = EditProfileForm(instance=user, initial={
            'gender': up.gender,
            'experience': up.experience,
            })
        return render(request, 'userprofile/edit.html', {'form': form})


# @login_required
# def set_interests(request):
#     if request.method == 'POST':
#         response = {}
#         r_html = {}
#         r_elements = []
#         user = request.user
#         up = user.userprofile
#         interests = request.POST.get('value')
#         if type == 'All':
#             up.set_interests(interests)
#         up.set_interests(interests)
#         new_interest = user.userprofile.interests.get(tag=interests)
#         r_elements = ['detail_body']
#         r_html['detail_body'] = render_to_string('snippets/one_interest.html', {'interest': new_interest})
#         response['html'] = r_html
#         response['elements'] = r_elements
#         response['prepend'] = True
#         return HttpResponse(json.dumps(response), content_type="application/json")
#     else:
#         return redirect('/user/'+request.user.username)

#
# def set_interests(request):
#     if request.method == 'POST':
#         response = {}
#         r_html = {}
#         r_elements = []
#         user = request.user
#         up = user.userprofile
#         wp = user.userprofile.primary_workplace
#         # type = request.POST.get('type')
#         value = request.POST.get('tag')
#         if value:
#             t = wp.set_interests(value)
#             new_interest = t
#             r_elements = ['tag_container']
#             r_html['tag_container'] = render_to_string('snippets/tag_short.html', {'tag': new_interest, 'ajax':True})
#             response['html'] = r_html
#             response['elements'] = r_elements
#             response['prepend'] = True
#             return HttpResponse(json.dumps(response), content_type="application/json")
#     else:
#         return redirect('/user/'+request.user.username)


@login_required
def set_interests(request):
    if request.method == 'POST':
        response = {}
        r_html = {}
        r_elements = []
        user = request.user
        up = user.userprofile
        type = request.POST.get('type')
        value = request.POST.get('interests')
        if value:
            t = up.set_interests(value)
        new_interest = t
        r_elements = ['detail_body']
        r_html['detail_body'] = render_to_string('snippets/interests.html', {'interests': new_interest})
        response['html'] = r_html
        response['elements'] = r_elements
        response['prepend'] = True
        return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        return redirect('/user/'+request.user.username)


def delete_interest(request):
    if request.method == 'GET':
        user = request.user
        up = user.userprofile
        delete = request.GET['delete']

        response = {}
        # Tags.objects.get(tag=delete)
        up.interests.remove(tag=delete)

        return HttpResponse(json.dumps(response), content_type="application/json")


def set_experience(request):
    if request.method == 'POST':
        response = {}
        user = request.user
        up = user.userprofile
        experience = request.POST.get('experience')
        up.experience = experience
        up.save()
        return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        return redirect('/user/'+request.user.username)


def get_interests(request):
    page_user = User.objects.get(id=id)
    interests = page_user.userprofile.interests.all()
    return interests


def search_area(request):
    if 'the_query' in request.GET:
        t = request.GET['the_query']
        create = request.GET['the_create']
        o = Tags.objects.filter(type='A')[:6]

        return render(request, 'tags/list.html', {'o': o, 'create': create})
    else:
        return render(request, 'tags/list.html')


def search_person(request):                  # for searching the workplace
    if request.method == 'GET':
        w = request.GET['the_query']
        o = User.objects.filter(Q(first_name__icontains=w) | Q(last_name__icontains=w) | Q(username__icontains=w))[:5]
        # o = User.objects.filter(username__icontains=w)
        return render(request, 'tags/list_ppl.html', {'objects': o})
    else:
        return render(request, 'tags/list_ppl.html')


# def make_list(request):
#     ups = UserProfile.objects.filter(primary_workplace__workplace_type__in=['A', 'B'])
#     for u in ups:
#         tags = u.primary_workplace.tags.all()
#         li = []
#         for t in tags:
#             li.append(t.id)

def check_email(request):
    if request.method == 'POST':
        response = {}
        data = request.POST.get('data')
        e = data.strip()
        if e == '':
            response['valid'] = 2
        else:
            try:
                dup = User.objects.get(email=e)
                response['valid'] = 1
            except User.DoesNotExist:
                response['valid'] = 0
        return HttpResponse(json.dumps(response), content_type="application/json")


def check_username(request):
    if request.method == 'POST':
        response = {}
        data = request.POST.get('data')
        e = data.strip()
        if e == '':
            response['valid'] = 2
        else:
            try:
                dup = User.objects.get(username=e)
                response['valid'] = 1
            except User.DoesNotExist:
                response['valid'] = 0
        return HttpResponse(json.dumps(response), content_type="application/json")


def set_wp_type():
    us = UserProfile.objects.filter(workplace_type='N')
    for u in us:
        if u.primary_workplace:
            t = u.primary_workplace.workplace_type
            u.workplace_type = t
            u.save()
    return
