from django.db import models
from industryo.unique_slug import unique_slugify


# type of tags = assets, materials, operations, skills, area

class Tags(models.Model):
    tag = models.CharField(max_length=50, db_index=True)
    tag_types = (('S', 'Segment'), ('C', 'City'), ('E', 'Event'), ('I', 'IndustrialArea'), ('D', 'ProductCategory'),
                 ('A', 'Asset'), ('O', 'Operation'), ('M', 'Material'), ('P', 'ParentInstitution'),)
    type = models.CharField(max_length=1, null=True, blank=True)
    logo = models.ForeignKey('nodes.Images', null=True, blank=True)
    slug = models.SlugField(max_length=50)
    description = models.CharField(max_length=500, null=True, blank=True)
    count = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)
    # related_tags = models.ManyToManyField('self', null=True, blank=True) make provision for showing similar tags

    # popular = models.Manager()

    def __str__(self):
        return self.tag

    def save(self, *args, **kwargs):
        if not self.id:                  # Newly created object, so set slug
            slug_str = self.tag
            unique_slugify(self, slug_str)
            # self.slug = slugify(self.get_full_name()).__str__()
            super(Tags, self).save(*args, **kwargs)

    def get_logo(self):
        default_image = 'images/tags/tag.JPG'
        if self.logo:
            image_url = '/images/'+str(self.profile_image.image_thumbnail)
            return image_url
        else:
            return default_image







# Create your models here.
