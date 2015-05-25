from django.db import models
from workplace.models import Workplace
from nodes.models import Images
from django.db.models.signals import post_save
from django.db.models import signals
from industryo.unique_slug import unique_slugify


class Material(models.Model):
    name = models.CharField(max_length=20)
    slug = models.CharField(max_length=20)

    class Meta:
        db_table = 'Material'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:                  # Newly created object, so set slug
            slug_str = self.name
            unique_slugify(self, slug_str)
            # self.slug = slugify(self.get_full_name()).__str__()
            super(Material, self).save(*args, **kwargs)


class Operation(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'operation'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:                  # Newly created object, so set slug
            slug_str = self.name
            unique_slugify(self, slug_str)
            # self.slug = slugify(self.get_full_name()).__str__()
            super(Operation, self).save(*args, **kwargs)


class Asset(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'Asset'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:                  # Newly created object, so set slug
            slug_str = self.name
            unique_slugify(self, slug_str)
            # self.slug = slugify(self.get_full_name()).__str__()
            super(Asset, self).save(*args, **kwargs)


class Area(models.Model):
    name = models.CharField(max_length=50)
    industrial_area = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        if not self.industrial_area:
            return self.name
        else:
            name = "%s (%s)" % (self.name, self.industrial_area)
            return name


class Events(models.Model):
    event = models.CharField(max_length=50)
    description = models.CharField(max_length=255)
    slug = models.SlugField(max_length=50)

    def __str__(self):
        return self.event

    def save(self, *args, **kwargs):
        if not self.id:                  # Newly created object, so set slug
            slug_str = self.event
            unique_slugify(self, slug_str)
            # self.slug = slugify(self.get_full_name()).__str__()
            super(Events, self).save(*args, **kwargs)


class Institution(models.Model):
    name = models.CharField(max_length=255)
    area = models.ForeignKey(Area)

    def __str__(self):
        return self.name


class WorkplaceProfile(models.Model):
    workplace = models.ForeignKey(Workplace)
    area = models.ForeignKey(Area,null=True)
    address = models.CharField(max_length=255)
    contact = models.CharField(max_length=255)
    about = models.TextField(null=True, blank=True)
    points = models.IntegerField(default=0)
    logo = models.ForeignKey(Images, null=True)
    # Team
    institution = models.ForeignKey(Institution, null=True)
    participation = models.ManyToManyField(Events)
    # SME
    materials = models.ManyToManyField(Material)
    assets = models.ManyToManyField(Asset)
    capabilities = models.TextField(max_length=5000, null=True, blank=True)
    Operation = models.ManyToManyField(Operation)                                ## capital O in next syncdb change to operations
    product_details = models.TextField(max_length=5000, null=True, blank=True)
    # LSI

    def __str__(self):
        return self.workplace.name

    def set_area(self, area):
        # a, created = Area.objects.get_or_create(id=area)
        self.area = area

    def set_institution(self, institution):
        # a, created = Area.objects.get_or_create(id=area)
        # t, created = Institution.objects.get_or_create(id=institution, area=a)
        self.institution = institution

    def create_participation(self, parti):

        part = parti.split(' ')
        li = []
        for p in part:

            t, created = Events.objects.get_or_create(event=p)
            li.append(t)
        self.participation = li

    def set_materials(self, materials):
        material_tags = materials.split(' ')
        li = []
        for m in material_tags:

            t, created = Material.objects.get_or_create(name=m)
            li.append(t)
        self.materials = li

    def set_operations(self, operations):
        operation_tags = operations.split(' ')
        li = []
        for m in operation_tags:

            t, created = Operation.objects.get_or_create(name=m)
            li.append(t)
        self.Operation = li

    def set_assets(self, assets):
        asset_tags = assets.split(' ')
        li = []
        for m in asset_tags:

            t, created = Asset.objects.get_or_create(name=m)
            li.append(t)
        self.assets = li

    # def calculate_points(self):
    #
    #
    #
    # def get_members(self):
    #
    def set_logo(self, image, user):
        i = Images()
        a = i.upload_image(image=image, user=user)

        self.logo = a





def create_workplace_profile(sender, instance, created, **kwargs):
    """Create ModelB for every new ModelA."""
    if created:
        WorkplaceProfile.objects.create(workplace=instance)

signals.post_save.connect(create_workplace_profile, sender=Workplace, weak=False,
                          dispatch_uid='models.create_workplace_profile')








