# from django.db import models
# from workplace.models import Workplace
# from nodes.models import Images
# from django.db.models.signals import post_save
# from django.db.models import signals
# from industryo.unique_slug import unique_slugify
# from tags.models import Tags
#
#
# class Events(models.Model):
#     event = models.CharField(max_length=50)
#     description = models.CharField(max_length=1000)
#     slug = models.SlugField(max_length=50)
#
#     def __str__(self):
#         return self.event
#
#     def save(self, *args, **kwargs):
#         if not self.id:                  # Newly created object, so set slug
#             slug_str = self.event
#             unique_slugify(self, slug_str)
#             # self.slug = slugify(self.get_full_name()).__str__()
#             super(Events, self).save(*args, **kwargs)
#
#
# class Institution(models.Model):
#     name = models.CharField(max_length=255)
#     slug = models.SlugField(max_length=50, null=True, blank=True)
#
#     area = models.ForeignKey(Area)
#
#     def __str__(self):
#         return self.name
#
#
# class WorkplaceProfile(models.Model):
#     workplace = models.ForeignKey(Workplace)
#
#     address = models.CharField(max_length=255)
#     contact = models.CharField(max_length=255)
#     about = models.TextField(null=True, blank=True)
#     points = models.IntegerField(default=0)
#     logo = models.ForeignKey(Images, null=True)
#     # Team
#     institution = models.ForeignKey(Institution, null=True)
#     participation = models.ManyToManyField(Events)
#     # SME
#     capabilities = models.TextField(max_length=5000, null=True, blank=True)
#     product_details = models.TextField(max_length=5000, null=True, blank=True)
#
#     # LSI
#
#     def __str__(self):
#         return self.workplace.name
#
#     def set_area(self, area):
#         # a, created = Area.objects.get_or_create(id=area)
#         self.area = area
#
#     def set_institution(self, institution):
#         # a, created = Area.objects.get_or_create(id=area)
#         # t, created = Institution.objects.get_or_create(id=institution, area=a)
#         self.institution = institution
#
#     def create_participation(self, parti):
#
#         part = parti.split(' ')
#         li = []
#         st = []
#         for m in part:
#
#             t, created = Events.objects.get_or_create(event=m)
#             p, created = Tags.objects.get_or_create(tag=m, type="event")
#             li.append(t)
#             st.append(p)
#         self.participation = li
#
#     def set_logo(self, image, user):
#         i = Images()
#         a = i.upload_image(image=image, user=user)
#
#         self.logo = a
#
#
# def create_workplace_profile(sender, instance, created, **kwargs):
#     """Create ModelB for every new ModelA."""
#     if created:
#         WorkplaceProfile.objects.create(workplace=instance)
#
# signals.post_save.connect(create_workplace_profile, sender=Workplace, weak=False,
#                           dispatch_uid='models.create_workplace_profile')
#
#
#
#
#
#
#
#
