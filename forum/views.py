from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
from forum.models import *
from tags.models import Tags
from forum.forms import AskForm
from activities.models import *
import json
from nodes.models import Comments
from django.db.models import Q


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
    if 'qid' in request.GET:
        q = request.GET['qid']
        question = Question.objects.get(id=q)
        print("question found")
        user = request.user
        try:
            vote = Activity.objects.get(user=user, question=question, activity='U')
            vote.delete()
            # user.userprofile.unotify_q_upvoted(question)
            question.votes -=1
            question.save()
        except Exception:
            vote = Activity.objects.create(user=user, question=question, activity='U')
            vote.save()
            # user.userprofile.notify_q_upvoted(question)
            question.votes +=1
            question.save()
        return HttpResponse()
    elif 'aid' in request.GET:
        a = request.GET['aid']
        answer = Answer.objects.get(id=a)
        user = request.user
        try:
            vote = Activity.objects.get(user=user, answer=answer, activity='U')
            vote.delete()
            # user.userprofile.unotify_a_upvoted(answer)
            answer.votes -= 1
            answer.save()
        except Exception:
            vote = Activity.objects.create(user=user, answer=answer, activity='U')
            vote.save()
            # user.userprofile.notify_a_upvoted(answer)
            answer.votes += 1
            answer.save()
        return HttpResponse()


def votedown(request):
    if 'qid' in request.GET:
        q = request.GET['qid']
        question = Question.objects.get(id=q)
        user = request.user
        try:
            vote = Activity.objects.get(user=user, question=question, activity='D')
            vote.delete()
            # user.userprofile.unotify_q_downvoted(question)
            question.votes -= 1
            question.save()
        except Exception:
            vote = Activity.objects.create(user=user, question=question, activity='D')
            vote.save()
            # user.userprofile.notify_q_downvoted(question)
            question.votes += 1
            question.save()
        return HttpResponse()
    elif 'aid' in request.GET:
        a = request.GET['aid']
        answer = Answer.objects.get(id=a)
        user = request.user
        try:
            vote = Activity.objects.get(user=user, answer=answer, activity='D')
            # User.
            vote.delete()
            # user.userprofile.unotify_a_downvoted(answer)
            answer.votes += 1
            answer.save()
        except Exception:
            vote = Activity.objects.create(user=user, answer=answer, activity='D')
            vote.save()
            # user.userprofile.notify_a_downvoted(answer)
            answer.votes -= 1
            answer.save()
        return HttpResponse()


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

    return render(request, 'forum/questions.html', locals())


def w_questions(request):           # for team
    user = request.user
    wt = user.userprofile.primary_workplace.workplace_type
    questions = Question.objects.filter(user__userprofile__primary_workplace__workplace_type=wt)

    return render(request, 'forum/questions.html', locals())


def s_questions(request):           # for segments
    user = request.user
    workplace = user.userprofile.primary_workplace
    segments = workplace.segments.all()
    questions = None
    for segment in segments:
        q = Question.objects.filter(Q(tags=segment) | Q(user__userprofile__primary_workplace__segments=segments))

        if questions is None:
            questions = q
        else:
            questions = questions & q

    return render(request, 'forum/questions.html', locals())


# def a_questions(request):           # for SME
#     user = request.user
#     area =


