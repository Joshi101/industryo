from django.db import models
from django.contrib.auth.models import User
from tags.models import Tags
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill
from industryo.unique_slug import unique_slugify
from activities.models import Activity
from django.utils.timezone import now
# from userprofile.models import UserProfile



class Images(models.Model):
    image = ProcessedImageField(upload_to='main',
                                          processors=[ResizeToFill(400, 400)],
                                          format='JPEG',
                                          options={'quality': 100})
    image_thumbnail = ProcessedImageField(upload_to='thumbnails',
                                          processors=[ResizeToFill(110, 110)],
                                          format='JPEG',
                                          options={'quality': 100})
    # caption = models.CharField(max_length=255)
    time = models.TimeField(auto_now_add=True)
    # slug = models.SlugField(max_length=20, null=True)
    user = models.ForeignKey(User)

    def __str__(self):
        return self.caption
    #
    # def save(self, *args, **kwargs):
    #     if not self.id:                  # Newly created object, so set slug
    #         slug_str = self.id
    #         unique_slugify(self, slug_str)
    #         # self.slug = slugify(self.get_full_name()).__str__()
    #         super(Images, self).save(*args, **kwargs)

    def upload_image(self, image, user):
        i = Images.objects.create(image=image, image_thumbnail=image, user=user)
        return i


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
    # parent = models.ForeignKey('self', null=True, blank=True)
    comments_count = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    admin_score = models.FloatField(default=1)
    score = models.FloatField(default=0)
    is_active = models.BooleanField(default=True)           # use this to keep unpublished articles
    tags = models.ManyToManyField(Tags)
    image = models.ForeignKey(Images, null=True)

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
        return self.id

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

    def get_score(self):
        p = self.likes+self.comments    # popularity
        t = (now()-self.date).total_seconds()/3600  # age_in_hrs
        # last_activity =
        n = self.admin_score
        score = (p/pow((t+1), 1.2))*n
        self.score = score
        return score





# Create your models here.
