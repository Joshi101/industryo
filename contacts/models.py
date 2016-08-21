from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from activities.models import Enquiry
import pytz
import random
from workplace.models import Workplace


class ContactEmails(models.Model):
    email = models.EmailField()
    first_name = models.CharField(max_length=20, null=True, blank=True, default='')
    last_name = models.CharField(max_length=20, null=True, blank=True)
    user = models.ForeignKey(User)
    provider = models.CharField(max_length=10)      # google/facebook
    contact_id = models.CharField(max_length=255, null=True, blank=True)        # google
    sent = models.IntegerField(default=0)
    valid = models.BooleanField(default=True)

    class Meta:
        db_table = 'ContactEmail'

    def __str__(self):
        return self.email

    def get_image(self):
        token_id = ""
        a = 'https://www.google.com/m8/feeds/photos/media/{0}/{1}?access_token={2}'.format(self.user.email,
                                                                                           self.contact_id, token_id)
        return a

    def get_first_name(self):
        if self.first_name:
            return self.first_name
        else:
            return ''


class MailSend(models.Model):
    user = models.ForeignKey(User, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    '''
    1: sp@corelogs.com
    2: admin@corelogs.com
    3: info@corelogs.com
    4: marketing@corelogs.com
    '''
    from_email = models.CharField(max_length=1, null=True, blank=True)
    body = models.TextField(max_length=10000, null=True)
    subject = models.CharField(max_length=255, null=True)
    template = models.CharField(max_length=15, null=True)
    arguments = models.CharField(max_length=100, null=True)
    sent = models.BooleanField(default=False)
    reasons = models.CharField(max_length=10, null=True)
    date = models.DateTimeField(auto_now_add=True)
    enquiry = models.ForeignKey(Enquiry, null=True, blank=True)
    random_id = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'MailSend'

    # send initial product upload request - 1 hour after wp register
    # send Second product upload request - Next day
    # send Third product upload request - two days
    # ..
    # send update details of products request
    # send request to add more data like capabilities etc
    # send request to add google contacts
    # send enq mail day1-7
    # send message mail
    # send mail once wp is set, asking review.
    # if no wp set, send , add confirmation template with set wp

    def save(self, *args, **kwargs):
        if not self.id:
            t = self.date
            type = self.from_email
            start_time = t - timedelta(minutes=1)
            end_time = t + timedelta(minutes=1)

            m = MailSend.objects.filter(date__range=[start_time, end_time], from_email=type)
            if len(m) > 7:
                # t = t + timedelta(minutes=3)
                nt = MailSend.objects.last().date
                self.date = nt + timedelta(minutes=1)
                z = MailSend.objects.filter(date__range=[t-timedelta(minutes=30), t+timedelta(minutes=120)], from_email='4')
                if len(z) > 10:
                    q = ['2', '1', '3']
                    self.from_email = random.choice(q)

        super(MailSend, self).save(*args, **kwargs)
        return self.id

    def get_company(self):
        if self.user.userprofile.workplace_type is not 'N':
            company = self.user.userprofile.primary_workplace
        else:
            company = 'CoreLogs'
        return company


class Emails(models.Model):
    email = models.EmailField(unique=True)
    user = models.ForeignKey(User, null=True, blank=True)
    workplace = models.ForeignKey(Workplace, null=True, blank=True)
    workplace_type = models.CharField(max_length=1, default='N')
    date = models.DateTimeField(auto_now_add=True)

    primary_for_user = models.BooleanField(default=False)
    primary_for_workplace = models.BooleanField(default=False)

    deliverable = models.BooleanField(default=True)
    sent = models.IntegerField(default=0)
    opened = models.IntegerField(default=0)

    class Meta:
        db_table = 'Emails'

    def __str__(self):
        return self.email






# Create your models here.
