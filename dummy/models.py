from django.db import models
from industryo.unique_slug import unique_slugify


class Company(models.Model):
    cin = models.CharField(max_length=22)
    dor = models.DateField()
    name = models.CharField(max_length=200)
    status = models.CharField(max_length=25)
    company_class = models.CharField(max_length=25)
    authorized_c = models.CharField(max_length=15)
    paidup_c = models.CharField(max_length=15)
    activity = models.CharField(max_length=100)
    address = models.CharField(max_length=500)
    category = models.CharField(max_length=100)

    state = models.CharField(max_length=100)

    email = models.CharField(max_length=100, null=True, blank=True)
    about = models.TextField(max_length=5000, null=True, blank=True)
    website = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:             # Newly created object, so set slug

            slug_str = self.name
            unique_slugify(self, slug_str)

        super(Companies, self).save(*args, **kwargs)
        return self.id


class Director(models.Model):
    din = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    company = models.ForeignKey(Company)