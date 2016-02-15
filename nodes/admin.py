from django.contrib import admin
from nodes.models import Node, Images, Comments


class NodeAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'post', ]

admin.site.register(Node, NodeAdmin)


class ImageAdmin(admin.ModelAdmin):
    list_display = ['image', 'image_thumbnail', 'user', ]

admin.site.register(Images, ImageAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'node', 'comment', ]

admin.site.register(Comments, CommentAdmin)

# class ImageAdmin(admin.ModelAdmin):
#     list

# Register your models here.
