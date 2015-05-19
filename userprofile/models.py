from django.db import models
from django.contrib.auth.models import User
from workplace.models import Workplace
from imagekit.models import ProcessedImageField, ImageSpecField
from imagekit.processors import ResizeToFill
from django.db.models.signals import post_save


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    # workplace = models.ManyToManyField(Workplace, through='UserWorkplace')
    primary_workplace = models.ForeignKey(Workplace, null=True)
    GenderChoices = (('M', 'Male'), ('F', 'Female'),)
    gender = models.CharField(max_length=1, choices=GenderChoices, null=True)
    job_position = models.CharField(max_length=255, null=True)
    experience = models.TextField(blank=True, null=True)
    points = models.IntegerField(default=0)

    follows = models.ManyToManyField('self', through='Relationship', related_name='related_to', symmetrical=False)
    image = ProcessedImageField(upload_to='user/main',
                                          processors=[ResizeToFill(1000, 1000)],
                                          format='JPEG',
                                          options={'quality': 60})
    image_thumbnail = ProcessedImageField(upload_to='user/thumbnails',
                                          processors=[ResizeToFill(100, 100)],
                                          format='JPEG',
                                          options={'quality': 60})

    def __str__(self):
        return self.user.get_full_name()

    def get_name(self):
        return self.user.first_name

    def get_image(self):
        default_image = 'user/main/user.jpg'
        if self.image:
            return self.image
        else:
            return default_image

    def get_image_thumbnail(self):
        default = 'user/thumbnails/user.jpg'
        if self.image_thumbnail:
            return self.image_thumbnail
        else:
            return default


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        up = UserProfile.objects.create(user=instance)
        up.save()

#
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()
#     print("profile saved")

post_save.connect(create_user_profile, sender=User)
# post_save.connect(save_user_profile, sender=User)


class ActiveRelationshipManager(models.Manager):
    def get_queryset(self):
        return super(ActiveRelationshipManager, self).get_queryset().filter(status='F')

RELATIONSHIP_FOLLOWING = 'F'
RELATIONSHIP_BLOCKED = 'B'


class Relationship(models.Model):

    RELATIONSHIP_STATUSES = ((RELATIONSHIP_FOLLOWING, 'Following'), (RELATIONSHIP_BLOCKED, 'Blocked'), )
    from_user = models.ForeignKey(UserProfile, related_name='from_person')
    to_user = models.ForeignKey(UserProfile, related_name='to_person')
    status = models.CharField(max_length=1, choices=RELATIONSHIP_STATUSES)
    created = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
    active = ActiveRelationshipManager()

    class Meta:
        ordering = ('created',)
        verbose_name = ('relationship',)
        verbose_name_plural = ('relationships',)

    def __str__(self):
        return 'relationship from %s to %s' % (self.from_user.get_name, self.to_user.get_name)


class UserWorkplace(models.Model):
    user = models.ForeignKey(UserProfile)
    workplace = models.ForeignKey(Workplace)
    authenticated = models.BooleanField(default=False)
    date_joined = models.TimeField(auto_now_add=True)




# Create your models here.
