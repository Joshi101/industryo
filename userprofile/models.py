from django.db import models
from django.contrib.auth.models import User
from workplace.models import Workplace
from django.db.models.signals import post_save
from allauth.socialaccount.models import SocialAccount
import hashlib
from tags.models import Tags
from activities.models import Notification
from home import tasks
from datetime import datetime, timedelta


class UserProfile(models.Model):
    user = models.OneToOneField(User)

    primary_workplace = models.ForeignKey(Workplace, null=True, blank=True)
    workplaces = models.ManyToManyField(Workplace, through='Workplaces', related_name='wps', blank=True)

    date_joined = models.DateTimeField(auto_now_add=True, null=True)
    workplace_type = models.CharField(max_length=1, default='N', null=True)

    GenderChoices = (('M', 'Male'), ('F', 'Female'),)
    gender = models.CharField(max_length=1, choices=GenderChoices, null=True, blank=True)
    job_position = models.CharField(max_length=255, null=True, blank=True)
    experience = models.TextField(max_length=5000, blank=True, null=True)
    points = models.IntegerField(default=100)

    profile_image = models.ForeignKey('nodes.Images', null=True, blank=True)

    interests = models.ManyToManyField(Tags, blank=True)
    approved = models.BooleanField(default=True)

    mobile_contact = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    # Product related info
    product_email = models.EmailField(null=True, blank=True)
    product_phone = models.CharField(max_length=100, null=True, blank=True)

    # tag_list = models.CharField(max_length=244, null=True, blank=True)
    # back_tags = models.ManyToManyField(Tags, related_name='back_tags', null=True, blank=True)
    dummy = models.BooleanField(default=False)

    class Meta:
        db_table = 'userprofile'

    def __str__(self):
        if self.user.first_name:
            name = "%s %s" % (self.user.first_name, self.user.last_name)
        else:
            name = self.user.username
        return name

    def get_name(self):
        if self.user.first_name:
            name = "%s %s" % (self.user.first_name, self.user.last_name)
        else:
            name = self.user.username
        return name

    def get_all_workplaces(self):
        w = self.workplaces.all()
        return w

    # Code dependent upon django-allauth. Will change if we shift to another module

    def get_provider(self):
        provider = None
        a = SocialAccount.objects.filter(user=self.user)    # multiple socialaccounts can be connected to 1 usr
        if len(a) > 1:
            provider = a[0].provider + ' '+a[1].provider
        elif len(a) == 1:
            provider = a[0].provider
        elif len(a) == 0:
            provider = "email"
        return provider

    def get_profile_image(self):
        default_image = '/images/user_man.png'
        if self.profile_image:
            image_url = '/images/'+str(self.profile_image.image_thumbnail)
            return image_url
        else:
            try:
                fb_uid = SocialAccount.objects.filter(user_id=self.user.id, provider='facebook')
                if len(fb_uid):
                    return "http://graph.facebook.com/{}/picture?width=120&height=120".format(fb_uid[0].uid)
                return "http://www.gravatar.com/avatar/{}?s=40".format(hashlib.md5(self.user.email).hexdigest())

            except Exception:
                try:
                    google_uid = SocialAccount.objects.get(user_id=self.user.id, provider='Google')
                    if google_uid:
                        return google_uid.extra_data['picture']

                except Exception:
                    return default_image

    def set_primary_workplace(self, primary_workplace, job_position):
        self.primary_workplace = primary_workplace
        self.job_position = job_position
        self.workplace_type = primary_workplace.workplace_type
        self.save()
        primary_workplace.update_wp_score()
        return

    def set_interests(self, interests):
        if interests:
            workplace_tags = interests.split(',')
            li = []
            for m in workplace_tags:
                try:
                    t = Tags.objects.get(tag__iexact=m)
                except Exception:
                    if len(m) > 2:
                        t = Tags.objects.create(tag=m, type='T')
                li.append(t)
                t.count += 1
                t.save()
            self.interests.add(*li)
            return li

    def get_interests(self):
        interests = self.interests.all()
        return interests

    def get_city(self):
        interests = self.interests.filter(type='C')
        return interests

    def get_no_city(self):
        interests = self.interests.all().exclude(type='C')
        return interests

    def get_email0(self):
        email = self.user.email
        return email

    def get_email_prod(self):
        if self.product_email:
            email = self.product_email
        elif self.workplace_type is not 'N':
            if self.primary_workplace.office_mail_id:
                email = self.primary_workplace.office_mail_id
            else:
                email = self.user.email
        else:
            email = self.user.email
        return email

    def get_best_email(self):
        if self.product_email:
            email = self.product_email
        elif self.workplace_type is not 'N':
            if self.primary_workplace.office_mail_id:
                email = self.primary_workplace.office_mail_id
            else:
                email = self.user.email
        else:
            email = self.user.email
        return email

    def set_skills(self, skills):
        skills_tags = skills.split(', ')
        for m in skills_tags:

            t, created = Tags.objects.get_or_create(tag=m)
            t.count +=1
            t.save()
            self.interests.add(t)

    def set_area(self, area):
        t, created = Tags.objects.get_or_create(tag=area)
        self.interests = t
        t.count +=1
        t.save()

    def set_product_contacts(self, product_email, product_phone):
        self.product_email = product_email
        self.product_phone = product_phone
        self.save()
        return

    def get_workplace_points(self):
        members = UserProfile.objects.filter(primary_workplace=self.primary_workplace)
        points = 0
        for member in members:
            points += member.points
        self.primary_workplace.points = points
        self.primary_workplace.save()
        return points

    def get_emails(self):
        emails = []
        em = self.user.emails_set.all()
        for e in em:
            emails.append(e.email)
        return emails

    def add_points(self, points):
        self.points += points
        self.save()
        return self


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        up = UserProfile.objects.create(user=instance)
        up.save()
        tasks.get_contacts(up.user.id)
        tasks.execute_view('check_no_wp', up.user.id, schedule=timedelta(seconds=30))


post_save.connect(create_user_profile, sender=User)
# post_save.connect(save_user_profile, sender=User)


class Workplaces(models.Model):
    workplace = models.ForeignKey(Workplace, null=True)
    userprofile = models.ForeignKey(UserProfile, related_name='up', null=True)
    job_position = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = 'workplaces'




# Create your models here.