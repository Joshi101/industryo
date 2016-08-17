import re
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.conf.urls import include, url


def nav_suggest(request):
    path = request.META['HTTP_REFERER']
    if request.user.is_authenticated():
        message = "Listing more Products brings you more Inquiries Directly and makes your Company profile stronger"
        link = "/products/edit_add/new/"
        link_text = "List Products Here."
        # wp = reverse('workplace:workplace_profile', kwargs={'slug': request.user.userprofile.primary_workplace.slug})
        print(path)
        if path[:5] == '/tags':
            message = ""
        if path[:5] == '/user':
            message = 'Listing more Products brings more business. You will get Product Inquiries directly in Inbox'
            link = "/products/edit_add/new/"
            link_text = "List Products Here."
        if path[:5] == '/work':
            message = 'Listing more Products brings more business. You will get Product Inquiries directly in Inbox'
            link = "/products/edit_add/new/"
            link_text = "List Products Here."
        if path[:5] == '/mark':
            message = 'Companies are listing 100s of Products. Simple Relation. More Products>> More Inquiries>> More Business'
            link = "/products/edit_add/new/"
            link_text = "List Products Here."
        if path[:5] == '/cate':
            message = 'Companies are listing 100s of Products. Simple Relation. More Products>> More Inquiries>> More Business'
            link = "/products/edit_add/new/"
            link_text = "List Products Here."
        if path[:5] == '/lead':
            message = 'You can send Direct Quotations. It will be seen only by the person who created th lead'
            link = "/products/edit_add/new/"
            link_text = "List Products Here."

    else:
        message = "Register your Company to get a free Company Profile in the Network and Connect to other SMEs online"
        link = "/accounts/signup/"
        link_text = "Register Now"
        # if path[:5] == '/lead':
        #     message = "You can send Direct Quotations. But You need to register your Company for that. It's Free."
        #     link = "/accounts/signup/"
        #     link_text = "Register Now"
    #     if path[:5] == '/cate':
    #         message = 'Does your company also fall in this Category? List Your Company and appear in Searches'
    #         link = "/accounts/signup/"
    #         link_text = "Register Now"
    # print(message)
    return render(request, 'snippets/messages/top_nav_msg.html', {'msg': message, 'link': link, 'link_text': link_text})
