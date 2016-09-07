from django.db import models
from tags.models import Tags
from nodes.models import Images
from industryo.unique_slug import unique_slugify
from workplace.models import Workplace
from django.contrib.auth.models import User
import traceback
import os.path


class SellManager(models.Manager):
    def get_queryset(self):
        return super(SellManager, self).get_queryset().\
            filter(status=1).order_by('-date')     # .order_by('-score', '-date')


class RentManager(models.Manager):
    def get_queryset(self):
        return super(RentManager, self).get_queryset().\
            filter(status=2).order_by('-date')


class Products(models.Model):
    product = models.CharField(max_length=100)
    producer = models.ForeignKey(Workplace)
    user = models.ForeignKey(User, null=True)
    slug = models.SlugField(max_length=50)
    image = models.ForeignKey(Images, null=True, blank=True)
    tags = models.ManyToManyField(Tags, blank=True)
    description = models.TextField(max_length=10000, null=True, blank=True)

    admin_score = models.FloatField(default=1)
    score = models.FloatField(default=0)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True, null=True)

    status = models.CharField(max_length=1, default=1)     # 0=showcase, 1=sell, 2 rent
    cost = models.CharField(max_length=50, null=True, blank=True)
    # offer = models.CharField(max_length=500, null=True, blank=True)
    Single_item = 'A'
    Bulk = 'B'
    Service = 'C'
    product_types = ((Single_item, 'Single Item Sale'), (Bulk, 'Bulk Product'), (Service, 'Service'),)
    product_type = models.CharField(max_length=1, choices=product_types, null=True, blank=True)

    delivery_details = models.CharField(max_length=200, blank=True, null=True)
    delivery_charges = models.CharField(max_length=200, blank=True, null=True)
    minimum = models.CharField(max_length=200, blank=True, null=True)

    categories = models.ManyToManyField('Category', through='Product_Categories', blank=True)

    available = models.BooleanField(default=True)
    manufactured = models.BooleanField(default=True)

    objects = models.Manager()
    sell = SellManager()
    rent = RentManager()
    # sell_SME = SellSMEManager()

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

    def get_image(self):
        default_image = '/images/main/product.png'
        if self.image:
            image_url = '/images/'+str(self.image.image)
            return image_url
        else:
            return default_image

    def get_image_thumbnail(self):
        default_image = '/images/product.png'
        if self.image:
            image_url = '/images/'+str(self.image.image_thumbnail)
            return image_url
        else:
            return default_image

    def get_status(self):
        if self.status == '0':
            status = 'Showcase Item'
        elif self.status == '1':
            status = 'For Sale'
        else:
            status = 'For Rent'
        return status

    def get_type(self):
        type = None
        if self.product_type == 'A':
            type = 'Single Item'
        elif self.product_type == 'B':
            type = 'Bilk Item'
        elif self.product_type == 'C':
            type = 'Service'
        return type

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

    def set_categories(self, li):
        categories = Category.objects.filter(pk__in=li)
        for c in categories:
            try:
                l = Product_Categories.objects.filter(product=self, level=c.level)
            except Exception:
                tb = traceback.format_exc()
                print(tb)

            if l:
                if len(l) == 1:
                    q = l[0]
                    q.category = c
                    q.save()
                else:
                    pass
            else:
                try:
                    Product_Categories.objects.create(product=self, category=c, level=c.level)
                except:
                    tb = traceback.format_exc()
                    print(tb)

        return categories

    def set_prod_category(self, c):
        if c:
            for t in c:
                Product_Categories.objects.create(product=self, category=t.category, level=t.level)


