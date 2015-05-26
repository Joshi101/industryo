from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from userprofile.models import UserProfile
from userprofile.forms import SetSkillsForm


def profile(request, slug):
    user = User.objects.get(username=slug)
    name = user.get_full_name()
    userprofile = UserProfile.objects.get(user=user)
    return render(request, 'userprofile/profile.html', locals())


# def tab_info(request):
#     user = request.user
#     userprofile = UserProfile.objects.get(user=user)
#     full_name = User.get_full_name()
#     try:
#         image = UserProfile.profile_image_url()
#     except Exception:
#         image = userprofile.get_image_thumbnail()
#     points = userprofile.points
#
#     return

def set_skills(request):
    form = SetSkillsForm(request.POST)
    if request.method == 'POST':
        if not form.is_valid():
            print("fuck")
            return redirect('/')
        else:
            user = request.user
            up = user.userprofile

            skills = form.cleaned_data.get('skills')
            up.set_skills(skills)
            return render(request, 'userprofile/set_skills.html', {'form': form})
    else:
        return render(request, 'userprofile/set_skills.html', {'form': form})



# Create your views here.
