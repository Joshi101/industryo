from django.shortcuts import render, HttpResponse
from leads.models import Leads, Reply
from chat.models import Conversation, Message
from activities.models import Enquiry
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
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
    con_list = []
    for con in conversations:
        con_list.append(con.id)
    messages = Message.objects.filter(conversation__in=con_list)
    all_result_list = sorted(
        chain(inquiries, quotations, conversations),
        key=attrgetter('date'), reverse=True)

    paginator = Paginator(all_result_list, 20)

    page = request.GET.get('page')
    try:
        result_list = paginator.page(page)
    except PageNotAnInteger:
        result_list = paginator.page(1)
    except EmptyPage:
        return
    if request.is_ajax():
        return render(request, 'inbox/20_messages.html', {'result_list': result_list, 'messages': messages})
    else:
        return render(request, 'inbox/inbox.html', {'result_list': result_list, 'messages': messages,
                                                    'empty': 'inbox/no_nothing.html'})


@login_required
def quotations(request):
    user = request.user
    wp = user.userprofile.primary_workplace
    quotations = Reply.objects.filter(lead__user=user).order_by('date')
    all_result_list = sorted(
        chain(quotations),
        key=attrgetter('date'), reverse=True)
    paginator = Paginator(all_result_list, 20)
    page = request.GET.get('page')
    try:
        result_list = paginator.page(page)
    except PageNotAnInteger:
        result_list = paginator.page(1)
    except EmptyPage:
        return
    if request.is_ajax():
        return render(request, 'inbox/20_messages.html', {'result_list': result_list, 'empty': 'inbox/no_quotations.html'})
    else:
        return render(request, 'inbox/inbox.html', {'result_list': result_list, 'empty': 'inbox/no_quotations.html'})


@login_required
def inquiries(request):
    user = request.user
    wp = user.userprofile.primary_workplace
    inquiries = Enquiry.objects.filter(Q(workplace=wp) | Q(product__producer=wp)).order_by('date')
    all_result_list = sorted(
        chain(inquiries),
        key=attrgetter('date'), reverse=True)
    paginator = Paginator(all_result_list, 20)
    page = request.GET.get('page')
    try:
        result_list = paginator.page(page)
    except PageNotAnInteger:
        result_list = paginator.page(1)
    except EmptyPage:
        return
    if request.is_ajax():
        return render(request, 'inbox/20_messages.html', {'result_list': result_list, 'empty': 'inbox/no_inquiries.html'})
    else:
        return render(request, 'inbox/inbox.html', {'result_list': result_list, 'empty': 'inbox/no_inquiries.html'})


@login_required
def messages(request):
    user = request.user
    wp = user.userprofile.primary_workplace
    conversations = Conversation.objects.filter(Q(user1=user) | Q(user2=user)).order_by('last_active')
    con_list = []
    for con in conversations:
        con_list.append(con.id)
    messages = Message.objects.filter(conversation__in=con_list)
    all_result_list = sorted(
        chain(conversations),
        key=attrgetter('date'), reverse=True)
    paginator = Paginator(all_result_list, 20)
    page = request.GET.get('page')
    try:
        result_list = paginator.page(page)
    except PageNotAnInteger:
        result_list = paginator.page(1)
    except EmptyPage:
        return
    if request.is_ajax():
        return render(request, 'inbox/20_messages.html', {'result_list': result_list, 'messages': messages, 'empty': 'inbox/no_inquiries.html'})
    else:
        return render(request, 'inbox/inbox.html', {'result_list': result_list, 'messages': messages, 'empty': 'inbox/no_inquiries.html'})


