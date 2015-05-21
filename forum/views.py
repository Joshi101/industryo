from django.shortcuts import render
from forum.models import *
from tags.models import Tags
from forum.forms import AskForm


def ask(request):

    form = AskForm(request.POST)
    if request.method == 'POST':
        if not form.is_valid():
            print("form invalid")
            return render(request, 'forum/ask.html', {'form': form})
        else:
            question = form.cleaned_data.get('question')
            title = form.cleaned_data.get('title')
            user = request.user
            question = Question(question=question, title=title, user=user)
            question.save()
            tags = form.cleaned_data.get('tags')
            question.create_tags(tags)

            return render(request, question)
    else:
        return render(request, 'forum/ask.html', {'form': form})


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


def question_tagged(request):
    questions = None

    tag = request.GET['tag']
    tags = tag.strip()
    tag_list = tags.split(' ')
    for ta in tag_list:

        t = Tags.objects.get(tag=ta)
        q = Question.objects.filter(tags=t.id)
        if questions is None:
            questions = q
        else:
            questions = questions | q

    return render(request, 'forum/questions.html', locals())