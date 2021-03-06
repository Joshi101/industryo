from django.db import models
from django.contrib.auth.models import User
from django.utils.html import escape
from home.notification_template import *


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


class Enquiry(models.Model):
    user = models.ForeignKey(User, null=True, blank=True)   # from
    email = models.EmailField(max_length=30, null=True, blank=True)
    name = models.CharField(max_length=30, null=True, blank=True)
    # contact = models.CharField(max_length=30, null=True, blank=True)
    company = models.CharField(max_length=30, null=True, blank=True)

    product = models.ForeignKey('products.Products', null=True, blank=True)
    workplace = models.ForeignKey('workplace.Workplace', null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=1000)
    seen = models.BooleanField(default=False)
    # conversation_fk = models.ForeignKey(Conversation, null=True, blank=True)      # New connection with message model
    response_made = models.BooleanField(default=False)
    enquirer_comment = models.CharField(max_length=200, null=True, blank=True)
    producer_comment = models.CharField(max_length=200, null=True, blank=True)

    phone_no = models.CharField(max_length=30, null=True, blank=True)

    def __str__(self):
        return self.message

    def get_producer(self):
        producer = self.product.producer
        return producer

    def get_status(self):
        if self.seen:
            return "Seen"
        else:
            return "Waiting"


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
    Inquired = 'I'
    Connected = 'N'

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
        (Inquired, 'Inquired'),
        (Connected, 'Connected'),
    )
    _LIKED_TEMPLATE = u'<a href="/user/{0}/">{1}</a> liked your post: <a href="/nodes/{2}/">{3}</a>'            # working
    _COMMENTED_N_TEMPLATE = u'<a href="/user/{0}/">{1}</a> commented on your post: <a href="/nodes/{2}/">{3}</a>'            # working
    _COMMENTED_Q_TEMPLATE = u'<a href="/user/{0}/">{1}</a> commented on your question: <a href="/forum/{2}/">{3}</a>'            # working
    _COMMENTED_A_TEMPLATE = u'<a href="/user/{0}/">{1}</a> commented on your answer: <a href="/forum/{2}/">{3}</a>'            # working
    _ALSO_COMMENTED_TEMPLATE = u'<a href="/user/{0}/">{1}</a> also commented on the post: <a href="/nodes/{2}/">{3}</a>'    # working
    _ALSO_Q_COMMENTED_TEMPLATE = u'<a href="/user/{0}/">{1}</a> also commented on the question: <a href="/forum/{2}/">{3}</a>'    # working
    _ALSO_A_COMMENTED_TEMPLATE = u'<a href="/user/{0}/">{1}</a> also commented on the answer: <a href="/forum/{2}/">{3}</a>'    # working
    _JOINED_TEMPLATE = u'<a href="/user/{0}/">{1}</a> has joined your company/ institution'  # fuck
    _ALSO_JOINED_TEMPLATE = u'<a href="/user/{0}/">{1}</a> also joined your workplace'  # fuck
    _EDITED_TEMPLATE = u'<a href="/user/{0}/">{1}</a> has made some edits to the enterprise profile'  # fuck
    _FOLLOWS_TEMPLATE = u'<a href="/user/{0}/">{1}</a> from <a href="/enterprise/{2}/">{3}</a> is following you now'  #fuck
    _VotedUpQ_TEMPLATE = u'<a href="/user/{0}/">{1}</a> votedUp your question: <a href="/forum/{2}/">{3}</a>'            # working
    _VotedDownQ_TEMPLATE = u'<a href="/user/{0}/">{1}</a> votedDown your question: <a href="/forum/{2}/">{3}</a>'            # working
    _VotedUpA_TEMPLATE = u'<a href="/user/{0}/">{1}</a> votedUp your answer: <a href="/forum/{2}/">{3}</a>'            # working
    _VotedDownA_TEMPLATE = u'<a href="/user/{0}/">{1}</a> votedDown your answer: <a href="/forum/{2}/">{3}</a>'            # working
    _ANSWERED_TEMPLATE = u'<a href="/user/{0}/">{1}</a> has replied to the question: <a href="/forum/{2}/">{3}</a>'            # working
    # _Inquired_User_Template = u'<a href="/user/{0}/">{1}</a> Made an <a href="/products/enquiry_all/">enquiry</a>'
    # _Inquired_Anon_Template = u'''{0}, made an <a href="/products/enquiry_all/">enquiry</a>'''
    _Connected_Template = u"<a href='/workplace/{0}/'>{1}</a> connected to your company"

    from_user = models.ForeignKey(User, related_name='+')
    to_user = models.ForeignKey(User, related_name='+')
    date = models.DateTimeField(auto_now_add=True)
    node = models.ForeignKey('nodes.Node', null=True, blank=True)
    question = models.ForeignKey('forum.Question', null=True, blank=True)
    answer = models.ForeignKey('forum.Answer', null=True, blank=True)
    workplace = models.ForeignKey('workplace.Workplace', null=True, blank=True)

    enquiry = models.ForeignKey(Enquiry, null=True, blank=True)

    notification_type = models.CharField(max_length=1, choices=NOTIFICATION_TYPES)
    is_read = models.BooleanField(default=False)
    mail_sent = models.BooleanField(default=False)  # after migration, change to false

    class Meta:
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        ordering = ('-date',)

    def __str__(self):
        if self.notification_type == self.LIKED:
            if self.node.category == 'A':
                return self._LIKED_TEMPLATE.format(escape(self.from_user.username), escape(self.from_user.userprofile),
                                                   self.node.slug, escape(self.node.title))
            else:
                return self._LIKED_TEMPLATE.format(
                    escape(self.from_user.username),
                    escape(self.from_user.userprofile),
                    self.node.slug,
                    escape(self.get_summary(self.node.post))
                    )
        elif self.notification_type == self.COMMENTED:
            if self.node:
                if self.node.category == 'A':
                    return self._LIKED_TEMPLATE.format(
                        escape(self.from_user.username),
                        escape(self.from_user.userprofile),
                        self.node.slug,
                        escape(self.node.title)
                        )
                else:
                    return self._LIKED_TEMPLATE.format(
                        escape(self.from_user.username),
                        escape(self.from_user.userprofile),
                        self.node.slug,
                        escape(self.get_summary(self.node.post))
                        )
            elif self.question:
                return self._COMMENTED_Q_TEMPLATE.format(
                    escape(self.from_user.username),
                    escape(self.from_user.userprofile),
                    self.question.slug,
                    escape(self.get_summary(self.question.title))
                    )
            elif self.answer:
                return self._COMMENTED_A_TEMPLATE.format(
                    escape(self.from_user.username),
                    escape(self.from_user.userprofile),
                    self.answer.question.slug,
                    escape(self.get_summary(self.answer.answer))
                    )

        elif self.notification_type == 'S':
            if self.node:
                if self.node.category == 'A':
                    return self._LIKED_TEMPLATE.format(
                        escape(self.from_user.username),
                        escape(self.from_user.userprofile),
                        self.node.slug,
                        escape(self.node.title)
                        )
                else:
                    return self._LIKED_TEMPLATE.format(
                        escape(self.from_user.username),
                        escape(self.from_user.userprofile),
                        self.node.slug,
                        escape(self.get_summary(self.node.post))
                        )
            elif self.question:
                return self._ALSO_Q_COMMENTED_TEMPLATE.format(
                    escape(self.from_user.username),
                    escape(self.from_user.userprofile),
                    self.question.slug,
                    escape(self.get_summary(self.question.title))
                    )
            elif self.answer:
                return self._ALSO_A_COMMENTED_TEMPLATE.format(
                    escape(self.from_user.username),
                    escape(self.from_user.userprofile),
                    self.answer.question.slug,
                    escape(self.get_summary(self.answer.answer))
                    )
            # return self._ALSO_COMMENTED_TEMPLATE.format(
            #     escape(self.from_user.username),
            #     escape(self.from_user.userprofile),
            #     self.node.pk,
            #     escape(self.get_summary(self.node.post))
            #     )

        elif self.notification_type == 'F':
            return self._FOLLOWS_TEMPLATE.format(
                escape(self.from_user.username),
                escape(self.from_user.userprofile),
                escape(self.from_user.enterprise.slug),
                escape(self.from_user.enterprise)
                )

        elif self.notification_type == 'J':
            return self._ALSO_JOINED_TEMPLATE.format(
                escape(self.from_user.username),
                escape(self.from_user.userprofile),
                )

        elif self.notification_type == 'E':
            return self._EDITED_TEMPLATE.format(
                escape(self.from_user.username),
                escape(self.from_user.userprofile),
                )
        if self.notification_type == 'U':
            if self.question:
                return self._VotedUpQ_TEMPLATE.format(
                    escape(self.from_user.username),
                    escape(self.from_user.userprofile),
                    self.question.slug,
                    escape(self.get_summary(self.question.title))
                    )
            else:
                return self._VotedUpA_TEMPLATE.format(
                    escape(self.from_user.username),
                    escape(self.from_user.userprofile),
                    self.answer.question.slug,
                    escape(self.get_summary(self.answer.answer))
                    )

        if self.notification_type == 'D':
            if self.question:
                return self._VotedDownQ_TEMPLATE.format(
                    escape(self.from_user.username),
                    escape(self.from_user.userprofile),
                    self.question.slug,
                    escape(self.get_summary(self.question.title))
                    )
            else:
                return self._VotedDownA_TEMPLATE.format(
                    escape(self.from_user.username),
                    escape(self.from_user.userprofile),
                    self.answer.question.slug,
                    escape(self.get_summary(self.answer.answer))
                    )
        elif self.notification_type == 'A':
            return self._ANSWERED_TEMPLATE.format(
                escape(self.from_user.username),
                escape(self.from_user.userprofile),
                self.question.slug,
                escape(self.get_summary(self.question.title))
                )
        elif self.notification_type == 'I':
            if self.enquiry.user:
                return self._Inquired_User_Template.format(
                    escape(self.from_user.username),
                    escape(self.from_user.userprofile),
                    )
            else:
                return self._Inquired_Anon_Template.format(
                    self.enquiry.name,
                    )
        elif self.notification_type == 'N':
            return self._Connected_Template.format(
                escape(self.workplace.slug),
                escape(self.workplace)
                )
        else:
            return "Oops! something went wrong."

    def get_summary(self, value):
        summary_size = 75
        if len(value) > summary_size:
            return u'{0}...'.format(value[:summary_size])
        else:
            return value

    def get_html(self):
        if self.notification_type == 'L':
            if self.node.category=='A':
                template = article_liked.format(self.to_user.userprofile, self.from_user.userprofile,
                                                self.from_user.username, self.node.title, self.node.slug)
            else:
                template = post_liked.format(self.to_user.userprofile, self.from_user.userprofile,
                                             self.from_user.username, self.node.slug)
        if self.notification_type == 'U':
            if self.question:
                template = question_upvoted.format(self.to_user.userprofile, self.from_user.userprofile,
                                                   self.from_user.username, self.question.title, self.question.slug) #done
            if self.answer:
                template = answer_upvoted.format(self.to_user.userprofile, self.from_user.userprofile,
                                                 self.from_user.username, self.answer.question.title,
                                                 self.answer.question.slug) #done
        # if self.notification_type == 'D':
        #     if self.question:
        #         template = question_downvoted.format(self.from_user, self.question.title, self.question.slug)
        #     if self.answer:
        #         template = answer_downvoted.format(self.from_user, self.answer.question.title, self.answer.question.slug)
        if self.notification_type == 'C':
            if self.node:
                if self.node.category == 'A':
                    template = article_commented.format(self.to_user.userprofile, self.from_user.userprofile,
                                                        self.from_user.username, self.node.title, self.node.slug) #done
                else:
                    template = post_commented.format(self.to_user.userprofile, self.from_user.userprofile,
                                                     self.from_user.username, self.node.slug) # done
            elif self.question:
                template = question_commented.format(self.to_user.userprofile, self.from_user.userprofile,
                                                     self.from_user.username, self.question.title, self.question.slug) #done
            elif self.answer:
                template = answer_commented.format(self.to_user.userprofile, self.from_user.userprofile,
                                                   self.from_user.username, self.answer.question.title,
                                                   self.answer.question.slug) #done
        if self.notification_type == 'S':
            pass    # also commented
        if self.notification_type == 'J':
            template = also_joined(self.to_user.userprofile, self.from_user.userprofile,
                                   self.from_user.username, self.workplace, self.workplace.slug)
        if self.notification_type == 'N':
            template = connected(self.to_user.userprofile, self.workplace, self.workplace.slug)
        return template

    def get_text(self):
        if self.notification_type == 'L':
            if self.node.category=='A':
                template = article_liked_text.format(self.to_user.userprofile, self.from_user.userprofile,
                                                     self.node.title) #done
            else:
                template = post_liked_text.format(self.to_user.userprofile, self.from_user.userprofile) #done
        if self.notification_type == 'U':
            if self.question:
                template = question_upvoted_text.format(self.to_user.userprofile, self.from_user.userprofile,
                                                        self.question.title) #done
            if self.answer:
                template = answer_upvoted_text.format(self.to_user, self.from_user, self.answer.question.title) #done
        # if self.notification_type == 'D':
        #     if self.question:
        #         template = question_downvoted_text.format(self.from_user, self.question.title, self.question.slug)
        #     if self.answer:
        #         template = answer_downvoted_text.format(self.from_user, self.answer.question.title, self.answer.question.slug)
        if self.notification_type == 'C':
            if self.node:
                if self.node.category == 'A':
                    template = article_commented_text.format(self.to_user. userprofile, self.from_user.userprofile,
                                                             self.node.title) #done
                else:
                    template = post_commented_text.format(self.to_user.userprofile, self.from_user.userprofile) #done
            elif self.question:
                template = question_commented_text.format(self.to_user.userprofile, self.from_user.userprofile,
                                                          self.question.title) #done
            elif self.answer:
                template = answer_commented_text.format(self.to_user.userprofile, self.from_user.userprofile,
                                                        self.answer.question.title) #done
        if self.notification_type == 'S':
            pass    # also commented
        if self.notification_type == 'J':
            template = also_joined_text.format(self.to_user.userprofile, self.from_user.userprofile, self.workplace)
        if self.notification_type == 'N':
            template = connected_text.format(self.to_user.userprofile, self.workplace)

        return template

    def get_subject(self):
        if self.notification_type == 'L':
            if self.node.category=='A':
                subject = '[CoreLogs] {0} likes your Article'.format(self.from_user.userprofile)
            else:
                subject = '[CoreLogs] {0} likes your update'.format(self.from_user.userprofile)
        if self.notification_type == 'U':
            if self.question:
                subject = '[CoreLogs] {0} upvoted your Question'.format(self.from_user.userprofile)
            if self.answer:
                subject = '[CoreLogs] {0} upvoted your Answer'.format(self.from_user.userprofile)

        if self.notification_type == 'C':
            if self.node:
                if self.node.category == 'A':
                    subject = '[CoreLogs] {0} commented on your Article'.format(self.from_user.userprofile)
                else:
                    subject = '[CoreLogs] {0} commented on your Update'.format(self.from_user.userprofile)
            elif self.question:
                subject = '[CoreLogs] {0} commented on your Question'.format(self.from_user.userprofile)
            elif self.answer:
                subject = '[CoreLogs] {0} commented on your Answer'.format(self.from_user.userprofile)
        if self.notification_type == 'S':
            pass    # also commented
        if self.notification_type == 'J':
            subject = '[CoreLogs] {0} joined your {1} as {2}'.format(self.from_user.userprofile,
                                                                     self.workplace.get_type_short(),
                                                                     self.from_user.userprofile.job_position)
        if self.notification_type == 'N':
            subject = '[CoreLogs] {0} Connected to Your Company on CoreLogs'.format(self.workplace)

        return subject

# Create your models here.
