from django.contrib import admin
from products.models import Products


class ProductAdmin(admin.ModelAdmin):
    list_display = ['product', 'producer', 'user', ]

admin.site.register(Products, ProductAdmin)
# Register your models here.
