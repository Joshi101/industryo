from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from userprofile.models import UserProfile
from userprofile.forms import EditProfileForm, SetSkillsForm, UserDetailsForm
from nodes.forms import *
from forum.models import Question, Answer
from nodes.models import Node
from django.contrib.auth.decorators import login_required
from tags.models import Tags


def profile(request, username):
    user = User.objects.get(username=username)
    name = user.get_full_name()
    userprofile = UserProfile.objects.get(user=user)
    profile_image_form = SetProfileImageForm()

    questions = Question.objects.filter(user=user)
    answers = Answer.objects.filter(user=user)
    feeds = Node.feed.filter(user=user)
    articles = Node.article.filter(user=user)
    interests = userprofile.get_interests()
    return render(request, 'userprofile/profile.html', locals())


def set_details(request):
    form = UserDetailsForm(request.POST)
    user = request.user
    if request.method == 'POST':
        if not form.is_valid():
            print("fuck")
            return render(request, 'userprofile/edit.html', {'form': form})
        else:

            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')

            user.first_name = first_name
            user.last_name = last_name
            user.save()
            return redirect('/')
    else:
        form = UserDetailsForm(instance=user, initial={
            'first_name': user.first_name,
            'last_name': user.last_name,
            })
        return render(request, 'userprofile/details.html', {'form': form})


def edit(request):
    form = EditProfileForm(request.POST)
    user = request.user
    up = user.userprofile
    if request.method == 'POST':
        if not form.is_valid():
            print("fuck")
            return render(request, 'userprofile/edit.html', {'form': form})
        else:

            gender = form.cleaned_data.get('gender')
            experience = form.cleaned_data.get('experience')

            up.gender = gender
            up.experience = experience
            up.save()
            return redirect("/user/"+user.username)
    else:
        form = EditProfileForm(instance=user, initial={
            'gender': up.gender,
            'experience': up.experience,
            })
        return render(request, 'userprofile/edit.html', {'form': form})

# @login_required
def set_interests(request):
    print("fucks")
    form = SetSkillsForm(request.POST)
    if request.method == 'POST':
        print("fuck")

        if not form.is_valid():
            print("fucking")
            return redirect('/')
        else:
            print("fucki")

            user = request.user
            print("fuckin")
            print(user)

            up = user.userprofile

            interests = form.cleaned_data.get('skills')
            up.set_interests(interests)
            return redirect('/user/'+user.username)
    else:
        return render(request, 'userprofile/set_interests.html', {'form': form})


def search_area(request):
    if 'the_query' in request.GET:
        t = request.GET['the_query']
        create = request.GET['the_create']
        o = Tags.objects.filter(type='A')[:6]

        return render(request, 'tags/list.html', {'o': o, 'create': create})
    else:
        return render(request, 'tags/list.html')


def set_area(request):
    form = SetSkillsForm(request.POST)
    if request.method == 'POST':
        if not form.is_valid():
            return redirect('/')
        else:
            user = request.user
            up = user.userprofile
            area = form.cleaned_data.get('area')
            up.set_area(area)
            return redirect('/user/'+user.username)
    else:
        return render(request, 'userprofile/set_interests.html', {'form': form})

#
# def get_my_question(request):
#     user = request.user
#     questions = Question.objects.filter(user=user)





# Create your views here.
