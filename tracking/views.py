from django.shortcuts import render
from .models import Tracker
from datetime import datetime, timedelta


def get_data(request):
    now = datetime.now()
    last_week_mail = Tracker.objects.filter(date__range=[now-timedelta(days=7), now], source='2')
    last_week_direct = Tracker.objects.filter(date__range=[now-timedelta(days=7), now], source='1')
    last_week_sos = Tracker.objects.filter(date__range=[now-timedelta(days=7), now], source='3')
    last_week_gci = Tracker.objects.filter(date__range=[now-timedelta(days=7), now], source='6')
    last_week_referral = Tracker.objects.filter(date__range=[now-timedelta(days=7), now], source='7')
    return render(request, 'trackind/data.html', locals())



# Create your views here.
