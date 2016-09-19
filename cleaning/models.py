from django.db import models


class HTML(models.Model):
    name = models.CharField(max_length=255)
    path = models.CharField(max_length=255)
    complete_path = models.CharField(max_length=255)
    extends = models.ManyToManyField('self', blank=True)
    includes = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:                  # Newly created object, so set slug
            slug_str = "%s/%s" % (self.path, self.name)
            self.complete_path = slug_str
        super(HTML, self).save(*args, **kwargs)


class PY(models.Model):
    name = models.CharField(max_length=255)
    path = models.CharField(max_length=255)
    complete_path = models.CharField(max_length=255)
    includes_temp = models.ManyToManyField(HTML, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.id:                  # Newly created object, so set slug
            slug_str = "%s/%s" % (self.path, self.name)
            self.complete_path = slug_str
        super(PY, self).save(*args, **kwargs)
