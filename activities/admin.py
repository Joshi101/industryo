from django.contrib import admin
from activities.models import Enquiry


class EnquiryAdmin(admin.ModelAdmin):
    list_display = ['product', 'message', 'user', 'name', 'seen']

admin.site.register(Enquiry, EnquiryAdmin)

# Register your models here.
