from django.db import models
from industryo.unique_slug import unique_slugify
from datetime import datetime


class Tags(models.Model):
    tag = models.CharField(max_length=50, db_index=True)
    other_names = models.CharField(max_length=1000, null=True, blank=True)
    tag_types = (('S', 'Segment'), ('C', 'City'), ('E', 'Event'), ('I', 'IndustrialArea'), ('D', 'ProductCategory'),
                 ('A', 'Asset'), ('O', 'Operation'), ('M', 'Material'), ('P', 'ParentInstitution'),
                 ('N', 'None'), ('T', 'Topic/Subject'))
    type = models.CharField(max_length=1, choices=tag_types, null=True, default='T')
    logo = models.ForeignKey('nodes.Images', null=True, blank=True)
    slug = models.SlugField(max_length=50)
    description = models.CharField(max_length=500, null=True, blank=True)
    count = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)

    related_tags = models.ManyToManyField('self', through='TagRelations', symmetrical=False) # make provision for showing similar tags

    date = models.DateTimeField(auto_now_add=True) # default=datetime.now()

    def __str__(self):
        return self.tag

    def get_detail(self):
        detail = "%s (%s)" % (self.tag, self.type)
        return detail

    def save(self, *args, **kwargs):
        if not self.id:                  # Newly created object, so set slug
            slug_str = self.tag
            unique_slugify(self, slug_str)
            # self.slug = slugify(self.get_full_name()).__str__()
        super(Tags, self).save(*args, **kwargs)

    def get_logo(self):
        default_image = '/images/thumbnails/image.png'
        if self.logo:
            image_url = '/images/'+str(self.logo.image_thumbnail)
            return image_url
        else:
            return default_image

    def get_image(self):
        default_image = '/images/main/image.png'
        if self.logo:
            image_url = '/images/'+str(self.logo.image)
            return image_url
        else:
            return default_image

    def get_type(self):
        if self.type == 'A':
            return "Asset"
        elif self.type == 'C':
            return "City"
        elif self.type == 'S':
            return "Industry Segment"
        elif self.type == 'E':
            return "Event"
        elif self.type == 'I':
            return "Industrial Area"
        elif self.type == 'D':
            return "Product Category"
        elif self.type == 'O':
            return "Operation"
        elif self.type == 'M':
            return "Material"
        elif self.type == 'P':
            return "Institution"
        elif self.type == 'T':
            return "Topic / Subject"
        else:
            return "Not specified, Please specify"

    def set_relation(self, tag1, tag2):
        try:
            o = TagRelations.objects.filter(tag1=tag1, tag2=tag2).first()

            if o:
                p = o.count
                o.count = p+1
                o.save()
        except Exception:
            o = TagRelations.objects.filter(tag2=tag1, tag1=tag2).first()

            if o:
                p = o.count
                o.count = p+1
                o.save()
        finally:
            t, created = TagRelations.objects.get_or_create(tag1=tag1, tag2=tag2)
            if not created:
                t.count +=1
                t.save()


class TagRelations(models.Model):
    tag1 = models.ForeignKey(Tags, related_name='+')
    tag2 = models.ForeignKey(Tags, related_name='+')
    count = models.IntegerField(default=1)

    class Meta:
        db_table = 'TagRelations'



# Create your models here.
