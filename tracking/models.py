from django.db import models
from django.contrib.sessions.models import Session


class Tracker(models.Model):
    session = models.ForeignKey(Session, null=True, blank=True)
    source_type = (('1', 'direct'), ('2', 'from_email'), ('3', 'from_some other_SME'), ('4', 'product_snippet'),
                   ('5', 'workplace_snippet'), ('6', 'google_contact_invite'), ('7', 'from referral'))
    source = models.CharField(max_length=2, choices=source_type)
    source_url = models.URLField(null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'Tracker'



# Create your models here.
