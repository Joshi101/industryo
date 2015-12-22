from django.db import models
from tags.models import Tags
from nodes.models import Images
from industryo.unique_slug import unique_slugify
from workplace.models import Workplace
from django.contrib.auth.models import User


class Products(models.Model):
    product = models.CharField(max_length=50)
    producer = models.ForeignKey(Workplace)
    user = models.ForeignKey(User, null=True)
    slug = models.SlugField(max_length=50)
    image = models.ForeignKey(Images, null=True, blank=True)
    tags = models.ManyToManyField(Tags, blank=True)
    description = models.TextField(max_length=1000, null=True, blank=True)
    LargeScaleIndustry = 'A'
    SME = 'B'
    SAE_Team = 'C'
    Educational_Institution = 'O'
    target_segments = (
        (LargeScaleIndustry, 'Large Scale Industry'),
        (SME, 'Small & Medium Scale Enterprise'),
        (SAE_Team, 'SAE Collegiate club'),
        (Educational_Institution, 'Educational Institution')
    )
    target_segment = models.CharField(max_length=4, null=True, blank=True)
    admin_score = models.FloatField(default=1)
    score = models.FloatField(default=0)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True, null=True)

    cost = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = 'Products'

    def __str__(self):
        return self.product

    def save(self, *args, **kwargs):
        if not self.id:                  # Newly created object, so set slug
            slug_str = "%d-%s" % (self.producer.id, self.product)
            unique_slugify(self, slug_str)
            # self.slug = slugify(self.get_full_name()).__str__()
        super(Products, self).save(*args, **kwargs)

    def set_tags(self, tags):
        if tags:
            question_tags = tags.split(',')
            li = []
            for m in question_tags:
                try:
                    t = Tags.objects.get(tag=m)
                except Exception:
                    if len(m) > 2:
                        t = Tags.objects.create(tag=m, type='T')
                li.append(t)
                t.count +=1
                t.save()
            self.tags = li
        return li

    def get_tags(self):
        tags = self.tags.all()
        return tags

    def get_image(self):
        default_image = '/images/main/product.jpg'
        if self.image:
            image_url = '/images/'+str(self.image.image)
            return image_url
        else:
            return default_image

    def get_image_thumbnail(self):
        default_image = '/images/main/product.jpg'
        if self.image:
            image_url = '/images/'+str(self.image.image_thumbnail)
            return image_url
        else:
            return default_image

    def set_target_segments(self, li):
        l = len(li)
        if l == 1:
            q = li[0]
        elif l == 2:
            q = li[0] + li[1]
        elif l == 3:
            q = li[0] + li[1] + li[2]
        else:
            q = li[0] + li[1] + li[2] + li[3]
        self.target_segment = q
        self.save()
        return q





# Create your models here.
