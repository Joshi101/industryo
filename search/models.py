from django.db import models


class SavedSearch(models.Model):
    text = models.CharField(max_length=20)
    url = models.CharField(max_length=20)
    hits = models.IntegerField(default=0)

    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        db_table = 'SavedSearch'

    def __str__(self):
        return self.text
