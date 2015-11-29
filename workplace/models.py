from django.db import models
from industryo.unique_slug import unique_slugify
from nodes.models import Images
from tags.models import Tags
from django.contrib.auth.models import User


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

    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    verified = models.BooleanField(default=False)
    slug = models.SlugField(max_length=255)
    address = models.CharField(max_length=255, null=True, blank=True)
    contact = models.CharField(max_length=255, null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    points = models.IntegerField(default=0)
    logo = models.ForeignKey('nodes.Images', null=True, blank=True)

    segments = models.ManyToManyField(Tags, related_name='segments', blank=True)
    # Team
    institution = models.ForeignKey(Tags, related_name='institution', null=True, blank=True)            # don't know why
    # SME
    capabilities = models.TextField(max_length=5000, null=True, blank=True)
    product_details = models.TextField(max_length=5000, null=True, blank=True)

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
        if materials:
            workplace_tags = materials.split(',')
            li = []
            for m in workplace_tags:
                try:
                    t = Tags.objects.get(tag=m)
                except Exception:
                    if len(m) > 2:
                        t = Tags.objects.create(tag=m, type='M')
                li.append(t)
                print(t)
                t.count += 1
                t.save()
            for t in li:
                try:
                    e = WpTags.objects.get(workplace=self, tags=t, category='M')
                except Exception:
                    e = WpTags.objects.create(workplace=self, tags=t, category='M')
            return li

    def set_segments(self, segments):
        if segments:
            workplace_tags = segments.split(',')
            li = []
            for m in workplace_tags:
                try:
                    t = Tags.objects.get(tag=m)
                except Exception:
                    if len(m) > 2:
                        t = Tags.objects.create(tag=m, type='S')
                li.append(t)
                print(t)
                t.count += 1
                t.save()
            for t in li:
                try:
                    e = WpTags.objects.get(workplace=self, tags=t, category='S')
                except Exception:
                    e = WpTags.objects.create(workplace=self, tags=t, category='S')
            return li

    def set_operations(self, operations):
        if operations:
            workplace_tags = operations.split(',')
            li = []
            print('setting operations')
            for m in workplace_tags:
                try:
                    t = Tags.objects.get(tag=m)
                except Exception:
                    if len(m) > 2:
                        t = Tags.objects.create(tag=m, type='O')
                li.append(t)
                print(t)
                t.count += 1
                t.save()
            for t in li:
                try:
                    e = WpTags.objects.get(workplace=self, tags=t, category='O')
                except Exception:
                    e = WpTags.objects.create(workplace=self, tags=t, category='O')
            return li

    # def set_industrial_area(self, industrial_area):
    #     if industrial_area:
    #         workplace_tags = industrial_area.split(',')
    #         li = []
    #         for m in workplace_tags:
    #             try:
    #                 t = Tags.objects.get(tag=m)
    #             except Exception:
    #                 t = Tags.objects.create(tag=m, type='I')
    #             li.append(t)
    #             t.count += 1
    #             t.save()
    #         for t in li:
    #             WpTags.objects.create(workplace=self, tags=t, category='I')
    #         return li

    def set_assets(self, assets):
        if assets:
            workplace_tags = assets.split(',')
            li = []
            for m in workplace_tags:
                try:
                    t = Tags.objects.get(tag=m)
                except Exception:
                    if len(m) > 2:
                        t = Tags.objects.create(tag=m, type='A')
                li.append(t)
                t.count += 1
                t.save()
            for t in li:
                try:
                    e = WpTags.objects.get(workplace=self, tags=t, category='A')
                except Exception:
                    e = WpTags.objects.create(workplace=self, tags=t, category='A')
            return li

    def set_institution(self, institution):
        if institution:
            workplace_tags = institution.split(',')
            li = []
            for m in workplace_tags:
                try:
                    t = Tags.objects.get(tag=m)
                    print('tag exists')
                except Exception:
                    if len(m) > 2:
                        t = Tags.objects.create(tag=m, type='P')
                    print('tag created')
                li.append(t)
                print(t)
                t.count += 1
                t.save()
            for t in li:
                try:
                    e = WpTags.objects.get(workplace=self, tags=t, category='P')
                    print('a')
                    print(e)
                except Exception:
                    e = WpTags.objects.create(workplace=self, tags=t, category='P')
                    print('b')
                    print(e)
            return li

    def set_city(self, city):
        if city:
            workplace_tags = city.split(',')
            li = []
            print('here')
            for m in workplace_tags:
                try:
                    t = Tags.objects.get(tag=m)
                except Exception:
                    if len(m) > 2:
                        t = Tags.objects.create(tag=m, type='C')
                li.append(t)
                print(t)
                t.count += 1
                t.save()
            for t in li:
                try:
                    e = WpTags.objects.get(workplace=self, tags=t, category='C')
                except Exception:
                    e = WpTags.objects.create(workplace=self, tags=t, category='C')
            return li

    def set_events(self, events):
        if events:
            workplace_tags = events.split(',')
            li = []
            for m in workplace_tags:
                try:
                    t = Tags.objects.get(tag=m)
                except Exception:
                    if len(m) > 2:
                        t = Tags.objects.create(tag=m, type='E')
                li.append(t)
                t.count += 1
                t.save()
            for t in li:
                try:
                    e = WpTags.objects.get(workplace=self, tags=t, category='E')
                except Exception:
                    e = WpTags.objects.create(workplace=self, tags=t, category='E')
            return li

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
        o = WpTags.objects.filter(workplace=self, category='O')
        operations = []
        for b in o:
            operations.append(b.tags)

        a = WpTags.objects.filter(workplace=self, category='A')
        assets = []
        for b in a:
            assets.append(b.tags)

        # industrial_area = self.wptags.filter(type='I')
        c = WpTags.objects.filter(workplace=self, category='C')
        city = []
        for b in c:
            city.append(b.tags)

        m = WpTags.objects.filter(workplace=self, category='M')
        materials = []
        for b in m:
            materials.append(b.tags)

        s = WpTags.objects.filter(workplace=self, category='S')
        segments = []
        for b in s:
            segments.append(b.tags)

        e = WpTags.objects.filter(workplace=self, category='E')
        events = []
        for b in e:
            events.append(b.tags)

        i = WpTags.objects.filter(workplace=self, category='P')
        institution = []
        for b in i:
            institution.append(b.tags)
        return locals()

    def get_institution(self):
        institution = self.institution
        return institution

    def get_count(self):
        ups = self.userprofile_set.all()
        count = ups.count()
        return count

    def get_tags_count(self):
        a = self.wptags.all()
        count = len(a)
        return count

    def get_members(self):
        ups = self.userprofile_set.all()
        return ups

    def get_type(self):
        if self.workplace_type == 'A':
            return "Large Scale Industry"
        elif self.workplace_type == 'B':
            return "Small / Medium Scale Enterprise"
        elif self.workplace_type == 'C':
            return "SAE Collegiate Club"
        elif self.workplace_type == 'O':
            return "Educational Institution"


class WpTags(models.Model):
    workplace = models.ForeignKey(Workplace, related_name='w_tags')
    tags = models.ForeignKey(Tags, related_name='wp_relations')
    tag_types = (('S', 'Segment'), ('C', 'City'), ('E', 'Event'), ('I', 'IndustrialArea'), ('D', 'ProductCategory'),
                 ('A', 'Asset'), ('O', 'Operation'), ('M', 'Material'), ('P', 'ParentInstitution'),
                 ('N', 'None'), ('T', 'Topic/Subject'))
    category = models.CharField(max_length=1, choices=tag_types, null=True)

    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        db_table = 'WpTags'

    def get_display(self):
        category = self.category
        if category == 'C':
            return "Exists in this city."
        if category == 'E':
            return "Participates in this Event."
        if category == 'S':
            return "Is related to this Segment."
        if category == 'O':
            return "Performs this Operation."
        if category == 'M':
            return "Deals in this Material"
        if category == 'D':
            return "Deals in this Product Category"
        if category == 'A':
            return "Exists in this city"
        if category == 'I':
            return "Exists in this Industrial Area"
        else:
            return "Oops this was remaining"





# Create your models here.
