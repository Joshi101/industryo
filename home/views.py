from django.shortcuts import render, redirect, render_to_response, RequestContext
from nodes.models import *
from userprofile.models import UserProfile
from tags.models import Tags
from forum.models import Question, Answer
from django.db.models import Q


def home(request):
    if request.user.is_authenticated():
        user = request.user
        if request.user.userprofile.primary_workplace:
            # name = user.username
            workplace = request.user.userprofile.primary_workplace
            profile = UserProfile.objects.get(user=user)
            workplace = profile.primary_workplace
            job_position = profile.job_position
            t = workplace.workplace_type

            related_node = Node.feed.filter(user__userprofile__primary_workplace__workplace_type=t)
            # questions = Question.objects.filter(user__userprofile__primary_workplace=workplace)
            # content1 = Node.objects.filter(user__workplace__workplace_type=t)
            # content2 = Question.objects.filter(tags=user.userprofile.interests)
            content3 = Question.objects.filter(user__userprofile__primary_workplace__workplace_type=t)
            content4 = Question.objects.filter(answer__question__user__userprofile__primary_workplace__workplace_type=t)
            # content5 = Question.objects.filter(tags=workplace.tags)
            # related_node = Q(Node.objects.filter(user__workplace__workplace_type=t))\
            #                | Q(Question.objects.filter(user__userprofile__primary_workplace=workplace))\
            #                | Q(Answer.objects.filter(question__user__userprofile__primary_workplace=workplace))

            return render(request, 'home.html', locals())
        else:
            return redirect('/set/')
    else:
        return render(request, 'home.html', locals())


def search(request):
    if 'q' in request.GET:
        return redirect('/search/')

    else:
        return render(request, 'search/search.html')


# def content(request):
#     user = request.user
#     workplace = request.user.userprofile.workplace
#     type = workplace.workplace_type
#     questions = Question.objects.filter(Q(user__workplace__workplace_type=type)|Q(tags=user.userprofile.interests)|Q(user__userprofile__workplace=workplace)|Q(tags=workplace.tags))
#     content1 = Node.objects.filter(user__workplace__workplace_type=type)
#     content2 = Question.objects.filter(tags=user.userprofile.interests)
#     content3 = Question.objects.filter(user__userprofile__workplace=workplace)
#     content4 = Question.objects.filter(question__user__userprofile__workplace=workplace)
#     content5 = Question.objects.filter(tags=workplace.tags)


#|Q(tags=workplace.tags)

#
# def set_workplace(request):
#     if request.method == 'POST':




