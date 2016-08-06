import re
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.conf.urls import patterns, include, url


def nav_suggest(request):
    path = request.POST.get('path')
    if request.user.is_authenticated():
        message = "Listing more Products brings you more Inquiries Directly and makes your Company profile stronger"
        link = "/products/edit_add/new/"
        link_text = "List Products Here."
        wp = reverse('workplace:workplace_profile', kwargs={'slug': request.user.userprofile.primary_workplace.slug})
        # print(wp, path)
        # if path == '/feed/':
        #     message = "Hi Sir, This is feed and you are weed"
        #     link = "/feed/"
        #     link_text = "I'll show you a feed"

    else:
        message = "Register your Company to get a free Company Profile in the Network and Connect to other SMEs online"
        link = "/accounts/signup/"
        link_text = "Register Now"
    return render(request, 'snippets/messages/top_nav_msg.html', {'msg': message, 'link': link, 'link_text': link_text})