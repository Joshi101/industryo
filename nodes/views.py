from django.shortcuts import render, redirect, HttpResponseRedirect
from nodes.forms import *
from nodes.models import *
from workplaceprofile.models import WorkplaceProfile
from activities.models import Activity, Notification


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
            wp.save()
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
        return redirect('/user/'+request.user.username)
    else:
        print("fuck3")
        return redirect('/')


def like(request):
    if 'id' in request.GET:
        q = request.GET['id']
        node = Node.objects.get(id=q)
        user = request.user

        try:
            lik = Activity.objects.get(user=user, node=node, activity='L')
            # User.
            lik.delete()

        except Exception:
            lik = Activity.objects.create(user=user, node=node, activity='L')
            lik.save()

        return redirect('/nodes/'+ str(node.pk))
    else:
        return redirect('/')


def comment(request):
    if request.method == 'POST':
        node_id = request.POST['node']
        node = Node.objects.get(pk=node_id)
        post = request.POST['post']
        post = post.strip()
        if len(post) > 0:
            post = post[:500]
            user = request.user
            node.comment(user=user, post=post)
            # myuser.myuserprofile.notify_commented(node)
            # myuser.myuserprofile.notify_also_commented(node)

        return HttpResponseRedirect('/')
    else:
        node_id = request.GET.get('node')
        node = Node.objects.get(pk=node_id)
        return render(request, 'feeds/partial_feed_comments.html', {'node': node})


def node(request, id):
    node = Node.objects.get(id=id)
    # if node:
    #     print(name)
    return render(request, 'nodes/one_node.html', {'node': node})





# Create your views here.
