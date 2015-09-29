from django.contrib import admin
from userprofile.models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'primary_workplace', ]

admin.site.register(UserProfile, UserProfileAdmin)

# Register your models here.
