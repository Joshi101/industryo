from django.db import models
from django.contrib.auth.models import User
from tags.models import Tags
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from industryo.unique_slug import unique_slugify
from activities.models import Activity


class Images(models.Model):
    image = ProcessedImageField(upload_to='main',
                                          processors=[ResizeToFill(400, 400)],
                                          format='JPEG',
                                          options={'quality': 100})
    image_thumbnail = ProcessedImageField(upload_to='thumbnails',
                                          processors=[ResizeToFill(110, 110)],
                                          format='JPEG',
                                          options={'quality': 100})
    caption = models.CharField(max_length=255)
    time = models.TimeField(auto_now_add=True)
    slug = models.SlugField(max_length=20, null=True)
    user = models.ForeignKey(User)

    def __str__(self):
        return self.caption

    def save(self, *args, **kwargs):
        if not self.id:                  # Newly created object, so set slug
            slug_str = self.id
            unique_slugify(self, slug_str)
            # self.slug = slugify(self.get_full_name()).__str__()
            super(Images, self).save(*args, **kwargs)

    def upload_image(self, image, user):
        i = Images.objects.create(image=image, image_thumbnail=image, user=user, caption='asdf')
        return i


class FeedManager(models.Manager):
    def get_queryset(self):
        return super(FeedManager, self).get_queryset().\
            filter(parent=None, category='F', is_active=True).order_by('-score', '-date')


class ArticleManager(models.Manager):
    def get_queryset(self):
        return super(ArticleManager, self).get_queryset().\
            filter(parent=None, category='A', is_active=True).order_by('date', '-score')


class Node(models.Model):
    user = models.ForeignKey(User)
    node_type = (('F', 'Feed'), ('A', 'Article'), ('C', 'Comment'), ('D', 'Dashboard'))
    category = models.CharField(max_length=1, choices=node_type, default='F')
    title = models.TextField(max_length=255, null=True, blank=True, db_index=True)
    post = models.TextField(max_length=10000)
    slug = models.SlugField(max_length=255, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True)
    comments = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    admin_score = models.FloatField(default=1)
    score = models.FloatField(default=0)
    is_active = models.BooleanField(default=True)
    tags = models.ManyToManyField(Tags)
    image = models.ForeignKey(Images, null=True)
    published = models.BooleanField(default=True)           ## articles as draft

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
        return Node.article.all()

    def save(self, *args, **kwargs):
        if not self.id:             # Newly created object, so set slug
            if not self.parent:
                if self.category is 'A':
                    slug_str = self.title
                    unique_slugify(self, slug_str)
                elif self.category is 'F':
                    slug_str = self.post[:250]
                    unique_slugify(self, slug_str)
                elif self.category is 'D':
                    slug_str = self.post[:250]
                    unique_slugify(self, slug_str)

        super(Node, self).save(*args, **kwargs)

    def set_tags(self, tags):
        article_tags = tags.split(' ')
        li = []
        for m in article_tags:

            t, created = Tags.objects.get_or_create(tag=m)
            li.append(t)
        self.tags = li

    def get_like_count(self):
        likes = Activity.objects.filter(node=self.pk).count()
        return likes

    def get_likers(self):
        likers = []
        likes = Activity.objects.filter(node=self.pk)
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
        comments = Node.objects.filter(parent=self.pk)[:1]
        for comment in comments:
            return comment

# Create your models here.