def outbox(request):
    user = request.user
    wp = user.userprofile.primary_workplace
    inquiries = Enquiry.objects.filter(user=user).order_by('date')
    quotations = Reply.objects.filter(user=user).order_by('date')
    # messages = Message.objects.filter()
    conversations = Conversation.objects.filter(Q(user1=user) | Q(user2=user)).order_by('last_active')
    con_list = []
    for con in conversations:
        con_list.append(con.id)
    messages = Message.objects.filter(conversation__in=con_list)
    all_result_list = sorted(
        chain(inquiries, quotations, conversations),
        key=attrgetter('date'), reverse=True)
    paginator = Paginator(all_result_list, 20)
    page = request.GET.get('page')
    try:
        result_list = paginator.page(page)
    except PageNotAnInteger:
        result_list = paginator.page(1)
    except EmptyPage:
        return
    if request.is_ajax():
        return render(request, 'inbox/20_messages.html', {'result_list': result_list, 'messages': messages})
    else:
        return render(request, 'inbox/inbox.html', {'result_list': result_list, 'messages': messages,
                                                    'empty': 'inbox/no_nothing.html'})


@login_required
def sent_quotations(request):
    user = request.user
    wp = user.userprofile.primary_workplace
    quotations = Reply.objects.filter(user=user).order_by('date')
    all_result_list = sorted(
        chain(quotations),
        key=attrgetter('date'), reverse=True)
    paginator = Paginator(all_result_list, 20)
    page = request.GET.get('page')
    try:
        result_list = paginator.page(page)
    except PageNotAnInteger:
        result_list = paginator.page(1)
    except EmptyPage:
        return
    if request.is_ajax():
        return render(request, 'inbox/20_messages.html', {'result_list': result_list, 'empty': 'inbox/no_quotations.html'})
    else:
        return render(request, 'inbox/inbox.html', {'result_list': result_list, 'empty': 'inbox/no_quotations.html'})


@login_required
def sent_inquiries(request):
    user = request.user
    wp = user.userprofile.primary_workplace
    inquiries = Enquiry.objects.filter(user=user).order_by('date')
    all_result_list = sorted(
        chain(inquiries),
        key=attrgetter('date'), reverse=True)
    paginator = Paginator(all_result_list, 20)
    page = request.GET.get('page')
    try:
        result_list = paginator.page(page)
    except PageNotAnInteger:
        result_list = paginator.page(1)
    except EmptyPage:
        return
    if request.is_ajax():
        return render(request, 'inbox/20_messages.html', {'result_list': result_list, 'empty': 'inbox/no_inquiries.html'})
    else:
        return render(request, 'inbox/inbox.html', {'result_list': result_list, 'empty': 'inbox/no_inquiries.html'})


@login_required
def sent_messages(request):
    user = request.user
    wp = user.userprofile.primary_workplace
    conversations = Conversation.objects.filter(Q(user1=user) | Q(user2=user)).order_by('last_active')
    con_list = []
    for con in conversations:
        con_list.append(con.id)
    messages = Message.objects.filter(conversation__in=con_list)
    all_result_list = sorted(
        chain(conversations),
        key=attrgetter('date'), reverse=True)
    paginator = Paginator(all_result_list, 20)
    page = request.GET.get('page')
    try:
        result_list = paginator.page(page)
    except PageNotAnInteger:
        result_list = paginator.page(1)
    except EmptyPage:
        return
    if request.is_ajax():
        return render(request, 'inbox/20_messages.html', {'result_list': result_list, 'messages': messages, 'empty': 'inbox/no_inquiries.html'})
    else:
        return render(request, 'inbox/inbox.html', {'result_list': result_list, 'messages': messages, 'empty': 'inbox/no_inquiries.html'})


@csrf_exempt
def mark_seen(request):
    what = request.POST.get('what')
    id = request.POST.get('id')
    if what == 'quotation':
        r = Reply.objects.get(id=id)
        r.seen = True
        r.save()
    if what == 'inquiry':
        e = Enquiry.objects.get(id=id)
        e.seen = True
        e.save()
    if what == 'message':
        m = Message.objects.get(id=id)
        m.seen = True
        m.save()
        c = m.conversation
        c.seen = True
        c.save()
    return HttpResponse()


def set_wp_inq():
    enquiries = Enquiry.objects.all()
    for en in enquiries:
        if en.product:
            en.workplace = en.product.producer
            en.save()