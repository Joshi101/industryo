from django.contrib import admin
from tags.models import Tags


class TagAdmin(admin.ModelAdmin):
    list_display = ['tag', 'type', ]

admin.site.register(Tags, TagAdmin)

# Register your models here.
