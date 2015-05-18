from django.shortcuts import render
from forum.models import *
from tags.models import Tags


def ask(request):

    if request.method == "POST":
        question = request.POST['question']
        title = request.POST['title']
        user = request.user
        question = Question(question=question, title=title, user=user)
        question.save()

        tags = request.POST['POST']
        for tag in tags:
            tag, created = Tags.objects.get_or_create(tag=tag)

            if created:
                tag.save()
                return tag

        question.tags = tags

        return render(request, question)


def ques_comment(request, id):
    if request.method == 'POST':
        user = request.user
        comment = request.POST['comment']
        question = Question.objects.get(id=id)
        comment = QuestionComment(question=question, user=user, comment=comment)
        comment.save()


def reply(request, id):
    if request.method == 'POST':
        answer = request.POST['answer']
        user = request.user
        question = Question.objects.get(id=id)
        answer = Answer(answer=answer, user=user, question=question)
        answer.save()


def ans_comment(request, id):
    if request.method == 'POST':
        comment = request.POST['comment']
        answer = Answer.objects.get(id=id)
        user = request.user
        comment = AnswerComment(answer=answer, comment=comment, user=user)
        comment.save()


def tag(request):
    if request.method == 'POST':
        t = request.POST['tag']
        tag, created = Tags.objects.get_or_create(tag=t)
        return tag
    else:
        t = request.GET['tag']
        tag = Tags.objects.get(tag=t)
        return tag
# Create your views here.
