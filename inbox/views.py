from django.shortcuts import render
from leads.models import Leads, Reply
from chat.models import Conversation, Message
from activities.models import Enquiry
from django.contrib.auth.decorators import login_required


@login_required
def inbox(request):
    user = request.user
    
    return render(request, 'inbox/inbox.html', locals())

# Create your views here.
