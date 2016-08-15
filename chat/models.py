from django.db import models
from django.contrib.auth.models import User

from django.db.models import Max


class Conversation(models.Model):
    user1 = models.ForeignKey(User, related_name='+')
    user2 = models.ForeignKey(User, related_name='+')
    last_message_from = models.ForeignKey(User, null=True, blank=True)      # 1=frm_use 2=to_user
    last_active = models.DateTimeField(auto_now=True, null=True)
    date = models.DateTimeField(auto_now=True, null=True)
    seen = models.BooleanField(default=False)

    class Meta:
        db_table = 'Conversation'

    # def __str__(self):
    #     return self.mes

    def get_other_user(self, user):
        if self.user1 == user:
            return self.user2
        else:
            return self.user1

    def get_last_message(self):
        m = Message.objects.filter(conversation=self.id).last()
        return m

    def get_read(self):
        m = Message.objects.filter(conversation=self.id).last()
        read = m.is_read
        return read

    def get_msg_count(self):
        c = Message.objects.filter(conversation=self.id).count()
        return c


class Message(models.Model):
    conversation = models.ForeignKey(Conversation)
    from_user = models.ForeignKey(User, related_name='+', null=True)
    to_user = models.ForeignKey(User, related_name='+', null=True)
    message = models.CharField(max_length=1000)
    seen = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Message'

    def __str__(self):
        return self.message









# Create your models here.
