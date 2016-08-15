from django.db import models
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User


class Tracker(models.Model):
    session = models.ForeignKey(Session, null=True, blank=True)
    source_type = (('1', 'direct'), ('2', 'from_email'), ('3', 'from_some other_SME'), ('4', 'product_snippet'),
                   ('5', 'workplace_snippet'), ('6', 'google_contact_invite'), ('7', 'from referral'))
    source = models.CharField(max_length=2, choices=source_type, null=True, blank=True)
    source_url = models.URLField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Tracker'


class Referral(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=30, null=True, blank=True)
    company = models.CharField(max_length=40, null=True, blank=True)

    user = models.ForeignKey(User)

    deliverable = models.BooleanField(default=True)
    sent = models.SmallIntegerField(default=0)
    opened = models.SmallIntegerField(default=0)
    joined = models.BooleanField(default=False)

    class Meta:
        db_table = 'Referral'

    def __str__(self):
        return self.email
# Create your models here.
