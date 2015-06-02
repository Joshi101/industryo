from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
from forum.models import *
from tags.models import Tags
from forum.forms import AskForm
from activities.models import *
import json

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
            tag = form.cleaned_data.get('tags')
            question.create_tags(tag)
            slug = question.slug

            return HttpResponseRedirect('/forum/'+slug)
    else:
        return render(request, 'forum/ask.html', {'form': form})


def get_question(request, slug):
    q = Question.objects.get(slug=slug)
    comments = QuestionComment.objects.filter(question=q.id)
    answers = Answer.objects.filter(question=q.id)

    return render(request, 'forum/quest.html', locals())


def ques_comment(request):
    # slug = request.POST['slug']
    if request.method == 'POST':
        user = request.user
        comment = request.POST['comment']
        id = request.POST['id']
        slug = request.POST['slug']
        question = Question.objects.get(id=id)
        comment = QuestionComment(question=question, user=user, comment=comment)
        comment.save()
        return HttpResponseRedirect('/forum/'+slug)


def voteup(request):
    if 'qid' in request.GET:
        q = request.GET['qid']
        question = Question.objects.get(id=q)
        user = request.user
        response = {}
        r_data = {}
        r_fields = []
        try:
            vote = Activity.objects.get(user=user, question=question, activity='U')
            vote.delete()
            question.votes -= 1
            question.save()
            r_data['upvote'] = 'Upvote'
        except Exception:
            vote = Activity.objects.create(user=user, question=question, activity='U')
            vote.save()
            question.votes += 1
            question.save()
            r_data['upvote'] = 'Unupvote'
        r_data['votes']=question.votes
        r_fields = ['upvote','votes']
        response['data'] = r_data
        response['fields'] = r_fields
        print(response)
        return HttpResponse(json.dumps(response), content_type="application/json")
    elif 'aid' in request.GET:
        a = request.GET['aid']
        answer = Answer.objects.get(id=a)
        user = request.user
        try:
            vote = Activity.objects.get(user=user, answer=answer, activity='U')
            vote.delete()
            answer.votes -= 1
            r_data['upvote'] = 'Upvote'
        except Exception:
            vote = Activity.objects.create(user=user, answer=answer, activity='U')
            vote.save()
            answer.votes += 1
            r_data['upvote'] = 'Unupvote'
        r_data['votes']=answer.get_votes()
        r_fields = ['upvote','votes']
        response['data'] = r_data
        response['fields'] = r_fields
        return HttpResponse(json.dumps(response), content_type="application/json")

'''def vote():
    if 'qid' in request.GET:
        q = request.GET['qid']
        qa = Question.objects.get(id=q)
        status = True
    elif 'aid' in request.GET:
        a = request.GET['aid']
        qa = Answer.objects.get(id=a)
        status = True
    if not status:
        return ('/')
    try:
        vote = Activity.objects.get(user=user, question=question, activity='D')

    return HttpResponse(json.dumps(response), content_type="application/json")
'''
def votedown(request):
    if 'qid' in request.GET:
        q = request.GET['qid']
        question = Question.objects.get(id=q)
        # a = request.GET['aid']
        # answer = Answer.objects.get(id=a)
        user = request.user
        try:
            vote = Activity.objects.get(user=user, question=question, activity='D')
            vote.delete()
            question.votes -= 1
            r_data['downvote'] = 'Downvote'
        except Exception:
            vote = Activity.objects.create(user=user, question=question, activity='D')
            vote.save()
            question.votes += 1
            r_data['downvote'] = 'Undownpvote'
        r_data['votes']=question.get_votes()
        r_fields = ['downvote','votes']
        response['data'] = r_data
        response['fields'] = r_fields
        return HttpResponse(json.dumps(response), content_type="application/json")
    elif 'aid' in request.GET:
        a = request.GET['aid']
        answer = Answer.objects.get(id=a)
        user = request.user
        try:
            vote = Activity.objects.get(user=user, answer=answer, activity='D')
            # User.
            vote.delete()
            answer.votes += 1
            r_data['downvote'] = 'Downvote'
        except Exception:
            vote = Activity.objects.create(user=user, answer=answer, activity='D')
            vote.save()
            answer.votes -= 1
            r_data['downvote'] = 'Undownvote'
        r_data['votes']=answer.get_votes()
        r_fields = ['downvote','votes']
        response['data'] = r_data
        response['fields'] = r_fields
        return HttpResponse(json.dumps(response), content_type="application/json")


def reply(request):
    if request.method == 'POST':
        answer = request.POST['answer']
        user = request.user
        id = request.POST['id']

        question = Question.objects.get(id=id)
        slug = question.slug
        answer = Answer(answer=answer, user=user, question=question)
        answer.save()
        return HttpResponseRedirect('/forum/'+slug)
    else:
        print('problem hai')


def ans_comment(request):
    if request.method == 'POST':
        comment = request.POST['comment']
        id = request.POST['id']
        answer = Answer.objects.get(id=id)
        user = request.user
        slug = request.POST['slug']
        comment = AnswerComment(answer=answer, comment=comment, user=user)
        comment.save()
        return HttpResponseRedirect('/forum/'+slug)
    else:
        print('problem hai')


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
    if 'tag' in request.GET:
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
    else:
        return render(request, 'forum/questions.html')









