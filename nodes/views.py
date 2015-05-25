from django.shortcuts import render, redirect
from nodes.forms import *
from nodes.models import Images
from workplaceprofile.models import WorkplaceProfile


# def set_logo(request):
#     user = request.user


def upload_image(request):
    form = UploadImageForm(request.POST, request.FILES)
    if request.method == 'POST':
        if not form.is_valid():
            print("fuck")
            return render(request, 'nodes/upload.html', {'form': form})
        else:
            user = request.user
            image = form.cleaned_data.get('image')
            caption = form.cleaned_data.get('caption')
            Images.objects.create(image=image, user=user, caption=caption, image_thumbnail=image)
        return redirect('/')
    else:
        return render(request, 'nodes/upload.html', {'form': form})


def set_logo(request):
    form = SetLogoForm(request.POST, request.FILES)
    if request.method == 'POST':
        if not form.is_valid():
            print("fuck")
            return render(request, 'nodes/set_logo.html', {'form': form})
        else:
            user = request.user
            workplace = user.userprofile.primary_workplace
            wp = WorkplaceProfile.objects.get(workplace=workplace)
            image = form.cleaned_data.get('image')
            caption = form.cleaned_data.get('caption')
            i = Images.objects.create(image=image, user=user, caption=caption, image_thumbnail=image)
            wp.logo = i
        return redirect('/')
    else:
        return render(request, 'nodes/upload.html', {'form': form})


def set_profile_image(request):
    form = SetLogoForm(request.POST, request.FILES)
    if request.method == 'POST':
        if not form.is_valid():
            print("fuck")
            return render(request, 'nodes/set_logo.html', {'form': form})
        else:
            user = request.user
            userprofile = user.userprofile

            image = form.cleaned_data.get('image')
            caption = form.cleaned_data.get('caption')
            i = Images.objects.create(image=image, user=user, caption=caption, image_thumbnail=image)
            userprofile.profile_image = i
        return redirect('/')
    else:
        return render(request, 'nodes/upload.html', {'form': form})


# Create your views here.
