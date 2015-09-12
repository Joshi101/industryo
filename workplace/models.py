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
    Educational_Institution = 'O'
    Workplace_Type = (
        (LargeScaleIndustry, 'Large Scale Industry'),
        (SME, 'Small & Medium Scale Enterprise'),
        (SAE_Team, 'SAE Collegiate club'),
        (Educational_Institution, 'Educational Institution')
    )
    workplace_type = models.CharField(max_length=1, choices=Workplace_Type)

    verified = models.BooleanField(default=False)
    slug = models.SlugField(max_length=255)
    address = models.CharField(max_length=255, null=True, blank=True)
    contact = models.CharField(max_length=255, null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    points = models.IntegerField(default=0)
    logo = models.ForeignKey('nodes.Images', null=True, blank=True)

    segments = models.ManyToManyField(Tags, related_name='segments')
    # Team
    institution = models.ForeignKey(Tags, related_name='institution', null=True, blank=True)            # don't know why
    # SME
    capabilities = models.TextField(max_length=5000, null=True, blank=True)
    product_details = models.TextField(max_length=5000, null=True, blank=True)
    # tags = models.ManyToManyField(Tags)
    wptags = models.ManyToManyField(Tags, through='WpTags', related_name='wptags')

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
        try:
            t = Tags.objects.get(tag=materials)
        except Exception:
            t = Tags.objects.create(tag=materials, type='M')
        WpTags.objects.create(workplace=self, tags=t, category='M')
        t.count += 1
        t.save()
        return t

    def set_segments(self, segments):
        try:
            t = Tags.objects.get(tag=segments)
        except Exception:
            t = Tags.objects.create(tag=segments, type='S')
        WpTags.objects.create(workplace=self, tags=t, category='S')
        t.count += 1
        t.save()
        return t

    def set_operations(self, operations):
        try:
            t = Tags.objects.get(tag=operations)
        except Exception:
            t = Tags.objects.create(tag=operations, type='O')
        WpTags.objects.create(workplace=self, tags=t, category='O')
        t.count += 1
        t.save()
        return t

    def set_industrial_area(self, industrial_area):
        try:
            t = Tags.objects.get(tag=industrial_area)
        except Exception:
            t = Tags.objects.create(tag=industrial_area, type='I')
        WpTags.objects.create(workplace=self, tags=t, category='I')
        t.count += 1
        t.save()
        return t

    def set_assets(self, assets):
        try:
            t = Tags.objects.get(tag=assets)
        except Exception:
            t = Tags.objects.create(tag=assets, type='A')
        WpTags.objects.create(workplace=self, tags=t, category='A')
        t.count += 1
        t.save()
        return t

    def set_institution(self, institution):
        try:
            t = Tags.objects.get(tag=institution)
        except Exception:
            t = Tags.objects.create(tag=institution, type='P')
        WpTags.objects.create(workplace=self, tags=t, category='P')
        self.institution = t
        t.count += 1
        t.save()
        return t

    def set_city(self, city):
        try:
            t = Tags.objects.get(tag=city)
        except Exception:
            t = Tags.objects.create(tag=city, type='C')
        WpTags.objects.create(workplace=self, tags=t, category='C')
        t.count += 1
        t.save()
        return t

    def set_events(self, events):
        try:
            t = Tags.objects.get(tag=events)
        except Exception:
            t = Tags.objects.create(tag=events, type='E')
        WpTags.objects.create(workplace=self, tags=t, category='E')
        t.count +=1
        t.save()
        return t

    def set_logo(self, image, user):
        i = Images()
        a = i.upload_image(image=image, user=user)
        self.logo = a

    def get_city(self):
        city = self.wptags.filter(type='C')
        return city

    def get_logo(self):
        default_image = '/images/thumbnails/logo.JPG'
        if self.logo:
            image_url = '/images/'+str(self.logo.image_thumbnail)
            return image_url
        else:
            return default_image

    def get_tags(self):
        operations = self.wptags.filter(type='O')
        assets = self.wptags.filter(type='A')
        industrial_area = self.wptags.filter(type='I')
        city = self.wptags.filter(type='C')
        materials = self.wptags.filter(type='M')
        segments = self.wptags.filter(type='S')
        events = self.wptags.filter(type='E')
        institution = self.wptags.filter(type='P')
        return locals()

    def get_institution(self):
        institution = self.institution
        return institution


class WpTags(models.Model):
    workplace = models.ForeignKey(Workplace, related_name='w_tags')
    tags = models.ForeignKey(Tags, related_name='wp_relations')
    tag_types = (('S', 'Segment'), ('C', 'City'), ('E', 'Event'), ('I', 'IndustrialArea'), ('D', 'ProductCategory'),
                 ('A', 'Asset'), ('O', 'Operation'), ('M', 'Material'), ('P', 'ParentInstitution'),
                 ('N', 'None'), ('T', 'Topic/Subject'))
    category = models.CharField(max_length=1, choices=tag_types, null=True)

    class Meta:
        db_table = 'WpTags'





# Create your models here.