class Category(models.Model):
    name = models.CharField(max_length=70)
    level = models.PositiveSmallIntegerField()
    slug = models.SlugField(null=True, blank=True)
    sub_cat = models.ManyToManyField('self', blank=True)
    alpha = models.CharField(max_length=2, null=True, blank=True)
    meta_des = models.CharField(max_length=150, null=True, blank=True)
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

    def get_cats(self):
        lvl = self.level
        cats = self.sub_cat.all()
        g_parents, parents, siblings, children, g_children, cat_crumbs = [], [], [], [], [], []
        for c in cats:
            if (c.level - lvl) == 2:
                g_children.append(c)
            elif (c.level - lvl) == 1:
                children.append(c)
            elif c.level == lvl:
                siblings.append(c)
            elif (lvl - c.level) == 1:
                parents.append(c)
            elif (lvl - c.level) == 2:
                g_parents.append(c)
        cat_crumbs.append(self)
        if parents:
            cat_crumbs.append(parents[0])
            if g_parents:
                cat_crumbs.append(g_parents[0])
        return locals()

    def get_sub(self):
        n = self.level
        sub = self.sub_cat.filter(level=int(n)+1)
        return sub

    def get_sub_full(self):
        n = self.level
        sub = self.sub_cat.filter(level__gt=n)
        return sub

    def set_sub(self, c):
        self.sub_cat.add([c])
        return c

    def get_parent_cat(self):
        n = self.level
        sub = self.sub_cat.filter(level__lt=n)
        return sub

    def get_parent_all(self):
        n = self.level
        par = self.sub_cat.filter(level__lt=n)
        parents = Category.objects.filter(id__gte=10000)
        if par:
            for s in par:
                pare = s.get_parent_cat()
                parents = parents | pare
            parents = parents | par
        if not par:
            sub = self.sub_cat.filter(level=str(int(n)+1))[0]
            parents = sub.get_parent_cat()
        return parents

    def get_siblings(self):
        if self.level == 1:
            siblings = Category.objects.filter(level=1).exclude(pk=self.pk)
        else:
            parent = self.get_parent_cat()
            siblings = Category.objects.none()
            for p in parent:
                a = p.sub_cat.filter(level=p.level+1).exclude(pk=self.pk)
                siblings = siblings | a
        return siblings

    def get_hierarchy(self):
        parent = self.get_parent_all()
        child = self.get_sub_full()
        siblings = self.get_siblings()
        hierarchy = parent | child | siblings
        # self_cat = Category.objects.filter(id)
        # hierarchy = hierarchy | self_cat
        return hierarchy

    def related_categories(self):
        if self.level == '3':
            immediate_parent = self.sub_cat.filter(level=2)
            # super_parent = self.sub_cat.filter(level=1)
            imm_related = Category.objects.filter(id=self.id)
            for cat in immediate_parent:
                a = cat.get_sub()
                imm_related = imm_related | a
        elif self.level == '2':
            imm_related = Category.objects.filter(id=self.id).exclude(id=self.id)
            parent = self.sub_cat.filter(level=1)
            imm_related = parent
        else:
            imm_related = []
        return imm_related

    def distant_related(self):
        if self.level == '3':
            # immediate_parent = self.sub_cat.filter(level=2)
            super_parent = Category.objects.filter(id__gte=10000)
            imm_parent = self.sub_cat.filter(level=2)
            for p in imm_parent:
                a = p.get_parent_cat()
                super_parent = super_parent | a
            related = Category.objects.filter(id=self.id)
            rel = []
            for cat in super_parent:
                a = cat.get_sub()
                rel = related | a
            for r in rel:
                s = r.get_sub()
                related = related | s
        else:
            related = []
        to_exclude = self.related_categories()
        li = []
        for i in to_exclude:
            li.append(i.id)
        return related

    def get_logo(self):
        default_image = '/images/thumbnails/image.png'
        if self.image:
            image_url = '/images/'+str(self.image.image_thumbnail)
            return image_url
        else:
            return default_image

    def get_image(self):
        image = '/images/categories/'+str(self.id)+'.jpg'
        if os.path.isfile(image):
            return image
        else:
            return '/images/categories/default.png'


class Product_Categories(models.Model):
    product = models.ForeignKey(Products)
    category = models.ForeignKey(Category)
    level = models.CharField(max_length=1)

    class Meta:
        db_table = 'Product_Categories'




# Create your models here.
