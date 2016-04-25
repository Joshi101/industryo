from django.db import models
from django.contrib.auth.models import User


class ContactEmails(models.Model):
    email = models.EmailField()
    first_name = models.CharField(max_length=20, null=True, blank=True)
    last_name = models.CharField(max_length=20, null=True, blank=True)
    user = models.ForeignKey(User)
    provider = models.CharField(max_length=10)      # google/facebook
    contact_id = models.CharField(max_length=255, null=True, blank=True)        # google
    sent = models.IntegerField(default=0)
    valid = models.BooleanField(default=True)

    class Meta:
        db_table = 'ContactEmail'

    def __str__(self):
        return self.email

    def get_image(self):
        token_id = ""
        a = 'https://www.google.com/m8/feeds/photos/media/{0}/{1}?access_token={2}'.format(self.user.email,
                                                                                           self.contact_id, token_id)
        return a







# Create your models here.
