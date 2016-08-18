from django.shortcuts import render, HttpResponse
from .models import Tracker, Referral
from datetime import datetime, timedelta
from contacts.models import MailSend
from datetime import datetime
from home.templates import join_corelogs_mail


def get_data(request):
    now = datetime.now()
    last_week_mail = Tracker.objects.filter(date__range=[now-timedelta(days=7), now], source='2')
    last_week_direct = Tracker.objects.filter(date__range=[now-timedelta(days=7), now], source='1')
    last_week_sos = Tracker.objects.filter(date__range=[now-timedelta(days=7), now], source='3')
    last_week_gci = Tracker.objects.filter(date__range=[now-timedelta(days=7), now], source='6')
    last_week_referral = Tracker.objects.filter(date__range=[now-timedelta(days=7), now], source='7')
    return render(request, 'trackind/data.html', locals())


def refer(request):
    if request.method == 'POST':
        user = request.user
        now = datetime.now()
        subject = '{0} Invited You to join the network of SMEs'.format(user.userprofile)
        # mail_body = join_corelogs_mail.format(user.userprofile)
        # emails = request.POST.get('emails')
        li = []
        for key in request.POST:
            if '@' in request.POST[key]:
                li.append(request.POST[key])
        print(li)
        if li:
            # MailSend.objects.create(user=user, emails=li, reasons='jcm', subject=subject, date=now, body=mail_body,
            #                         from_email='3')
            for e in li:
                r = Referral.objects.create(email=e, user=user)
        return HttpResponse()
    else:
        return render(request, 'refer.html')




# Create your views here.
