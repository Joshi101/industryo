from django.shortcuts import render, redirect, HttpResponseRedirect
from nodes.forms import *
from nodes.models import *
from workplaceprofile.models import WorkplaceProfile


def post(request):
    if request.method == 'POST':
        post = request.POST['post']
        user = request.user

        node = Node(post=post, user=user)
        node.save()
        return redirect('/')
    else:
        return redirect('/')


def write(request):                 ## Write an article
    if request.method == 'POST':
        post = request.POST['post']
        title = request.POST['title']
        user = request.user
        tags = request.POST['tags']

        node = Node(post=post, title=title, category='A', user=user)
        node.save()
        node.set_tags(tags)
        # return HttpResponseRedirect('/nodes/'+node.slug)
        return redirect('/')
    else:
        return render(request, 'nodes/write.html', locals())


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
    form = SetProfileImageForm(request.POST, request.FILES)
    if request.method == 'POST':
        if not form.is_valid():
            print("fuck")
            return render(request, 'nodes/set_logo.html', {'form': form})
        else:
            user = request.user
            userprofile = user.userprofile
            image = form.cleaned_data.get('image')
            i = Images.objects.create(image=image, user=user, caption='lalala', image_thumbnail=image)
            userprofile.profile_image = i
            userprofile.save()
        return redirect('/')
    else:
        return redirect('/')


# Create your views here.
