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
    description = models.CharField(max_length=1000, null=True, blank=True)
    lead_type_o = (('A', 'Product'), ('B', 'Service'), ('D', 'Dashboard'))
    lead_type = models.CharField(max_length=1, choices=lead_type_o, null=True, blank=True)
    price_limits = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)      # True= Open
    slug = models.SlugField(max_length=255)

    user = models.ForeignKey(User, null=True, blank=True)
    workplace = models.ForeignKey(Workplace, null=True, blank=True)

    name = models.CharField(max_length=30, null=True, blank=True)
    email = models.CharField(max_length=50, null=True, blank=True)
    company_name = models.CharField(max_length=30, null=True, blank=True)
    mobile_number = models.CharField(max_length=30, null=True, blank=True)

    tags = models.ManyToManyField(Tags, null=True, blank=True)

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

    def get_image(self):
        if self.image:
            image_url = '/images/'+str(self.image.image)
            return image_url

    def set_tags(self, tags):
        if tags:
            lead_tags = tags.split(',')
            li = []
            for m in lead_tags:
                try:
                    t = Tags.objects.get(tag__iexact=m)
                except Exception:
                    if len(m) > 2:
                        t = Tags.objects.create(tag=m, type='T')
                li.append(t)
                t.count += 1
                t.save()
            self.tags = li
            return li


    def get_tags(self):
        tags = self.tags.all()
        return tags


class Reply(models.Model):
    lead = models.ForeignKey(Leads)
    reply = models.CharField(max_length=1000)
    user = models.ForeignKey(User, null=True, blank=True)
    workplace = models.ForeignKey(Workplace, null=True, blank=True)

    doc = models.ForeignKey(Document, null=True, blank=True)

    def __str__(self):
        return self.reply


