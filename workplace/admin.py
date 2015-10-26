from django.contrib import admin
from workplace.models import Workplace, WpTags


class WorkplaceAdmin(admin.ModelAdmin):
    list_display = ['name', 'workplace_type', 'verified', ]

admin.site.register(Workplace, WorkplaceAdmin)


class WpTagsAdmin(admin.ModelAdmin):
    list_display = ['tags', 'workplace', 'category', ]

admin.site.register(WpTags, WpTagsAdmin)

# Register your models here.
