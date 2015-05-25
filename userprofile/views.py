from django.shortcuts import render
from django.contrib.auth.models import User
from userprofile.models import UserProfile


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




# Create your views here.
