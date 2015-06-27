from django.contrib import admin
from workplace.models import Workplace


class WorkplaceAdmin(admin.ModelAdmin):
    list_display = ['name', 'workplace_type', 'verified', ]

admin.site.register(Workplace, WorkplaceAdmin)

# Register your models here.
