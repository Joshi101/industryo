from django.db import models
from industryo.unique_slug import unique_slugify
from nodes.models import Images
from tags.models import Tags
# from userprofile.models import UserProfile


class Workplace(models.Model):
    name = models.CharField(max_length=255)
    LargeScaleIndustry = 'A'
    SME = 'B'
    SAE_Team = 'C'
    Others = 'O'
    Workplace_Type = (
        (LargeScaleIndustry, 'Large Scale Industry'),
        (SME, 'Small & Medium Scale Enterprise'),
        (SAE_Team, 'College Teams'),
        (Others, 'Others')
    )
    workplace_type = models.CharField(max_length=1, choices=Workplace_Type)

    verified = models.BooleanField(default=False)
    slug = models.SlugField(max_length=255)
    # area = models.ManyToManyField(Tags, related_name='area')
    address = models.CharField(max_length=255, null=True, blank=True)
    contact = models.CharField(max_length=255, null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    points = models.IntegerField(default=0)
    logo = models.ForeignKey('nodes.Images', null=True, blank=True)

    segments = models.ManyToManyField(Tags, related_name='segments')
    # Team
    institution = models.ForeignKey(Tags, related_name='institution', null=True, blank=True)            # don't know why
    # participation = models.ManyToManyField(Tags, related_name='participation')
    # SME
    capabilities = models.TextField(max_length=5000, null=True, blank=True)
    product_details = models.TextField(max_length=5000, null=True, blank=True)

    tags = models.ManyToManyField(Tags)

    class Meta:
        db_table = 'Workplace'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:                  # Newly created object, so set slug
            slug_str = self.name
            unique_slugify(self, slug_str)
            # self.slug = slugify(self.get_full_name()).__str__()
        super(Workplace, self).save(*args, **kwargs)

    def set_materials(self, materials):
        t, created = Tags.objects.get_or_create(tag=materials, type='M')
        self.tags.add(t)
        t.count +=1
        t.save()
        return t

    def set_segments(self, materials):
        t, created = Tags.objects.get_or_create(tag=materials, type='S')
        self.tags.add(t)
        t.count +=1
        t.save()
        return t

    def set_operations(self, operations):
        t, created = Tags.objects.get_or_create(tag=operations, type='O')
        self.tags.add(t)
        t.count +=1
        t.save()
        return t

    def set_industrial_area(self, industrial_area):
        t, created = Tags.objects.get_or_create(tag=industrial_area, type='I')
        self.tags.add(t)
        t.count +=1
        t.save()
        return t

    def set_assets(self, assets):
        t, created = Tags.objects.get_or_create(tag=assets, type='A')
        self.tags.add(t)
        t.count +=1
        t.save()
        return t

    def set_institution(self, institution):
        t, created = Tags.objects.get_or_create(tag=institution, type='P')
        self.tags.add(t)
        self.institution = t
        t.count +=1
        t.save()
        return t

    def set_city(self, city):
        t, created = Tags.objects.get_or_create(tag=city, type='C')
        self.tags.add(t)
        t.count +=1
        t.save()
        return t

    def set_events(self, events):
        t, created = Tags.objects.get_or_create(tag=events, type='E')
        self.tags.add(t)
        t.count +=1
        t.save()
        return t

    def set_logo(self, image, user):
        i = Images()
        a = i.upload_image(image=image, user=user)
        self.logo = a

    def get_city(self):
        city = self.tags.filter(type='C')
        return city

    def get_logo(self):
        default_image = '/images/thumbnails/workplace.jpg'
        if self.logo:
            image_url = '/images/'+str(self.logo.image_thumbnail)
            return image_url
        else:
            return default_image

    def get_tags(self):
        operations = self.tags.filter(type='O')
        assets = self.tags.filter(type='A')
        industrial_area = self.tags.filter(type='I')
        city = self.tags.filter(type='C')
        materials = self.tags.filter(type='M')
        segments = self.tags.filter(type='S')
        events = self.tags.filter(type='E')
        institution = self.tags.filter(type='P')
        return locals()

    def get_institution(self):
        institution = self.institution
        return institution





# Create your models here.
