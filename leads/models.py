from django.db import models
from django.contrib.auth.models import User
from tags.models import Tags
from nodes.models import Images, Document
from industryo.unique_slug import unique_slugify
from activities.models import Activity
from nodes.models import Comments
# from datetime import datetime
from workplace.models import Workplace


class Leads(models.Model):
    lead = models.CharField(max_length=244)
    description = models.CharField(max_length=1000)
    lead_type_o = (('A', 'Product'), ('B', 'Service'))
    lead_type = models.CharField(max_length=1, choices=lead_type_o)
    price_limits = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)      # True= Open
    slug = models.SlugField(max_length=255)

    user = models.ForeignKey(User, null=True, blank=True)
    workplace = models.ForeignKey(Workplace, null=True, blank=True)

    name = models.CharField(max_length=30)
    email = models.CharField(max_length=50)
    company_name = models.CharField(max_length=30)
    mobile_number = models.CharField(max_length=30)

    tags = models.ForeignKey(Tags, null=True, blank=True)

    seen_by = models.IntegerField(default=0)
    responses = models.IntegerField(default=0)

    doc = models.ForeignKey(Document, null=True, blank=True)
    image = models.ForeignKey(Images, null=True, blank=True)

    def __str__(self):
        return self.lead

    def save(self, *args, **kwargs):
        if not self.id:             # Newly created object, so set slug

            slug_str = self.lead
            unique_slugify(self, slug_str)

        super(Leads, self).save(*args, **kwargs)
        return self.id


class Reply(models.Model):
    lead = models.ForeignKey(Leads)
    reply = models.CharField(max_length=1000)
    user = models.ForeignKey(User, null=True, blank=True)
    workplace = models.ForeignKey(Workplace, null=True, blank=True)

    doc = models.ForeignKey(Document, null=True, blank=True)

    def __str__(self):
        return self.reply



