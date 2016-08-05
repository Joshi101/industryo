import re
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.conf.urls import patterns, include, url


def nav_advert(request):
    path = request.GET['path']
    if request.user.is_authenticated():
        wp = reverse('workplace:workplace_profile', kwargs={'slug': request.user.userprofile.primary_workplace.slug})
        print(wp, path)
        if path == '/feed/':
            message = "Hi Sir, This is feed and you are weed"
            link = "/feed/"
            link_text = "I'll show you a feed"

        # message = "hello userqe87w678"
        # link = "/feed/"
        # link_text = "I'll show you a feed"
    else:
        message = "Register your Company to get a free Company Profile in the Network"
        link = "/"
        link_text = "Register Now"
    return render(request, 'snippets/messages/top_nav_msg.html', {'msg': message, 'link': link, 'link_text': link_text})