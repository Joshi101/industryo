from django.contrib import admin
from nodes.models import Node


class NodeAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'post', ]

admin.site.register(Node, NodeAdmin)


# class ImageAdmin(admin.ModelAdmin):
#     list

# Register your models here.
