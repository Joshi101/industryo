from PIL import Image
from django.core.files.images import get_image_dimensions
from django.db import models
from django.contrib.auth.models import User
from tags.models import Tags
from industryo.unique_slug import unique_slugify
from activities.models import Activity
from django.utils.timezone import now
import os
from io import BytesIO
from django.core.files.base import ContentFile
from django.conf import settings


THUMB_SIZES = [
    (233, 233),
    (89, 89),
    (34, 34)
]


class Images(models.Model):
    image = models.ImageField(upload_to='main', null=True, blank=True)
    image_thumbnail = models.ImageField(upload_to='thumbnails', null=True, blank=True)
    image_thumbnail_sm = models.ImageField(upload_to='thumbnails_sm', null=True, blank=True)
    image_thumbnail_xs = models.ImageField(upload_to='thumbnails_xs', null=True, blank=True)
    time = models.TimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    temp_key = models.SmallIntegerField(null=True, blank=True)
    image_format = models.CharField(null=True, blank=True, max_length=5)

    def __str__(self):
        return str(self.pk)

    def upload_image(self, image, user):
        if len(image.name) > 30:
            image.name = image.name[:20]
        # image.open()
        i = Images.objects.create(image=image, image_thumbnail=image, image_thumbnail_sm=image, user=user)
        return i

    def upload_image1(self, image, user, name):
        if len(name) > 30:
            name = name[:20]
        i = Images.objects.create(user=user)

        new_image_io = BytesIO()
        image.save(new_image_io, format='JPEG')
        i.image.save(name, content=ContentFile(new_image_io.getvalue()))
        i.image_thumbnail.save(name, content=ContentFile(new_image_io.getvalue()))
        i.image_thumbnail_sm.save(name, content=ContentFile(new_image_io.getvalue()))
        return i

    # this function needs threading
    def upload_image_new(self, image, user, name=None, trans=None):
        file = Image.open(image)
        f_format = file.format
        print('>> The image format is : '+f_format)
        if not name:
            name = image.name
        else:
            name += '.' + f_format.lower()
        if len(name) >= 70:
            name = name[:25] + '.' + f_format.lower()
        print('>> The name is going to be : '+name)
        # crop if trans is set
        if trans:
            trans = trans.split(',')
            if len(trans) == 6:
                x = float(trans[4])
                y = float(trans[5])
                scale = float(trans[0])
                x1 = -x/scale
                y1 = -y/scale
                x2 = (-x+250)/scale
                y2 = (-y+250)/scale
                box = (int(x1), int(y1), int(x2), int(y2))
                print('-- Image croped at : ', x1, y1, x2,y2)
                file = file.crop(box)
        file.load()
        image_io = BytesIO()
        file.save(image_io, f_format)
        self.user = user
        self.image_format = f_format
        self.image.save(name, content=ContentFile(image_io.getvalue()))
        #  image is successfully saved till here, proceed to gve a feedback
        #  any further calculation better be transferred to another thread
        #  because they may get expensive
        thumb = []
        for size in THUMB_SIZES:
            f_thumb = file
            f_thumb.thumbnail(size, resample=2)
            thumb_io = BytesIO()
            if f_format == 'JPEG':
                f_thumb.save(thumb_io, f_format, optimize=True, progressive=True)
            else:
                f_thumb.save(thumb_io, f_format, optimize=True)
            thumb.append(thumb_io)
        self.image_thumbnail.save(name, content=ContentFile(thumb[0].getvalue()))
        self.image_thumbnail_sm.save(name, content=ContentFile(thumb[1].getvalue()))
        self.image_thumbnail_xs.save(name, content=ContentFile(thumb[2].getvalue()))
        self.save()
        return self

    def get_full_image(self):
        return settings.MEDIA_URL+str(self.image)

    def get_image_thumb(self):
        if self.image_thumbnail:
            return settings.MEDIA_URL+str(self.image_thumbnail)
        else:
            self.get_full_image()

    def get_image_thumb_sm(self):
        if self.image_thumbnail_sm:
            return settings.MEDIA_URL+str(self.image_thumbnail_sm)
        else:
            self.get_image_thumb()

    def get_image_thumb_xs(self):
        if self.image_thumbnail_xs:
            return settings.MEDIA_URL+str(self.image_thumbnail_xs)
        else:
            self.get_image_thumb()


class Document(models.Model):
    name = models.CharField(max_length=100)
    doc = models.FileField(upload_to='docs')
    product_doc = models.FileField(upload_to='product_doc', null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)

    def __str__(self):
        return str(self.id)

    def upload_doc(self, doc, user):
        filename = doc.name
        ext = os.path.splitext(filename)[1]
        ext = ext.lower()
        if ext in ('.doc', '.pdf', '.docx', '.xls', '.xlsx', '.csv', '.xlsm'):
            if len(doc.name) > 30:
                doc.name = doc.name[:20]
            d = Document.objects.create(doc=doc, user=user, name=doc.name)
            return d
        else:
            raise TypeError('Filetype not accepted')

    def upload_product_doc(self, doc, user):
        filename = doc.name
        ext = os.path.splitext(filename)[1]
        ext = ext.lower()
        if ext in ('.doc', '.pdf', '.docx', '.xls', '.xlsx', '.csv', '.xlsm'):
            if len(doc.name) > 30:
                doc.name = doc.name[:20]
            d = Document.objects.create(product_doc=doc, user=user, name=doc.name)
            return d
        else:
            raise TypeError('Filetype not accepted')


