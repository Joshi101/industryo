from django.contrib import admin
from forum.models import Question


class QuestionAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'answers', ]

admin.site.register(Question, QuestionAdmin)


# Register your models here.
