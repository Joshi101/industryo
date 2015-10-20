from django.contrib import admin
from forum.models import Answer, Question


class QuestionAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'answers', ]

admin.site.register(Question, QuestionAdmin)


class AnswerAdmin(admin.ModelAdmin):
    list_display = ['user', 'answer', 'question', ]

admin.site.register(Answer, AnswerAdmin)

# Register your models here.
