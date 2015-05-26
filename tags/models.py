from django.db import models
from industryo.unique_slug import unique_slugify


class Tags(models.Model):
    tag = models.CharField(max_length=50)
    logo = models.ForeignKey('nodes.Images', null=True, blank=True)
    slug = models.SlugField(max_length=50)
    type = models.CharField(max_length=50, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    number = models.IntegerField(default=0)
    # type = models.CharField(max_length=1, choices=---)

    # popular = models.Manager()

    def __str__(self):
        return self.tag

    def save(self, *args, **kwargs):
        if not self.id:                  # Newly created object, so set slug
            slug_str = self.tag
            unique_slugify(self, slug_str)
            # self.slug = slugify(self.get_full_name()).__str__()
            super(Tags, self).save(*args, **kwargs)







# Create your models here.
