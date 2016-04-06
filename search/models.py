from django.db import models
from django.contrib.auth.models import User


class SavedSearch(models.Model):
    text = models.CharField(max_length=20)
    url = models.CharField(max_length=20)
    meta_des = models.CharField(max_length=160, null=True, blank=True)
    hits = models.IntegerField(default=0)

    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        db_table = 'SavedSearch'

    def __str__(self):
        return self.text


# class SearchHistory(models.Model):
#     text = models.CharField(max_length=100)
#     type = models.CharField(max_length=1)
#     user = models.ForeignKey(User, null=True, blank=True)
#     ip = models.IPAddressField(null=True, blank=True)
#     dropdown_only = models.BooleanField(default=True)
#
#     class Meta:
#         db_table = 'Searches'
#
#     def __str__(self):
#         return self.text