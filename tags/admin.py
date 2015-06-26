from django.contrib import admin
from tags.models import Tags


class TagAdmin(admin.ModelAdmin):
    list_display = ['tag', 'type', 'description', ]

admin.site.register(Tags, TagAdmin)

# Register your models here.
