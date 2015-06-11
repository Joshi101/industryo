from django.shortcuts import render, redirect, render_to_response, RequestContext
from nodes.models import Node
from nodes.forms import UploadImageForm
from userprofile.models import UserProfile
from forum.models import Question
from itertools import chain
from allauth.account.forms import AddEmailForm, ChangePasswordForm
from allauth.account.forms import LoginForm, ResetPasswordKeyForm
from allauth.account.forms import ResetPasswordForm, SetPasswordForm, SignupForm, UserTokenForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from operator import attrgetter


def home(request):
    if request.user.is_authenticated():
        user = request.user
        if request.user.userprofile.primary_workplace:
            # name = user.username
            profile = UserProfile.objects.select_related('primary_workplace__workplace_type').get(user=user)
            workplace = profile.primary_workplace       # .select_related('workplaceprofile')
            job_position = profile.job_position
            t = workplace.workplace_type

            related_node = Node.feed.filter(w_type=t).select_related('user__userprofile')
            # questions = Question.objects.filter(user__userprofile__primary_workplace=workplace)
            # content1 = Node.objects.filter(user__workplace__workplace_type=t)
            # content2 = Question.objects.filter(tags=user.userprofile.interests)
            content3 = Question.objects.all()            # filter(user__userprofile__primary_workplace__workplace_type=t).select_related('user__userprofile')
            content4 = Question.objects.filter(answer__question__user__userprofile__primary_workplace__workplace_type=t).select_related('user__userprofile')
            # content5 = Answer.objects.filter(question__)
            all_result_list = sorted(
                chain(related_node, content3, content4),
                key=attrgetter('date'), reverse=True)
                # key=lambda instance: ('-instance.date'))
            paginator = Paginator(all_result_list, 5)
            page = request.GET.get('page')

            try:
                result_list = paginator.page(page)
            except PageNotAnInteger:
                # If page is not an integer, deliver first page.
                result_list = paginator.page(1)
            except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
                return
                # result_list = paginator.page(paginator.num_pages)
            if page:
                return render(request, 'nodes/five_nodes.html', {'result_list': result_list})
            else:
                return render(request, 'home.html', {'result_list': result_list, 'workplace':workplace, 'feed_img_form':UploadImageForm()})
        else:
            return redirect('/set/')
    else:
        return render(request, 'cover.html',{'form_signup':SignupForm(), 'form_login':LoginForm()})


def search(request):
    if 'q' in request.GET:
        return redirect('/search/')
    else:
        return render(request, 'search/search.html')


# def content(request):
#     user = request.user
#     workplace = request.user.userprofile.workplace
#     type = workplace.workplace_type
#     questions = Question.objects.filter(Q(user__workplace__workplace_type=type)|Q(tags=user.userprofile.interests)
# |Q(user__userprofile__workplace=workplace)|Q(tags=workplace.tags))
#     content1 = Node.objects.filter(user__workplace__workplace_type=type)
#     content2 = Question.objects.filter(tags=user.userprofile.interests)
#     content3 = Question.objects.filter(user__userprofile__workplace=workplace)
#     content4 = Question.objects.filter(question__user__userprofile__workplace=workplace)
#     content5 = Question.objects.filter(tags=workplace.tags)


#|Q(tags=workplace.tags)

#
# def set_workplace(request):
#     if request.method == 'POST':
