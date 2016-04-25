from django.shortcuts import render, redirect, render_to_response, RequestContext, HttpResponse
from allauth.socialaccount.models import SocialAccount, SocialToken
import urllib.request as urllib2
from xml.etree import ElementTree as etree
from allauth.socialaccount.models import SocialToken




def get_email_google(request):
    # social = request.user.social_auth.get(provider='google-oauth2')
    user =request.user

    # Code dependent upon django-allauth. Will change if we shift to another module

    # if request.user.userprofile.get_provider() != "google":
    a = SocialAccount.objects.get(user=user)
    b = SocialToken.objects.get(account=a)
    # access = b.token
    access_token = b.token
    url = 'https://www.google.com/m8/feeds/contacts/default/full' + '?access_token=' + access_token + '&max-results=100' +'&alt=json'
    req = urllib2.Request(url, headers={'User-Agent' : "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.30 (KHTML, like Gecko) Ubuntu/11.04 Chromium/12.0.742.112 Chrome/12.0.742.112 Safari/534.30"})
    contacts = urllib2.urlopen(req).read()
    contacts_xml = etree.fromstring(contacts)
    # print
    # return render(request, 'search/random_text_print.html', locals())

    result = []

    for entry in contacts_xml.findall('{http://www.w3.org/2005/Atom}entry'):
        for address in entry.findall('{http://schemas.google.com/g/2005}email'):
            email = address.attrib.get('address')
            result.append(email)
        for address in entry.findall('{http://schemas.google.com/g/2005}fullName'):
            fullName = address.attrib.get('fullName')
            result.append(fullName)
    return render(request, 'search/random_text_print.html', locals())


