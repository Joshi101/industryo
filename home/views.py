from django.shortcuts import render, redirect, render_to_response, RequestContext
from django.contrib.auth import authenticate, logout

from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from nodes.models import Node
from userprofile.models import UserProfile


def home(request):
    if request.user.is_authenticated():
        user = request.user
        # name = user.username
        workplace = request.user.userprofile.primary_workplace
        text = "this is the landing page of this website for now"

        profile = UserProfile.objects.get(user=user)
        workplace = profile.primary_workplace
        job_position = profile.job_position
        # t = workplace.workplace_type

        # related_node = Node.objects.filter(user_workplace_workplace_type=workplace.workplace_type)

        return render(request, 'home.html', locals())
    else:
        text = "this is the landing page of this website for now"

        return render(request, 'home.html', locals())


def search(request):
    if 'q' in request.GET:
        return redirect('/search/')

    else:
        return render(request, 'search/search.html')


def content(request):
    user = request.user
    workplace = request.user.userprofile.workplace
    type = workplace.workplace_type
    related_node = Node.objects.filter(user_workplace_workplace_type=type)


#
# def set_workplace(request):
#     if request.method == 'POST':




