from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from activities.models import Enquiry
import pytz


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
    body = models.TextField(max_length=10000, null=True)
    subject = models.CharField(max_length=255, null=True)
    template = models.CharField(max_length=15, null=True)
    arguments = models.CharField(max_length=100, null=True)
    sent = models.BooleanField(default=False)
    reasons = models.CharField(max_length=10, null=True)
    date = models.DateTimeField(default=datetime.now(pytz.utc))
    enquiry = models.ForeignKey(Enquiry, null=True, blank=True)

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













# Create your models here.
