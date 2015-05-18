from django.db import models
from workplace.models import Workplace
from nodes.models import Images


class WorkplaceProfile(models.Model):
    workplace = models.ForeignKey(Workplace)
    area = models.CharField(max_length=50)
    address = models.CharField(max_length=255)
    contact = models.CharField(max_length=255)
    about = models.TextField(null=True, blank=True)
    points = models.IntegerField(default=0)
    logo = models.ForeignKey(Images, null=True)

    def __str__(self):
        return self.workplace.name



# Create your models here.
