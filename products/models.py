from django.db import models
from nodes.models import Images
from tags.models import Tags
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

    def add_image(self, image, user):
        i = Images()
        a = i.upload_image(image=image, user=user)
        self.image = a







# Create your models here.
