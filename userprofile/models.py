from django.db import models
from django.contrib.auth.models import User
from workplace.models import Workplace
from django.db.models.signals import post_save
from allauth.socialaccount.models import SocialAccount
import hashlib
from tags.models import Tags
from activities.models import Notification
from home import tasks
# from contacts.views import get_google_contacts_i, print_arg_fn
import json
from datetime import datetime, timedelta


class UserProfile(models.Model):
    user = models.OneToOneField(User)

    primary_workplace = models.ForeignKey(Workplace, null=True, blank=True)
    workplaces = models.ManyToManyField(Workplace, through='Workplaces', related_name='wps', null=True, blank=True)

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

    mobile_contact = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    # Product related info
    product_email = models.EmailField(null=True, blank=True)
    product_phone = models.CharField(max_length=25, null=True, blank=True)

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
            self.interests = li
            return li

    def get_interests(self):
        # page_user = User.objects.get(id=id)

        interests = self.interests.all()
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

    def notify_liked(self, node):           # working 1
        if self.user != node.user:
            notified_user = node.user.userprofile
            notified_user.points += 5
            notified_user.save()
            a = Notification.objects.create(notification_type=Notification.LIKED,
                                            from_user=self.user,
                                            to_user=node.user,
                                            node=node)
            tasks.notify_user(a.id, n=1)

    def unotify_liked(self, node):           # working
        if self.user != node.user:
            notified_user = node.user.userprofile
            notified_user.points -= 5
            notified_user.save()
            Notification.objects.filter(notification_type=Notification.LIKED,
                                        from_user=self.user,
                                        to_user=node.user,
                                        node=node).delete()

    def notify_q_commented(self, question):           # working 2
        if self.user != question.user:
            a = Notification.objects.create(notification_type=Notification.COMMENTED,
                                            from_user=self.user,
                                            to_user=question.user,
                                            question=question)
            tasks.notify_user(a.id, n=2)

    def notify_a_commented(self, answer):           # working 3
        if self.user != answer.user:
            a = Notification.objects.create(notification_type=Notification.COMMENTED,
                                            from_user=self.user,
                                            to_user=answer.user,
                                            answer=answer)
            tasks.notify_user(a.id, n=3)

    def notify_n_commented(self, node):           # working 4
        if self.user != node.user:
            a = Notification.objects.create(notification_type=Notification.COMMENTED,
                                            from_user=self.user,
                                            to_user=node.user,
                                            node=node)
            tasks.notify_user(a.id, n=4)

    def notify_also_n_commented(self, node):           # working 5
        comments = node.get_all_comments()
        users = []
        for comment in comments:
            if comment.user != self.user and comment.user != node.user:
                users.append(comment.user.pk)
        users = list(set(users))
        for user in users:
            a = Notification.objects.create(notification_type=Notification.ALSO_COMMENTED,
                                            from_user=self.user,
                                            to_user=User(id=user),
                                            node=node)
            tasks.notify_user(a.id, n=5)

    def notify_also_q_commented(self, question):           # working 6
        comments = question.get_comment_count()
        users = []
        for comment in comments:
            if comment.user != self.user and comment.user != question.user:
                users.append(comment.user.pk)
        users = list(set(users))
        for user in users:
            a = Notification.objects.create(notification_type=Notification.ALSO_COMMENTED,
                                            from_user=self.user,
                                            to_user=User(id=user),
                                            question=question)
            tasks.notify_user(a.id, n=6)

    def notify_also_a_commented(self, answer):           # working 7
        comments = answer.get_comments()
        users = []
        for comment in comments:
            if comment.user != self.user and comment.user != answer.user:
                users.append(comment.user.pk)
        users = list(set(users))
        for user in users:
            a = Notification.objects.create(notification_type=Notification.ALSO_COMMENTED,
                                            from_user=self.user,
                                            to_user=User(id=user),
                                            answer=answer)
            tasks.notify_user(a.id, n=7)

    def notify_q_upvoted(self, question):           # working 8
        if self.user != question.user:
            notified_user = question.user.userprofile
            notified_user.points += 5
            notified_user.save()
            a = Notification.objects.create(notification_type=Notification.VotedUp,
                                            from_user=self.user,
                                            to_user=question.user,
                                            question=question)
            tasks.notify_user(a.id, n=8)

    def notify_q_downvoted(self, question):           # working 9
        if self.user != question.user:
            notified_user = question.user.userprofile
            notified_user.points -= 5
            notified_user.save()
            a = Notification.objects.create(notification_type=Notification.VotedDown,
                                            from_user=self.user,
                                            to_user=question.user,
                                            question=question)
            tasks.notify_user(a.id, n=9)

    def notify_a_upvoted(self, answer):           # working 10
        if self.user != answer.user:
            notified_user = answer.user.userprofile
            notified_user.points += 5
            notified_user.save()
            a = Notification.objects.create(notification_type=Notification.VotedUp,
                                            from_user=self.user,
                                            to_user=answer.user,
                                            answer=answer)
            tasks.notify_user(a.id, n=10)

    def notify_a_downvoted(self, answer):           # working 11
        if self.user != answer.user:
            notified_user = answer.user.userprofile
            notified_user.points -= 5
            notified_user.save()
            a = Notification.objects.create(notification_type=Notification.VotedDown,
                                            from_user=self.user,
                                            to_user=answer.user,
                                            answer=answer)
            tasks.notify_user(a.id, n=11)

    def unotify_q_upvoted(self, question):           # working
        if self.user != question.user:
            notified_user = question.user.userprofile
            notified_user.points -= 5
            notified_user.save()
            n = Notification.objects.filter(notification_type=Notification.VotedUp,
                                            from_user=self.user,
                                            to_user=question.user,
                                            question=question)
            n.delete()

    def unotify_q_downvoted(self, question):
        if self.user != question.user:           # working
            notified_user = question.user.userprofile
            notified_user.points += 5
            notified_user.save()
            Notification.objects.filter(notification_type=Notification.VotedDown,
                                        from_user=self.user,
                                        to_user=question.user,
                                        question=question).delete()

    def unotify_a_upvoted(self, answer):           # working
        if self.user != answer.user:
            notified_user = answer.user.userprofile
            notified_user.points -= 5
            notified_user.save()
            Notification.objects.filter(notification_type=Notification.VotedUp,
                                        from_user=self.user,
                                        to_user=answer.user,
                                        answer=answer).delete()

    def unotify_a_downvoted(self, answer):           # working
        if self.user != answer.user:
            notified_user = answer.user.userprofile
            notified_user.points += 5
            notified_user.save()
            Notification.objects.filter(notification_type=Notification.VotedDown,
                                        from_user=self.user,
                                        to_user=answer.user,
                                        answer=answer).delete()

    def notify_also_joined(self, primary_workplace):           # working 12
        userprofiles = UserProfile.objects.filter(primary_workplace=primary_workplace)

        for userprofile in userprofiles:
            a = Notification.objects.create(notification_type=Notification.ALSO_JOINED,
                                            from_user=self.user,
                                            to_user=userprofile.user,)

            if userprofiles.count() < 3:
                tasks.notify_user(a.id, n=12)

    def notify_answered(self, question):           # working 13
        if self.user != question.user:
            a = Notification.objects.create(notification_type=Notification.ANSWERED,
                                            from_user=self.user,
                                            to_user=question.user,
                                            question=question)

            tasks.notify_user(a.id, n=13)
        answers = question.get_answers()
        answerers = []
        for answer in answers:
            if self.user != answer.user:
                answerers.append(answer.user.pk)
        answerers = list(set(answerers))
        for user in answerers:
            a = Notification.objects.create(notification_type=Notification.ANSWERED,            # working 14
                                            from_user=self.user,
                                            to_user=User(id=user),
                                            question=question)
            tasks.notify_user(a.id, n=14)

    # def notify_edited(self, workplace, node):
    #     users = User.objects.filter(enterprise=enterprise)
    #
    #     for user in users:
    #         Notification(notification_type=Notification.EDITED,
    #                      from_user=self.user,
    #                      to_user=user,
    #                      node=node).save()

    def notify_inquired(self, e, users):
        for u in users:
            Notification.objects.create(notification_type=Notification.Inquired,
                                        from_user=self.user,
                                        to_user=u.user,
                                        enquiry=e)
            # tasks.notify_user(a.id, n=14)

    def get_workplace_points(self):
        members = UserProfile.objects.filter(primary_workplace=self.primary_workplace)
        points = 0
        for member in members:
            points += member.points
        self.primary_workplace.points = points
        self.primary_workplace.save()
        return points


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