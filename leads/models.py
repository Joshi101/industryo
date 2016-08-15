from django.db import models
from django.contrib.auth.models import User
from tags.models import Tags
from nodes.models import Images, Document
from industryo.unique_slug import unique_slugify
from workplace.models import Workplace
from activities.models import Enquiry


class Leads(models.Model):
    lead = models.CharField(max_length=244)
    description = models.CharField(max_length=1000, null=True, blank=True)
    lead_type_o = (('A', 'Product'), ('B', 'Service'), ('D', 'Dashboard'))
    lead_type = models.CharField(max_length=1, choices=lead_type_o, null=True, blank=True)
    price_limits = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)      # True= Open
    slug = models.SlugField(max_length=255)
    anonymous = models.BooleanField(default=True)

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
            self.tags.add(*li)
            return li

    def get_tags(self):
        tags = self.tags.all()
        return tags

    def get_quotation_count(self):
        c = 0
        c = Reply.objects.filter(lead=self).count()
        return c


class Reply(models.Model):
    lead = models.ForeignKey(Leads, null=True, blank=True)
    to_user = models.ForeignKey(User, related_name='+', null=True, blank=True)
    inquiry = models.ForeignKey(Enquiry, null=True, blank=True)

    user = models.ForeignKey(User, null=True, blank=True)
    workplace = models.ForeignKey(Workplace, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, null=True)

    message = models.CharField(max_length=1000, null=True, blank=True)
    price = models.CharField(max_length=100, null=True, blank=True)
    taxes = models.CharField(max_length=100, null=True, blank=True)
    time_to_deliver = models.CharField(max_length=100, null=True, blank=True)
    delivery_charges = models.CharField(max_length=100, null=True, blank=True)
    payment_terms = models.CharField(max_length=100, null=True, blank=True)
    quality_assurance = models.CharField(max_length=255, null=True, blank=True)

    selected = models.BooleanField(default=False)
    seen = models.BooleanField(default=False)

    doc1 = models.ForeignKey(Document, related_name='doc1', null=True, blank=True)
    doc2 = models.ForeignKey(Document, related_name='doc2', null=True, blank=True)

    def __str__(self):
        return self.message
