from django.db import models
from django.contrib.auth.models import User
from workplace.models import Workplace
from django.db.models.signals import post_save
from allauth.socialaccount.models import SocialAccount
import hashlib
# from nodes.models import Images
from tags.models import Tags
from activities.models import Notification


class UserProfile(models.Model):
    user = models.OneToOneField(User)

    primary_workplace = models.ForeignKey(Workplace, null=True)

    GenderChoices = (('M', 'Male'), ('F', 'Female'),)
    gender = models.CharField(max_length=1, choices=GenderChoices, null=True)
    job_position = models.CharField(max_length=255, null=True)
    experience = models.TextField(max_length=5000, blank=True, null=True)
    points = models.IntegerField(default=100)

    profile_image = models.ForeignKey('nodes.Images', null=True, blank=True)

    interests = models.ManyToManyField(Tags)
    # area = models.ForeignKey('Area', null=True, blank=True)       # maybe m2m
    approved = models.BooleanField(default=True)

    class Meta:
        db_table = 'userprofile'

    def __str__(self):
        # if self.user.first_name:
        return self.user.get_full_name()
        # else:
        #     return self.user.username

    def get_details(self):
        detail = "%s | %s" % (self.user, self.primary_workplace)
        return detail

    def get_profile_image(self):
        default_image = '/images/thumbnails/user.JPG'
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

    def set_interests(self, interests):
        interests_tags = interests.split(',')
        for m in interests_tags:
            t, created = Tags.objects.get_or_create(tag=m)
            t.count += 1
            t.save()
            self.interests.add(t)

    def get_interests(self):
        # page_user = User.objects.get(id=id)

        interests = self.interests.all()
        return interests

    def set_skills(self, skills):
        skills_tags = skills.split(', ')
        for m in skills_tags:

            t, created = Tags.objects.get_or_create(tag=m, type='O')
            t.count +=1
            t.save()
            self.interests.add(t)

    def set_area(self, area):
        t, created = Tags.objects.get_or_create(tag=area, type="C")
        self.interests = t
        t.count +=1
        t.save()

    def notify_liked(self, node):           # working
        if self.user != node.user:
            notified_user = node.user.userprofile
            notified_user.points += 5
            notified_user.save()
            Notification(notification_type=Notification.LIKED,
                         from_user=self.user,
                         to_user=node.user,
                         node=node).save()

    def unotify_liked(self, node):           # working
        if self.user != node.user:
            notified_user = node.user.userprofile
            notified_user.points -= 5
            notified_user.save()
            Notification.objects.filter(notification_type=Notification.LIKED,
                                        from_user=self.user,
                                        to_user=node.user,
                                        node=node).delete()

    def notify_q_commented(self, question):           # working
        if self.user != question.user:
            Notification(notification_type=Notification.COMMENTED,
                         from_user=self.user,
                         to_user=question.user,
                         question=question).save()

    def notify_a_commented(self, answer):           # working
        if self.user != answer.user:
            Notification(notification_type=Notification.COMMENTED,
                         from_user=self.user,
                         to_user=answer.user,
                         answer=answer).save()

    def notify_n_commented(self, node):           # working
        if self.user != node.user:
            Notification(notification_type=Notification.COMMENTED,
                         from_user=self.user,
                         to_user=node.user,
                         answer=node).save()

    def notify_also_commented(self, node):
        comments = node.get_comments()
        users = []
        for comment in comments:
            if comment.user != self.user and comment.user != node.user:
                users.append(comment.user.pk)
        users = list(set(users))
        for user in users:
            Notification(notification_type=Notification.ALSO_COMMENTED,
                         from_user=self.user,
                         to_user=User(id=user),
                         node=node).save()

    def notify_q_upvoted(self, question):           # working
        if self.user != question.user:
            notified_user = question.user.userprofile
            notified_user.points += 5
            notified_user.save()
            Notification(notification_type=Notification.VotedUp,
                         from_user=self.user,
                         to_user=question.user,
                         question=question).save()
            print("noti created")

    def notify_q_downvoted(self, question):           # working
        if self.user != question.user:
            notified_user = question.user.userprofile
            notified_user.points -= 5
            notified_user.save()
            Notification(notification_type=Notification.VotedDown,
                         from_user=self.user,
                         to_user=question.user,
                         question=question).save()

    def notify_a_upvoted(self, answer):           # working
        if self.user != answer.user:
            notified_user = answer.user.userprofile
            notified_user.points += 5
            notified_user.save()
            Notification(notification_type=Notification.VotedUp,
                         from_user=self.user,
                         to_user=answer.user,
                         answer=answer).save()

    def notify_a_downvoted(self, answer):           # working
        if self.user != answer.user:
            notified_user = answer.user.userprofile
            notified_user.points -= 5
            notified_user.save()
            Notification(notification_type=Notification.VotedDown,
                         from_user=self.user,
                         to_user=answer.user,
                         answer=answer).save()

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

    def notify_joined(self, workplace, node):
        users = User.objects.filter(primary_workplace=workplace)

        for user in users:
            Notification(notification_type=Notification.ALSO_JOINED,
                         from_user=self.user,
                         to_user=user,
                         node=node).save()

    def notify_answered(self, question):           # working
        if self.user != question.user:
            Notification(notification_type=Notification.ANSWERED,
                         from_user=self.user,
                         to_user=question.user,
                         question=question).save()

    # def notify_edited(self, workplace, node):
    #     users = User.objects.filter(enterprise=enterprise)
    #
    #     for user in users:
    #         Notification(notification_type=Notification.EDITED,
    #                      from_user=self.user,
    #                      to_user=user,
    #                      node=node).save()

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

#
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()
#     print("profile saved")

post_save.connect(create_user_profile, sender=User)
# post_save.connect(save_user_profile, sender=User)







# Create your models here.
