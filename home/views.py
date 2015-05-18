from django.shortcuts import render, redirect, render_to_response, RequestContext
from django.contrib.auth import authenticate, logout

from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm


def home(request):
    if request.user.is_authenticated():
        user = request.user
        name = user.username
        text = "this is the landing page of this website for now"
        return render(request, 'home.html', locals())
    else:
        text = "this is the landing page of this website for now"

        return render(request, 'home.html', locals())

def search(request):
    if 'q' in request.GET:
        return redirect('/search/')

    else:
        return render(request, 'search/search.html')




