from django.contrib import admin
from chat.models import Message


class ChatAdmin(admin.ModelAdmin):
    list_display = ['message', 'user', 'from_user']

admin.site.register(Message, ChatAdmin)
# Register your models here.
