from django.db import models
from industryo.unique_slug import unique_slugify
# from nodes.models import Images
from tags.models import Tags


# class Segment(models.Model):
#     name = models.CharField(max_length=255)
#     logo = models.ForeignKey('Images', null=True, blank=True)
#     description = models.TextField(max_length=1000, null=True, blank=True)
#     workplace_type = models.CharField(max_length=1)   # whether LSI, SME or Team
#     slug = models.SlugField(max_length=255)
#
#     class Meta:
#         db_table = 'Segment'
#
#     def __str__(self):
#         return self.name
#
#     def save(self, *args, **kwargs):
#         if not self.id:                  # Newly created object, so set slug
#             slug_str = self.name
#             unique_slugify(self, slug_str)
#             # self.slug = slugify(self.get_full_name()).__str__()
#             super(Segment, self).save(*args, **kwargs)
#
#
# class Events(models.Model):
#     event = models.CharField(max_length=50)
#     description = models.CharField(max_length=1000)
#     slug = models.SlugField(max_length=50)
#
#     def __str__(self):
#         return self.event
#
#     def save(self, *args, **kwargs):
#         if not self.id:                  # Newly created object, so set slug
#             slug_str = self.event
#             unique_slugify(self, slug_str)
#             # self.slug = slugify(self.get_full_name()).__str__()
#             super(Events, self).save(*args, **kwargs)
#
#
# class Institution(models.Model):
#     name = models.CharField(max_length=255)
#     slug = models.SlugField(max_length=50, null=True, blank=True)
#
#     area = models.ForeignKey(Area)
#
#     def __str__(self):
#         return self.name

#
# class Area(models.Model):
#     name = models.CharField(max_length=50)
#     description = models.CharField(max_length=1000)
#     industrial_area = models.CharField(max_length=50, null=True, blank=True)
#     slug = models.SlugField(max_length=50, null=True, blank=True)
#
#     def __str__(self):
#         if not self.industrial_area:
#             return self.name
#         else:
#             name = "%s (%s)" % (self.name, self.industrial_area)
#             return name
#
#     def save(self, *args, **kwargs):
#         if not self.id:                  # Newly created object, so set slug
#             slug_str = self.name
#             unique_slugify(self, slug_str)
#             # self.slug = slugify(self.get_full_name()).__str__()
#             super(Area, self).save(*args, **kwargs)


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

    # def set_materials(self, materials):
    #     material_tags = materials.split(' ')
    #     li = []
    #     for m in material_tags:
    #         t, created = Tags.objects.get_or_create(name=m, type="materials")
    #         li.append(t)
    #     self.tags = li
    #
    # def set_operations(self, operations):
    #     operation_tags = operations.split(' ')
    #     li = []
    #     st = []
    #     for p in operation_tags:
    #
    #         t, created = Tags.objects.get_or_create(name=p)
    #         m, created = Tags.objects.get_or_create(tag=p, type="operations")
    #         li.append(t)
    #         st.append(m)
    #     self.area = li
    #     self.tags = st
    #
    # def set_area(self, area):
    #     areas = area.split(' ')
    #     li = []
    #     st = []
    #     for p in areas:
    #
    #         t, created = Area.objects.get_or_create(event=p)
    #         m, created = Tags.objects.get_or_create(tag=p, type="area")
    #         li.append(t)
    #         st.append(m)
    #     self.area = li
    #     self.tags = st
    #
    # def set_assets(self, assets):
    #     asset_tags = assets.split(' ')
    #     li = []
    #     for p in asset_tags:
    #         t, created = Tags.objects.get_or_create(name=p, type="assets")
    #         li.append(t)
    #     self.tags = li

    # def set_logo(self, image, user):
    #     i = Images()
    #     a = i.upload_image(image=image, user=user)
    #
    #     self.logo = a

    # def set_institution(self, institution):
    #     # a, created = Area.objects.get_or_create(id=area)
    #     # t, created = Institution.objects.get_or_create(id=institution, area=a)
    #     self.institution = institution
    #
    # def create_participation(self, parti):
    #
    #     part = parti.split(' ')
    #     li = []
    #     st = []
    #     for m in part:
    #
    #         t, created = Events.objects.get_or_create(event=m)
    #         p, created = Tags.objects.get_or_create(tag=m, type="event")
    #         li.append(t)
    #         st.append(p)
    #     self.participation = li
    #
    #





# Create your models here.
