from django.contrib import admin
from products.models import Products, Category


class ProductAdmin(admin.ModelAdmin):
    list_display = ['product', 'producer', 'user', 'target_segment']

admin.site.register(Products, ProductAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'level', 'slug']

admin.site.register(Category, CategoryAdmin)
# Register your models here.
