from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
from forum.models import *
from tags.models import Tags
from forum.forms import AskForm
from activities.models import *
import json
from nodes.models import Comments


def ask(request):
    form = AskForm(request.POST)
    if request.method == 'POST':
        if not form.is_valid():
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
    comments = Comments.objects.filter(question=q.id)
    answers = Answer.objects.filter(question=q.id)

    return render(request, 'forum/quest.html', locals())


def ques_comment(request):
    if request.method == 'POST':
        user = request.user
        comment = request.POST['comment']
        id = request.POST['id']
        slug = request.POST['slug']
        question = Question.objects.get(id=id)
        comment = Comments(question=question, user=user, comment=comment)
        comment.save()
        return HttpResponseRedirect('/forum/'+slug)


def voteup(request):
    response = {}
    r_data = {}
    r_fields = []
    if 'qid' in request.GET:
        q = request.GET['qid']
        question = Question.objects.get(id=q)
        user = request.user
        # response = {}
        # r_data = {}
        # r_fields = []
        try:
            vote = Activity.objects.get(user=user, question=question, activity='U')
            vote.delete()
            user.userprofile.unotify_q_upvoted(question)
            question.votes -= 1
            # question.votes.save()
            r_data['upvote'] = 'Upvote'
        except Exception:
            vote = Activity.objects.create(user=user, question=question, activity='U')
            vote.save()
            user.userprofile.notify_q_upvoted(question)
            # question.votes += 1
            question.votes.save()
            r_data['upvote'] = 'Unupvote'
        r_data['votes'] = question.votes
        r_fields = ['upvote', 'votes']
        response['data'] = r_data
        response['fields'] = r_fields
        print(response)
        return HttpResponse(json.dumps(response), content_type="application/json")
    elif 'aid' in request.GET:
        a = request.GET['aid']
        answer = Answer.objects.get(id=a)
        user = request.user
        r_data = {}
        try:
            vote = Activity.objects.get(user=user, answer=answer, activity='U')
            vote.delete()
            user.userprofile.unotify_a_upvoted(answer)
            answer.votes -= 1
            r_data['upvote'] = 'Upvote'
        except Exception:
            vote = Activity.objects.create(user=user, answer=answer, activity='U')
            vote.save()
            user.userprofile.notify_a_upvoted(answer)
            answer.votes += 1
            r_data['upvote'] = 'Unupvote'
        r_data['votes']=answer.get_votes()
        r_fields = ['upvote', 'votes']
        response['data'] = r_data
        response['fields'] = r_fields
        return HttpResponse(json.dumps(response), content_type="application/json")

def vote(request):
    if 'qid' in request.GET:
        q = request.GET['qid']
        qa = Question.objects.get(id=q)
        status = True
        q = True
    elif 'aid' in request.GET:
        a = request.GET['aid']
        qa = Answer.objects.get(id=a)
        status = True
        q = False
    if not status:
        return ('/')
    d = request.GET['direction']
    print(qa,d,qa.votes)
    if d == 'D':
        value = -1
    elif d == 'U':
        value = 1
    user = request.user
    response = {}
    r_data = {}
    r_fields = []
    try:
        if q:
            vote = Activity.objects.get(user=user, question=qa, activity=d)
        else:
            vote = Activity.objects.get(user=user, answer=qa, activity=d)
        print(vote)
        vote.delete()
        if value:
            user.userprofile.unotify_q_upvoted(qa)
        else:
            user.userprofile.unotify_q_downvoted(qa)
        print(qa.votes)
        qa.votes -= value
        qa.save()
        print(qa.votes)
        q = request.GET['qid']
        qa2 = Question.objects.get(id=q)
        print(qa2.votes)
        r_data['vote'] = 'Vote'
    except Exception:
        if q:
            vote = Activity.objects.create(user=user, question=qa, activity=d)
            vote.save()
        else:
            vote = Activity.objects.create(user=user, answer=qa, activity=d)
            vote.save()
        print(vote.question)
        vote.save()
        if value:
            user.userprofile.notify_q_upvoted(qa)
        else:
            user.userprofile.notify_q_downvoted(qa)
        print(qa.votes)
        qa.votes += value
        qa.save()
        print(qa.votes)
        r_data['vote'] = 'Cancel'
    r_data['votes'] = qa.votes
    response['data'] = r_data
    r_fields = ['vote','votes']
    response['fields'] = r_fields
    print(response)
    return HttpResponse(json.dumps(response), content_type="application/json")

def votedown(request):
    response = {}
    r_data = {}
    r_fields = []
    if 'qid' in request.GET:
        q = request.GET['qid']
        question = Question.objects.get(id=q)
        # a = request.GET['aid']
        # answer = Answer.objects.get(id=a)
        user = request.user
        try:
            vote = Activity.objects.get(user=user, question=question, activity='D')
            vote.delete()
            user.userprofile.unotify_q_downvoted(question)
            question.votes -= 1
            r_data['downvote'] = 'Downvote'
        except Exception:
            vote = Activity.objects.create(user=user, question=question, activity='D')
            vote.save()
            user.userprofile.notify_q_downvoted(question)
            question.votes += 1
            r_data['downvote'] = 'Undownpvote'
        r_data['votes']=question.get_votes()
        r_fields = ['downvote', 'votes']
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
            user.userprofile.unotify_a_downvoted(answer)
            answer.votes += 1
            r_data['downvote'] = 'Downvote'
        except Exception:
            vote = Activity.objects.create(user=user, answer=answer, activity='D')
            vote.save()
            user.userprofile.notify_a_downvoted(answer)
            answer.votes -= 1
            r_data['downvote'] = 'Undownvote'
        r_data['votes']=answer.get_votes()
        r_fields = ['downvote', 'votes']
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
        c = Comments(answer=answer, comment=comment, user=user)
        c.save()
        return HttpResponseRedirect('/forum/'+slug)
    else:
        print('problem hai')


def tag(request):           # this for what
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


def questions(request):
    questions = Question.objects.all().select_related('user__userprofile__workplaceprofile').order_by('-date')
    for q in questions:
        print(q.title, q.question)
    return render(request, 'forum/questions.html', locals())



