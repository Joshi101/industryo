from django.shortcuts import HttpResponse
from django.template.loader import render_to_string
from chat.models import Message, Conversation
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import json
from datetime import datetime
from activities.models import Enquiry


@login_required
def delete(request):
    return HttpResponse()


@login_required
def send_message(request):
    sender = request.user
    message = request.POST.get('message')
    to_user = request.POST.get('person')
    subject = request.POST.get('subject')
    c = request.POST.get('id')
    receiver = User.objects.get(username=to_user)

    conversation = Conversation.objects.create(user1=sender, user2=receiver, subject=subject)
    m = Message.objects.create(message=message, conversation=conversation, from_user=sender, to_user=receiver)
    conversation.last_message_from = sender
    conversation.last_message_to = receiver
    conversation.last_active = datetime.now()
    conversation.save()
    response = {}
    response['msg'] = render_to_string('inbox/one_msg.html', {'msg': m})
    return HttpResponse(json.dumps(response), content_type="application/json")


@login_required
def reply(request):
    conversation = Conversation.objects.get(id=request.POST.get('id'))
    message = request.POST.get('message')
    sender = request.user
    li = [conversation.user1, conversation.user2]
    li.remove(sender)
    receiver = li[0]
    m = Message.objects.create(message=message, conversation=conversation, from_user=sender, to_user=receiver)
    conversation.last_message_from = sender
    conversation.last_message_to = receiver
    conversation.last_active = datetime.now()
    conversation.save()
    response = {}
    response['msg'] = render_to_string('inbox/one_msg.html', {'msg': m})
    return HttpResponse(json.dumps(response), content_type="application/json")


# def forward()


def send_reply_to(from_user, to_user, subject, message):
    c = Conversation.objects.create(from_user=from_user, to_user=to_user, subject=subject, last_message_from=from_user,
                                    last_message_to=to_user, last_active=datetime.now())
    m = Message.objects.create(from_user=from_user, to_user=to_user, message=message)
    # c.save()
    return c
