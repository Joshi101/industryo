from django.db import models
from django.contrib.auth.models import User
from django.utils.html import escape


class Activity(models.Model):
    user = models.ForeignKey(User)
    LIKE = 'L'
    VoteUp = 'U'
    VoteDown = 'D'

    ACTIVITY_TYPES = (
        (LIKE, 'Like'),
        (VoteUp, 'VoteUp'),
        (VoteDown, 'VoteDown'),
    )
    activity = models.CharField(max_length=1, choices=ACTIVITY_TYPES)
    date = models.DateTimeField(auto_now_add=True)
    node = models.ForeignKey('nodes.Node', null=True, blank=True)
    question = models.ForeignKey('forum.Question', null=True, blank=True)
    answer = models.ForeignKey('forum.Answer', null=True, blank=True)

    class Meta:
        db_table = 'activity'
        verbose_name = 'Activity'
        verbose_name_plural = 'Activities'

    def __str__(self):
        return self.activity


class Notification(models.Model):
    LIKED = 'L'
    COMMENTED = 'C'
    ALSO_COMMENTED = 'S'
    JOINED = 'J'
    ANSWERED = 'A'
    # approved
    ALSO_JOINED = 'J'
    EDITED = 'E'
    # FOLLOWS = 'F'
    VotedUp = 'U'
    VotedDown = 'D'

    NOTIFICATION_TYPES = (
        (LIKED, 'Liked'),
        (COMMENTED, 'Commented'),
        (ALSO_COMMENTED, 'Also commented'),
        (ALSO_JOINED, 'Also joined'),
        (EDITED, 'Edited'),
        # (FOLLOWS, 'Follows'),
        (VotedUp, 'VotedUp'),
        (VotedDown, 'VotedDown'),
        (ANSWERED, 'Answered'),
        (JOINED, 'Joined'),
    )
    _LIKED_TEMPLATE = u'<a href="/user/{0}/">{1}</a> liked your post: <a href="/nodes/{2}/">{3}</a>'            # working
    _COMMENTED_N_TEMPLATE = u'<a href="/user/{0}/">{1}</a> commented on your post: <a href="/nodes/{2}/">{3}</a>'            # working
    _COMMENTED_Q_TEMPLATE = u'<a href="/user/{0}/">{1}</a> commented on your question: <a href="/forum/{2}/">{3}</a>'            # working
    _COMMENTED_A_TEMPLATE = u'<a href="/user/{0}/">{1}</a> commented on your answer: <a href="/forum/{2}/">{3}</a>'            # working
    _ALSO_COMMENTED_TEMPLATE = u'<a href="/user/{0}/">{1}</a> also commented on the post: <a href="/nodes/{2}/">{3}</a>'    # working
    _ALSO_Q_COMMENTED_TEMPLATE = u'<a href="/user/{0}/">{1}</a> also commented on the question: <a href="/forum/{2}/">{3}</a>'    # working
    _ALSO_A_COMMENTED_TEMPLATE = u'<a href="/user/{0}/">{1}</a> also commented on the answer: <a href="/forum/{2}/">{3}</a>'    # working
    _JOINED_TEMPLATE = u'<a href="/user/{0}/">{1}</a> has joined your enterprise'  # fuck
    _ALSO_JOINED_TEMPLATE = u'<a href="/user/{0}/">{1}</a> also joined your workplace'  # fuck
    _EDITED_TEMPLATE = u'<a href="/user/{0}/">{1}</a> has made some edits to the enterprise profile'  # fuck
    _FOLLOWS_TEMPLATE = u'<a href="/user/{0}/">{1}</a> from <a href="/enterprise/{2}/">{3}</a> is following you now'  #fuck
    _VotedUpQ_TEMPLATE = u'<a href="/user/{0}/">{1}</a> votedUp your question: <a href="/forum/{2}/">{3}</a>'            # working
    _VotedDownQ_TEMPLATE = u'<a href="/user/{0}/">{1}</a> votedDown your question: <a href="/forum/{2}/">{3}</a>'            # working
    _VotedUpA_TEMPLATE = u'<a href="/user/{0}/">{1}</a> votedUp your answer: <a href="/forum/{2}/">{3}</a>'            # working
    _VotedDownA_TEMPLATE = u'<a href="/user/{0}/">{1}</a> votedDown your answer: <a href="/forum/{2}/">{3}</a>'            # working
    _ANSWERED_TEMPLATE = u'<a href="/user/{0}/">{1}</a> has replied to the question: <a href="/forum/{2}/">{3}</a>'            # working

    from_user = models.ForeignKey(User, related_name='+')
    to_user = models.ForeignKey(User, related_name='+')
    date = models.DateTimeField(auto_now_add=True)
    node = models.ForeignKey('nodes.Node', null=True, blank=True)
    question = models.ForeignKey('forum.Question', null=True, blank=True)
    answer = models.ForeignKey('forum.Answer', null=True, blank=True)

    notification_type = models.CharField(max_length=1, choices=NOTIFICATION_TYPES)
    is_read = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ('-date',)

    def __str__(self):
        if self.notification_type == self.LIKED:
            return self._LIKED_TEMPLATE.format(
                escape(self.from_user.username),
                escape(self.from_user.first_name),
                self.node.slug,
                escape(self.get_summary(self.node.post))
                )
        elif self.notification_type == self.COMMENTED:
            if self.node:
                return self._COMMENTED_N_TEMPLATE.format(
                    escape(self.from_user.username),
                    escape(self.from_user.get_full_name()),
                    self.node.slug,
                    escape(self.get_summary(self.node.post))
                    )
            elif self.question:
                return self._COMMENTED_Q_TEMPLATE.format(
                    escape(self.from_user.username),
                    escape(self.from_user.get_full_name()),
                    self.question.slug,
                    escape(self.get_summary(self.question.title))
                    )
            elif self.answer:
                return self._COMMENTED_A_TEMPLATE.format(
                    escape(self.from_user.username),
                    escape(self.from_user.get_full_name()),
                    self.answer.question.slug,
                    escape(self.get_summary(self.answer.answer))
                    )

        elif self.notification_type == 'S':
            if self.node:
                return self._ALSO_COMMENTED_TEMPLATE.format(
                    escape(self.from_user.username),
                    escape(self.from_user.get_full_name()),
                    self.node.slug,
                    escape(self.get_summary(self.node.post))
                    )
            elif self.question:
                return self._ALSO_Q_COMMENTED_TEMPLATE.format(
                    escape(self.from_user.username),
                    escape(self.from_user.get_full_name()),
                    self.question.slug,
                    escape(self.get_summary(self.question.title))
                    )
            elif self.answer:
                return self._ALSO_A_COMMENTED_TEMPLATE.format(
                    escape(self.from_user.username),
                    escape(self.from_user.get_full_name()),
                    self.answer.question.slug,
                    escape(self.get_summary(self.answer.answer))
                    )
            # return self._ALSO_COMMENTED_TEMPLATE.format(
            #     escape(self.from_user.username),
            #     escape(self.from_user.get_full_name()),
            #     self.node.pk,
            #     escape(self.get_summary(self.node.post))
            #     )

        elif self.notification_type == 'F':
            return self._FOLLOWS_TEMPLATE.format(
                escape(self.from_user.username),
                escape(self.from_user.get_full_name()),
                escape(self.from_user.enterprise.slug),
                escape(self.from_user.enterprise)
                )

        elif self.notification_type == 'J':
            return self._ALSO_JOINED_TEMPLATE.format(
                escape(self.from_user.username),
                escape(self.from_user.get_full_name()),
                )

        elif self.notification_type == 'E':
            return self._EDITED_TEMPLATE.format(
                escape(self.from_user.username),
                escape(self.from_user.get_full_name()),
                )
        if self.notification_type == 'U':
            if self.question:
                return self._VotedUpQ_TEMPLATE.format(
                    escape(self.from_user.username),
                    escape(self.from_user.first_name),
                    self.question.slug,
                    escape(self.get_summary(self.question.title))
                    )
            else:
                return self._VotedUpA_TEMPLATE.format(
                    escape(self.from_user.username),
                    escape(self.from_user.first_name),
                    self.answer.question.slug,
                    escape(self.get_summary(self.answer.answer))
                    )

        if self.notification_type == 'D':
            if self.question:
                return self._VotedDownQ_TEMPLATE.format(
                    escape(self.from_user.username),
                    escape(self.from_user.first_name),
                    self.question.slug,
                    escape(self.get_summary(self.question.title))
                    )
            else:
                return self._VotedDownA_TEMPLATE.format(
                    escape(self.from_user.username),
                    escape(self.from_user.first_name),
                    self.answer.question.slug,
                    escape(self.get_summary(self.answer.answer))
                    )
        elif self.notification_type == 'A':
            return self._ANSWERED_TEMPLATE.format(
                escape(self.from_user.username),
                escape(self.from_user.get_full_name()),
                self.question.slug,
                escape(self.get_summary(self.question.title))
                )

        else:
            return "Oops! something went wrong."

    def get_summary(self, value):
        summary_size = 75
        if len(value) > summary_size:
            return u'{0}...'.format(value[:summary_size])
        else:
            return value




# Create your models here.
