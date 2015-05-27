from django.db import models
from django.contrib.auth.models import User
from workplace.models import Area
from workplaceprofile.models import Workplace
from django.db.models.signals import post_save
from allauth.socialaccount.models import SocialAccount
import hashlib
from nodes.models import Images
from tags.models import Tags


class UserProfile(models.Model):
    user = models.OneToOneField(User)

    primary_workplace = models.ForeignKey(Workplace, null=True)
    GenderChoices = (('M', 'Male'), ('F', 'Female'),)
    gender = models.CharField(max_length=1, choices=GenderChoices, null=True)
    job_position = models.CharField(max_length=255, null=True)
    experience = models.TextField(max_length=5000, blank=True, null=True)
    points = models.IntegerField(default=0)

    profile_image = models.ForeignKey(Images, null=True, blank=True)

    interests = models.ManyToManyField(Tags)
    area = models.ForeignKey(Area, null=True, blank=True)       # maybe m2m
    approved = models.BooleanField(default=True)

    class Meta:
        db_table = 'userprofile'

    def __str__(self):
        return self.user.get_full_name()

    def get_details(self):
        detail = "%s | %s" % (self.user, self.primary_workplace)
        return detail

    def profile_image_url(self):
        fb_uid = SocialAccount.objects.filter(user_id=self.user.id, provider='facebook')

        if len(fb_uid):
            return "http://graph.facebook.com/{}/picture?width=40&height=40".format(fb_uid[0].uid)

        return "http://www.gravatar.com/avatar/{}?s=40".format(hashlib.md5(self.user.email).hexdigest())

    def get_profile_image(self):
        if self.profile_image:

            return self.profile_image.image_thumbnail

    def set_interests(self, skills):
        skill_tags = skills.split(' ')
        li = []
        for m in skill_tags:

            t, created = Tags.objects.get_or_create(tag=m, type='skills')
            li.append(t)
        self.interests = li

    def get_interests(self):
        if self.interests == 'transmission':
            return self.get_details()

    def set_area(self, area):
        t, created = Area.objects.get_or_create(name=area)
        p, created = Tags.objects.get_or_create(tag=area, type="area")
        self.area = t
        self.interests = p


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







# Create your models here.
