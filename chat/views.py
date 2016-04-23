from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
from chat.models import Message, Conversation
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import json
from django.db.models import Q
from home import tasks

from datetime import datetime, timedelta, time, date

# @login_required
# def inbox(request):
#     conversations = Message.get_conversations(user=request.user)
#     active_conversation = None
#     messages = None
#     if conversations:
#         conversation = conversations[0]
#         active_conversation = conversation['user'].username
#         messages = Message.objects.filter(user=request.user, conversation=conversation['user'])
#         messages.update(is_read=True)
#         for conversation in conversations:
#             if conversation['user'].username == active_conversation:
#                 conversation['unread'] = 0
#     return render(request, 'messages/inbox.html', {
#         'messages': messages,
#         'conversations': conversations,
#         'active': active_conversation
#         })
#
#
# @login_required
# def messages(request, username):
#     conversations = Message.get_conversations(user=request.user)
#     active_conversation = username
#     messages = Message.objects.filter(user=request.user, conversation__username=username)
#     messages.update(is_read=True)
#     for conversation in conversations:
#         if conversation['user'].username == username:
#             conversation['unread'] = 0
#     return render(request, 'messages/inbox.html', {
#         'messages': messages,
#         'conversations': conversations,
#         'active': active_conversation
#         })

@login_required
def delete(request):
    return HttpResponse()

# @login_required
# def new(request):
#     if request.method == 'POST':
#         from_user = request.user
#         to_user_username = request.POST.get('person')
#         try:
#             to_user = User.objects.get(username=to_user_username)
#         except Exception:
#             try:
#                 to_user_username = to_user_username[to_user_username.rfind('(')+1:len(to_user_username)-1]
#                 to_user = User.objects.get(username=to_user_username)
#             except Exception:
#                 return redirect('/messages/new/')
#         message = request.POST.get('message')
#         if len(message.strip()) == 0:
#             return redirect('/messages/new/')
#         if from_user != to_user:
#             Message.send_message(from_user, to_user, message)
#             tasks.send_html_mail(to_user.id, 50)
#         return redirect(u'/messages/{0}/'.format(to_user_username))
#
#     else:
#         conversations = Message.get_conversations(user=request.user)
#         return render(request, 'messages/new_modal.html', {'conversations': conversations})
#
#
# @login_required
# def send(request):
#     if request.method == 'POST':
#         from_user = request.user
#         to_user_username = request.POST.get('to')
#         to_user = User.objects.get(username=to_user_username)
#         message = request.POST.get('message')
#         if len(message.strip()) == 0:
#             return HttpResponse()
#         if from_user != to_user:
#             yesterday = date.today() - timedelta(days=1)
#             ms = Message.objects.filter(user=to_user, date__gt=yesterday).count()
#             if ms == 0:
#                 tasks.send_html_mail(to_user.id, 50)
#             msg = Message.send_message(from_user, to_user, message)
#
#             return render(request, 'snippets/partial_message.html', {'message': msg})
#         return HttpResponse()
#     else:
#         return redirect('/')
#
#
# @login_required
# def users(request):
#     users = User.objects.filter(is_active=True)
#     dump = []
#     template = u'{0} ({1})'
#     for user in users:
#         dump.append(user.username)
#     data = json.dumps(dump)
#     return HttpResponse(data, content_type='application/json')
#
#
# @login_required
# def check(request):
#     response = {}
#     response['count'] = Message.objects.filter(user=request.user, is_read=False).count()
#     return HttpResponse(json.dumps(response), content_type="application/json")


@login_required
def send_message(request):
    if request.method == "POST":
        sender = request.user
        message = request.POST.get('message')
        to_user = request.POST.get('person')
        c = request.POST.get('id')
        receiver = User.objects.get(username=to_user)
        conversation = None
        if c:
            conversation = Conversation.objects.get(id=c)
        if conversation:
            m = Message.objects.create(message=message, conversation=conversation, from_user=sender, to_user=receiver)
            conversation.last_message_from=sender
            conversation.is_read = False
            conversation.save()
        else:

            try:
                conversation = Conversation.objects.get(Q(Q(user1=sender) | Q(user2=sender))& Q(Q(user1=receiver) | Q(user2=receiver)))
            except Exception:
                conversation = Conversation.objects.create(user1=sender, user2=receiver)
            m = Message.objects.create(message=message, conversation=conversation, from_user=sender, to_user=receiver)
            conversation.last_message_from=sender
            conversation.is_read = False
            conversation.save()
            return redirect('/messages/')
        return render(request, 'snippets/partial_message.html', {'message': m})

@login_required
def inbox(request):
    user = request.user
    conversations = Conversation.objects.filter(Q(user1=user) | Q(user2=user)).order_by('last_active')

    active_conversation = Conversation.objects.filter(Q(user1=user) | Q(user2=user)).order_by('last_active').last()
    messages = Message.objects.filter(conversation=active_conversation)
    return render(request, 'messages/inbox.html', {
        'messages': messages,
        'conversations': conversations,
        'active': active_conversation
        })

@login_required
def messages(request, id):
    user = request.user.id
    conversations = Conversation.objects.filter(Q(user1=user) | Q(user2=user))
    active_conversation = Conversation.objects.get(id=id)
    active_conversation.is_read = True
    active_conversation.save()
    messages = Message.objects.filter(conversation=active_conversation)

    return render(request, 'messages/inbox.html', {
        'messages': messages,
        'conversations': conversations,
        'active': active_conversation
        })


@login_required
def check(request):
    response = {}
    response['count'] = Conversation.objects.filter(Q(user1=request.user) | Q(user2=request.user)
                                                    , is_read=False).exclude(last_message_from=request.user).count()
    return HttpResponse(json.dumps(response), content_type="application/json")


def create_message_enquiry(message, enquirer, users):
    m = 'You have got an <a href="/enquiry/all/">enquiry message</a>: '+message
    for up in users:

            try:
                conversation = Conversation.objects.get(Q(Q(user1=enquirer) | Q(user2=enquirer))& Q(Q(user1=up.user) | Q(user2=up.user)))
            except Exception:
                conversation = Conversation.objects.create(user1=enquirer, user2=up.user)
            msg = Message.objects.create(message=m, conversation=conversation, from_user=enquirer, to_user=up.user)
            conversation.last_message_from=enquirer
            conversation.is_read = False
            conversation.save()
    return






