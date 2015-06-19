from django.db import models
from tags.models import Tags
from nodes.models import Images
from industryo.unique_slug import unique_slugify
from workplace.models import Workplace


class Products(models.Model):
    product = models.CharField(max_length=50)
    producer = models.ForeignKey(Workplace)
    slug = models.SlugField(max_length=50)
    image = models.ForeignKey(Images, null=True, blank=True)
    tags = models.ManyToManyField(Tags)
    description = models.TextField(max_length=1000, null=True, blank=True)

    class Meta:
        db_table = 'Products'

    def __str__(self):
        return self.product

    def save(self, *args, **kwargs):
        if not self.id:                  # Newly created object, so set slug
            slug_str = "%d-%s" % (self.id, self.product)
            unique_slugify(self, slug_str)
            # self.slug = slugify(self.get_full_name()).__str__()
        super(Products, self).save(*args, **kwargs)

    def set_tags(self, tags):
        product_tags = tags.split(',')
        li = []
        for p in product_tags:
            t, created = Tags.objects.get_or_create(tag=p, type='D')
            t.count += 1
            t.save()
            li.append(t)
        self.tags = li

    def get_tags(self):
        tags = self.tags.all()
        return tags

    def get_image(self):
        default_image = '/images/thumbnails/workplace.jpg'
        if self.image:
            image_url = '/images/'+str(self.image.image_thumbnail)
            return image_url
        else:
            return default_image






# Create your models here.
