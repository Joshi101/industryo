from django.db import models
from tags.models import Tags
from nodes.models import Images
from industryo.unique_slug import unique_slugify
from workplace.models import Workplace
from django.contrib.auth.models import User


class SellManager(models.Manager):
    def get_queryset(self):
        return super(SellManager, self).get_queryset().\
            filter(status=1).order_by('-date')     # .order_by('-score', '-date')


class RentManager(models.Manager):
    def get_queryset(self):
        return super(RentManager, self).get_queryset().\
            filter(status=2).order_by('-date')


class SellSMEManager(models.Manager):
    def get_queryset(self):
        return super(SellSMEManager, self).get_queryset().\
            filter(target_segment__contains='B', status=1).order_by('-date')


class Products(models.Model):
    product = models.CharField(max_length=50)
    producer = models.ForeignKey(Workplace)
    user = models.ForeignKey(User, null=True)
    slug = models.SlugField(max_length=50)
    image = models.ForeignKey(Images, null=True, blank=True)
    tags = models.ManyToManyField(Tags, blank=True)
    description = models.TextField(max_length=1000, null=True, blank=True)
    LargeScaleIndustry = 'A'
    SME = 'B'
    SAE_Team = 'C'
    Educational_Institution = 'O'
    target_segments = (
        (LargeScaleIndustry, 'Large Scale Industry'),
        (SME, 'Small & Medium Scale Enterprise'),
        (SAE_Team, 'SAE Collegiate club'),
        (Educational_Institution, 'Educational Institution')
    )
    target_segment = models.CharField(max_length=4, null=True, blank=True)
    admin_score = models.FloatField(default=1)
    score = models.FloatField(default=0)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True, null=True)

    #new
    status = models.CharField(max_length=1, default=1)     # 0=showcase, 1=sell, 2 rent
    cost = models.CharField(max_length=50, null=True, blank=True)
    # offer = models.CharField(max_length=500, null=True, blank=True)

    # type = models.CharField(max_length=1, default=1)    # 0=single item sellable, 1=Bulk produce, 2 service
    categorisation = models.CharField(max_length=10, null=True, blank=True)

    categories = models.ManyToManyField('Category', through='Product_Categories', null=True, blank=True)

    objects = models.Manager()
    sell = SellManager()
    rent = RentManager()
    sell_SME = SellSMEManager()

    class Meta:
        db_table = 'Products'

    def __str__(self):
        return self.product

    def save(self, *args, **kwargs):
        if not self.id:                  # Newly created object, so set slug
            slug_str = "%d-%s" % (self.producer.id, self.product)
            unique_slugify(self, slug_str)
            # self.slug = slugify(self.get_full_name()).__str__()
        super(Products, self).save(*args, **kwargs)

    def set_tags(self, tags):
        if tags:
            question_tags = tags.split(',')
            li = []
            for m in question_tags:
                try:
                    t = Tags.objects.get(tag__iexact=m) # iexact
                    print(t)
                except Exception:
                    if len(m) > 2:
                        t = Tags.objects.create(tag=m, type='D')
                li.append(t)
                t.count +=1
                t.save()
            self.tags = li

    def get_tags(self):
        tags = self.tags.all()
        return tags

    def get_image(self):
        default_image = '/images/main/product.png'
        if self.image:
            image_url = '/images/'+str(self.image.image)
            return image_url
        else:
            return default_image

    def get_image_thumbnail(self):
        default_image = '/images/main/product.png'
        if self.image:
            image_url = '/images/'+str(self.image.image_thumbnail)
            return image_url
        else:
            return default_image

    def set_target_segments(self, li):
        l = len(li)
        if l == 1:
            q = li[0]
            self.target_segment = q
            self.target_segment = q
        elif l == 2:
            q = li[0] + li[1]
            self.target_segment = q
            self.target_segment = q

        elif l == 3:
            q = li[0] + li[1] + li[2]
            self.target_segment = q
            self.target_segment = q
        elif l == 4:
            q = li[0] + li[1] + li[2] + li[3]
            self.target_segment = q
            self.target_segment = q
        else:
            pass
        self.save()

    def get_status(self):
        if self.status == '0':
            status = 'Showcase Item'
        elif self.status == '1':
            status = 'For Sale'
        else:
            status = 'For Rent'
        return status

    def get_category1(self):
        try:
            category1 = self.categories.get(level=1)
            c1 = category1.id
        except Exception:
            c1 = None
        return c1

    def get_category2(self):
        try:
            category1 = self.categories.get(level=2)
            c1 = category1.id
        except Exception:
            c1 = None
        return c1

    def get_category3(self):
        try:
            category1 = self.categories.get(level=3)
            c1 = category1.id
        except Exception:
            c1 = None
        return c1

    def get_cat(self):
        categories = self.categories.all()
        return categories


class Category(models.Model):
    name = models.CharField(max_length=70)
    level = models.CharField(max_length=1)
    slug = models.SlugField(null=True, blank=True)
    # cascade = models.ForeignKey('self', null=True, blank=True)
    sub_cat = models.ManyToManyField('self', null=True, blank=True)
    alpha = models.CharField(max_length=2)
    meta_des = models.CharField(max_length=160, null=True, blank=True)
    tag = models.ForeignKey(Tags, null=True, blank=True)
    image = models.ForeignKey(Images, null=True, blank=True)
    # count = models.IntegerField(null=True, blank=True)

    class Meta:
        db_table = 'Category'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:                  # Newly created object, so set slug
            slug_str = self.name
            unique_slugify(self, slug_str)
            # self.slug = slugify(self.get_full_name()).__str__()
        super(Category, self).save(*args, **kwargs)

    def get_sub(self):
        n = self.level
        sub = self.sub_cat.filter(level__gt=n)
        return sub

    def set_sub(self, c):
        print("dsasadasdAS")
        f= [c]
        self.sub_cat = f
        return c


class Product_Categories(models.Model):
    product = models.ForeignKey(Products)
    category = models.ForeignKey(Category)
    level = models.CharField(max_length=1)

    class Meta:
        db_table = 'Product_Categories'








# Create your models here.
