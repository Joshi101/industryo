from django.db import models
from industryo.unique_slug import unique_slugify
from nodes.models import Images
from tags.models import Tags
from django.contrib.auth.models import User
from threading import Thread
from django.db.models import Q


class Workplace(models.Model):
    name = models.CharField(max_length=255)
    Workplace_Type = (
        ('A', 'Large Scale Industry'),
        ('B', 'Small & Medium Scale Enterprise'),
        ('C', 'SAE Collegiate club'),
        ('O', 'Educational Institution')
    )
    workplace_type = models.CharField(max_length=1, choices=Workplace_Type)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    verified = models.BooleanField(default=False)
    slug = models.SlugField(max_length=255)
    about = models.TextField(null=True, blank=True)
    points = models.IntegerField(default=0)
    logo = models.ForeignKey('nodes.Images', null=True, blank=True)
    segments = models.ManyToManyField(Tags, related_name='segments', blank=True)
    institution = models.ForeignKey(Tags, related_name='institution', null=True, blank=True)            # don't know why
    capabilities = models.TextField(max_length=5000, null=True, blank=True)
    product_details = models.TextField(max_length=5000, null=True, blank=True)
    wptags = models.ManyToManyField(Tags, through='WpTags', related_name='wptags')
    ##
    website = models.URLField(null=True, blank=True)
    fb_page = models.URLField(null=True, blank=True)
    linkedin_page = models.URLField(null=True, blank=True)
    office_mail_id = models.EmailField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    contact = models.CharField(max_length=255, null=True, blank=True)
    mobile_contact1 = models.CharField(max_length=20, null=True, blank=True)
    mobile_contact2 = models.CharField(max_length=20, null=True, blank=True)
    contact_person = models.ForeignKey(User, null=True, blank=True)

    history = models.TextField(null=True, blank=True)
    number_of_employees = models.CharField(max_length=10, null=True, blank=True)
    year_established = models.CharField(max_length=10, null=True, blank=True)
    turnover = models.CharField(max_length=10, null=True, blank=True)
    revenue = models.CharField(max_length=10, null=True, blank=True)

    Manufacturing_SME = 'A'
    Service_Provider = 'B'
    Supplier = 'C'
    Other = 'O'
    SME_Type = (
        (Manufacturing_SME, 'Manufacturing SME'),
        (Service_Provider, 'Service Provider/ Consultancy'),
        (Supplier, 'Supplier/ Seller'),
        (Other, 'Others')
    )
    sme_type = models.CharField(null=True, blank=True, max_length=1, choices=SME_Type)

    Private_limited = 'A'
    Sole_proprietorship = 'B'
    Llp = 'C'
    Public = 'D'
    Partnership = 'E'
    Unregistered = 'U'
    Other = 'O'
    Legal_statuses = (
        (Private_limited, 'Private Limited'),
        (Sole_proprietorship, 'Sole Proprietorship'),
        (Llp, 'Limited Liability Partnership'),
        (Public, 'Public'),
        (Partnership, 'Partnership Firm'),
        (Unregistered, 'Unregistered'),
        (Other, 'Other')
    )
    legal_status = models.CharField(max_length=1, blank=True, null=True, choices=Legal_statuses)

    connections = models.ManyToManyField('self', through='Connections', symmetrical=False)

    hits = models.IntegerField(default=0, null=True, blank=True)

    dummy_user = models.CharField(max_length=50, null=True, blank=True)
    email = models.CharField(max_length=100, null=True, blank=True)
    dummy = models.BooleanField(default=False)

    class Meta:
        db_table = 'Workplace'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:                  # Newly created object, so set slug
            slug_str = self.name
            unique_slugify(self, slug_str)
        super(Workplace, self).save(*args, **kwargs)

    def set_institution(self, institution):
        if institution:
            workplace_tags = institution.split(',')
            li = []
            for m in workplace_tags:
                try:
                    t = Tags.objects.get(tag__iexact=m)
                except Exception:
                    if len(m) > 2:
                        t = Tags.objects.create(tag=m, type='P')
                li.append(t)
                t.count += 1
                t.save()
            for t in li:
                try:
                    e = WpTags.objects.get(workplace=self, tags=t, category='P')
                except Exception:
                    e = WpTags.objects.create(workplace=self, tags=t, category='P')
            return li

    def set_tags(self, **kwargs):       # tags, typ, primary
        tags = kwargs['tags']
        typ = kwargs['typ']
        if kwargs['primary']:
            primary = kwargs['primary']
        else:
            primary = True
        if tags:
            workplace_tags = tags.split(',')
            li = []
            for m in workplace_tags:
                try:
                    t = Tags.objects.get(tag__iexact=m)
                except Exception:
                    if len(m) > 2:
                        t = Tags.objects.create(tag=m, type=typ)
                li.append(t)
                t.count += 1
                t.save()
            for t in li:
                try:
                    e = WpTags.objects.get(workplace=self, tags=t, category=typ)
                except Exception:
                    e = WpTags.objects.create(workplace=self, tags=t, category=typ, primary=primary)
            # t = Thread(target=leads_mail, args=(l.id, 'created'))
            return li

    def set_events(self, events):
        if events:
            workplace_tags = events.split(',')
            li = []
            for m in workplace_tags:
                try:
                    t = Tags.objects.get(tag__iexact=m)
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

    def set_event(self, tag):
        try:
            e = WpTags.objects.get(workplace=self, tags=tag, category='E')
            e.count += 1
            e.save()
        except Exception:
            e = WpTags.objects.create(workplace=self, tags=tag, category='E')
            e.count += 1
            e.save()

    def set_logo(self, image, user):
        i = Images()
        a = i.upload_image(image=image, user=user)
        self.logo = a

    def get_legal_status(self):
        status = ''
        values = {
            'A': 'Private Limited',
            'B': 'Sole Proprietorship',
            'C': 'Limited Liability Partnership',
            'D': 'Public',
            'E': 'Partnership Firm',
            'O': 'Other',
            'U': 'Unregistered',
        }
        for value in values.keys():
            if value == self.legal_status:
                status = values[value]
        return status

    def get_sme_type(self):
        status = 'Others'
        values = {
            'A': 'Manufacturing SME',
            'B': 'Supplier',
            'C': 'Service Provider',
            'O': 'Others',
        }
        for value in values.keys():
            if value == self.sme_type:
                status = values[value]
        return status

    def get_type(self):
        if self.workplace_type == 'A':
            return "Large Scale Industry"
        elif self.workplace_type == 'B':
            return "Small / Medium Scale Enterprise"
        elif self.workplace_type == 'C':
            return "SAE Collegiate Club"
        elif self.workplace_type == 'O':
            return "Educational Institution"

    def get_type_short(self):
        if self.workplace_type == 'A':
            return "Company"
        elif self.workplace_type == 'B':
            return "SME"
        elif self.workplace_type == 'C':
            return "Team"
        elif self.workplace_type == 'O':
            return "Institution"

    def get_logo(self):
        default_image = '/images/wp.png'
        if self.logo:
            image_url = '/images/'+str(self.logo.image_thumbnail)
            return image_url
        else:
            return default_image

    def get_website(self):
        w = self.website
        if w and w != 'None':
            if "http" in w[0:4]:
                return w
            else:
                w = 'http://'+w
        else:
            w = ''
        return w

    def get_fb_page(self):
        w = self.fb_page
        if w and w != 'None':
            if "http" in w[0:4]:
                return w
            elif  "www.facebook.com" in w[0:16]:
                w = 'http://'+w
            elif "facebook.com" in w[0:12]:
                w = 'http://www.'+w
            else:
                w = "http://www.facebook.com/"+w
        else:
            w = ''
        return w

    def get_linkedin_page(self):
        w = self.linkedin_page
        if w and w != 'None':
            if "http" in w[0:4]:
                return w
            elif  "www.linkedin." in w[0:14]:
                w = 'http://'+w
            elif "linkedin.com" in w[0:12]:
                w = 'http://www.'+w
            else:
                w = "http://www.linkedin.com/"+w
        else:
            w = ''
        return w

    def get_city(self):
        city = self.wptags.filter(type='C')
        return city

    def get_tags(self):
        tags = WpTags.objects.filter(workplace=self).select_related('tags')
        operations, assets, city, materials, segments, events, institution = [], [], [], [], [], [], []
        for t in tags:
            if t.category == 'O':
                operations.append(t.tags)
            elif t.category == 'A':
                assets.append(t.tags)
            elif t.category == 'C':
                city.append(t.tags)
            elif t.category == 'M':
                materials.append(t.tags)
            elif t.category == 'S':
                segments.append(t.tags)
            elif t.category == 'E':
                events.append(t.tags)
            elif t.category == 'P':
                institution.append(t.tags)
        return locals()

    def get_all_tags(self):
        o = WpTags.objects.filter(workplace=self)
        li =''
        for i in o:
            li = li+i.tags.tag+','
        return li

    def get_members(self):
        ups = self.userprofile_set.all()
        return ups

    def get_enq(self):
        a = self.enquiry_set.filter(seen=False)
        b = self.enquiry_set.all()
        return {'new': a, 'total': b}

    def get_tags_count(self):
        a = self.wptags.all()
        count = len(a)
        return count

    def get_enq_count(self):
        a = self.enquiry_set.filter(seen=False).count()
        b = self.enquiry_set.all().count()
        return {'new': a, 'total': b}

    def get_product_count(self):
        count = self.products_set.all().count()
        return count

    def get_count(self):
        ups = self.userprofile_set.all()
        count = ups.count()
        return count

    def get_member_score(self):
        member_count = self.get_count()
        if member_count < 2:
            n = 20
        elif member_count in range(2, 5):
            n = 40
        elif member_count in range(5, 10):
            n = 60
        elif member_count in range(10, 20):
            n = 80
        else:
            n = 100
        return n

    def get_info_score(self):
        li = [self.contact, self.mobile_contact1, self.mobile_contact2, self.website, self.fb_page, self.legal_status,
              self.linkedin_page, self.address, self.office_mail_id, self.about, self.product_details, self.sme_type,
              self.year_established, self.turnover, self.revenue]
        a = list(filter(lambda x: x!='None', li))
        b = list(filter(lambda x: x!=None, a))
        m = len(b)
        n = int(round(m*10/1.8))
        if n:
            return n
        else:
            return 5

    def get_tags_score(self):
        m = self.wptags.all().count()
        # m=len(a)
        if m < 2:
            n = 0
        elif m in range(2, 4):
            n = 20
        elif m in range(5, 10):
            n = 40
        elif m in range(11, 15):
            n = 60
        elif m in range(16, 20):
            n = 80
        else:
            n = 100
        return n

    def get_asset_score(self):
        a = self.wptags.filter(type='A')
        m=len(a)
        if m < 2:
            n = 20
        elif m in range(2, 4):
            n = 40
        elif m in range(5, 8):
            n = 60
        elif m in range(9, 14):
            n = 80
        else:
            n = 100
        return n

    def get_product_score(self):
        m = self.products_set.all().count()
        if m < 1:
            n = 0
        elif m in range(1, 4):
            n = 20
        elif m in range(5, 8):
            n = 40
        elif m in range(9, 19):
            n = 60
        elif m in range(20, 35):
            n = 60
        else:
            n = 100
        return n

    def update_wp_score(self):
        ups = self.userprofile_set.all()
        points = 0
        for up in ups:
            points += up.points
        self.points = points
        self.save()
        return

    def get_avg_prod(self):
        z = 25
        return z

    def get_connection_list(self):
        cons = Connections.objects.filter(Q(my_company=self) | Q(other_company=self))
        li = []
        for c in cons:
            li.append(c.get_other_company().id)
        return li


class WpTags(models.Model):
    workplace = models.ForeignKey(Workplace, related_name='w_tags')
    tags = models.ForeignKey(Tags, related_name='wp_relations')
    tag_types = (('S', 'Segment'), ('C', 'City'), ('E', 'Event'), ('I', 'IndustrialArea'), ('D', 'ProductCategory'),
                 ('A', 'Asset'), ('O', 'Operation'), ('M', 'Material'), ('P', 'ParentInstitution'),
                 ('N', 'None'), ('T', 'Topic/Subject'))
    category = models.CharField(max_length=1, choices=tag_types, null=True)

    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    primary = models.BooleanField(default=True)

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


class Connections(models.Model):
    my_company = models.ForeignKey(Workplace, related_name='+')
    other_company = models.ForeignKey(Workplace, related_name='+')
    status = models.BooleanField(default=True)
    connection_types = (('S', 'Sell'), ('P', 'Purchase'), ('K', 'Know'), ('F', 'Follow'))
    type = models.CharField(max_length=1, choices=connection_types, null=True, default='T')
    approved = models.BooleanField(default=False)

    class Meta:
        db_table = 'Connections'

    def get_other_company(self, company):
        if self.my_company == company:
            return self.other_company
        else:
            return self.my_company


# Create your models here.
