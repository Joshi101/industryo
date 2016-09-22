from django.db import models
from industryo.unique_slug import unique_slugify


class Company(models.Model):
    cin = models.CharField(max_length=22, null=True, blank=True)
    dor = models.CharField(max_length=15, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    status = models.CharField(max_length=100, null=True, blank=True)
    company_class = models.CharField(max_length=100, null=True, blank=True)
    company_category = models.CharField(max_length=100, null=True, blank=True)
    authorized_c = models.CharField(max_length=200, null=True, blank=True)
    paidup_c = models.CharField(max_length=200, null=True, blank=True)
    business = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=500, null=True, blank=True)
    # category = models.CharField(max_length=100, null=True, blank=True)
    registrar = models.CharField(max_length=200, null=True, blank=True)
    state = models.CharField(max_length=200, null=True, blank=True)
    sub_c = models.CharField(max_length=200, null=True, blank=True)

    # email = models.CharField(max_length=100, null=True, blank=True)
    # about = models.TextField(max_length=5000, null=True, blank=True)
    # website = models.CharField(max_length=100, null=True, blank=True)
    #
    # scraped = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:

            slug_str = self.name
            unique_slugify(self, slug_str)

        super(Company, self).save(*args, **kwargs)
        return self.id


class Director(models.Model):
    din = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    company = models.ForeignKey(Company, null=True, blank=True)

    def __str__(self):
        return self.name
