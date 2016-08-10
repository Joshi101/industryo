from django.shortcuts import render
from leads.models import Leads, Reply
from chat.models import Conversation, Message
from activities.models import Enquiry
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from operator import attrgetter
from itertools import chain
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@login_required
def inbox(request):
    user = request.user
    wp = user.userprofile.primary_workplace
    inquiries = Enquiry.objects.filter(Q(workplace=wp) | Q(product__producer=wp)).order_by('date')
    quotations = Reply.objects.filter(lead__user=user).order_by('date')
    # messages = Message.objects.filter()
    conversations = Conversation.objects.filter(Q(user1=user) | Q(user2=user)).order_by('last_active')

    all_result_list = sorted(
        chain(inquiries, quotations, conversations),
        key=attrgetter('date'), reverse=True)

    paginator = Paginator(all_result_list, 20)

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
        return render(request, 'inbox/inbox.html', {'result_list': result_list})


@login_required
def inbox_received(request):
    user = request.user
    wp = user.userprofile.primary_workplace
    inquiries = Enquiry.objects.filter(user=user).order_by('date')
    quotations = Reply.objects.filter(user=user).order_by('date')
    # messages = Message.objects.filter()
    conversations = Conversation.objects.filter(Q(user1=user) | Q(user2=user)).order_by('last_active')

    all_result_list = sorted(
        chain(inquiries, quotations, conversations),
        key=attrgetter('date'), reverse=True)

    paginator = Paginator(all_result_list, 20)

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
        return render(request, 'inbox/inbox.html', {'result_list': result_list})



# Create your views here.