class FeedManager(models.Manager):
    def get_queryset(self):
        return super(FeedManager, self).get_queryset().\
            filter(category='F', is_active=True).order_by('-score', '-date')


class ArticleManager(models.Manager):
    def get_queryset(self):
        return super(ArticleManager, self).get_queryset().\
            filter(category='A', is_active=True).order_by('-date', '-score')


class Comments(models.Model):
    user = models.ForeignKey(User)
    comment = models.TextField(max_length=1000)
    node = models.ForeignKey('nodes.Node', null=True, blank=True)
    question = models.ForeignKey('forum.Question', null=True, blank=True)
    answer = models.ForeignKey('forum.Answer', null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment

    def get_last_comment(self):
        comments = Comments.objects.filter(node=self).select_related('user__userprofile__primary_workplace')[:1]
        for comment in comments:
            return comment


class Node(models.Model):
    user = models.ForeignKey(User)
    anonymous = models.BooleanField(default=False)         # anonymous
    w_type = models.CharField(max_length=1)         # workplace_type
    node_type = (('F', 'Feed'), ('A', 'Article'), ('D', 'Dashboard'))
    category = models.CharField(max_length=1, choices=node_type, default='F')
    title = models.TextField(max_length=255, null=True, blank=True)
    post = models.TextField(max_length=10000)
    slug = models.SlugField(max_length=255, null=True, blank=True)# no blank
    date = models.DateTimeField(auto_now_add=True)
    last_active = models.TimeField(auto_now=True)       # last_activity
    comments_count = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    admin_score = models.FloatField(default=1)
    score = models.FloatField(default=0)
    is_active = models.BooleanField(default=True)           # use this to keep unpublished articles
    tags = models.ManyToManyField(Tags, blank=True)
    images = models.ManyToManyField(Images, blank=True)

    hits = models.IntegerField(default=0, null=True, blank=True)

    # back_tags = models.ManyToManyField(Tags, related_name='back_tags', null=True, blank=True)

    objects = models.Manager()
    feed = FeedManager()
    article = ArticleManager()

    def __str__(self):
        if self.category is 'A':
            return self.title
        else:
            return self.post

    class Meta:
        ordering = ('-score', '-date')

    @staticmethod
    def get_feeds():
        feeds = Node.feed.all()
        return feeds

    @staticmethod
    def get_nodes():
        nodes = Node.objects.all()
        return nodes

    @staticmethod
    def get_articles():
        articles = Node.article.all()
        return articles

    def save(self, *args, **kwargs):
        if not self.id:             # Newly created object, so set slug

            if self.category is 'A':
                slug_str = self.title
                unique_slugify(self, slug_str)
            elif self.category is 'F':
                slug_str = self.post[:100]
                unique_slugify(self, slug_str)
            elif self.category is 'D':
                slug_str = self.post[:250]
                unique_slugify(self, slug_str)

        super(Node, self).save(*args, **kwargs)
        return self.id

    def set_tags(self, tags):
        if tags:
            question_tags = tags.split(',')
            li = []
            for m in question_tags:
                try:
                    t = Tags.objects.get(tag__iexact=m)
                    print(t)
                except Exception:
                    if len(m) > 2:
                        t = Tags.objects.create(tag=m, type='T')
                li.append(t)
                t.count +=1
                t.save()
            self.tags = li

    def set_tag(self, id):
        t = Tags.objects.get(id=id)
        li = []
        li.append(t)
        t.count += 1
        t.save()
        self.tags = li

    def get_like_count(self):
        likes = Activity.objects.filter(node=self.pk).count()
        self.likes = likes
        self.save()
        return likes

    def get_likers(self):
        likers = []
        likes = Activity.objects.filter(node=self.pk).select_related('user')
        for like in likes:
            likers.append(like.user)
        return likers

    def comment(self, user, post):
        feed_comment = Node(user=user, post=post, parent=self)
        feed_comment.save()
        self.comments = Node.objects.filter(parent=self).count()
        self.save()
        return feed_comment

    def get_last_comment(self):
        comments = Comments.objects.filter(node=self).select_related('user__userprofile__primary_workplace')[:1]
        for comment in comments:
            return comment

    def get_images(self):

        images = self.images.all()
        return images

    def get_score(self):
        p = self.likes+self.comments    # popularity
        t = (now()-self.date).total_seconds()/3600  # age_in_hrs
        # last_activity =
        n = self.admin_score
        score = (p/pow((t+1), 1.2))*n
        self.score = score
        return score

    def add_image(self, image, user):
        i = Images()
        a = i.upload_image(image=image, user=user)
        self.image = a

    def get_tags(self):
        tags = self.tags.all()
        return tags

    def get_all_comments(self):
        comments = Comments.objects.filter(node=self).select_related('user__userprofile__primary_workplace')
        return comments

    def get_summary(self):
        summary_size = 500
        value = self.post
        if len(value) > summary_size:
            return u'{0}...'.format(value[:summary_size])
        else:
            return value

# Create your models here.
