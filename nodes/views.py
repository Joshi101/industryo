from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
from django.template.loader import render_to_string
from nodes.forms import *
from nodes.models import *
from activities.models import Activity, Notification
import json


def post(request):
    form = UploadImageForm(request.POST, request.FILES)
    if request.method == 'POST':
        response = {}
        r_html = {}
        r_elements = []
        post = request.POST.get('post')
        user = request.user
        type = user.userprofile.primary_workplace.workplace_type
        node = Node.objects.create(post=post, user=user, w_type=type)
        # id = node.save()
        # new_nodes = Node.feed.filter(id=id)
        r_elements = ['feeds']
        r_html['feeds'] = render_to_string('nodes/one_node.html', {'node': node})
        response['html'] = r_html
        response['elements'] = r_elements
        response['prepend'] = True
        return HttpResponse(json.dumps(response), content_type="application/json")
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

            image = form.cleaned_data.get('image')
            caption = form.cleaned_data.get('caption')
            i = Images.objects.create(image=image, user=user, caption=caption, image_thumbnail=image)
            workplace.logo = i
            workplace.save()
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
            i = Images.objects.create(image=image, user=user, image_thumbnail=image)
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
            lik.delete()
            user.userprofile.unotify_liked(node)
        except Exception:
            lik = Activity.objects.create(user=user, node=node, activity='L')
            lik.save()
            user.userprofile.notify_liked(node)
        return HttpResponse()
    else:
        return redirect('/')


def comment(request):
    if request.method == 'POST':
        response = {}
        r_html = {}
        r_elements = []
        node_id = request.POST['node']
        user = request.user
        node = Node.objects.get(pk=node_id)
        post = request.POST['post']
        c = Comments(user=user, node=node, comment=post)
        c.save()
        r_elements = ['comments']
        print(c.user)
        r_html['comments'] = render_to_string('snippets/comment.html', {'comment':c})
        response['html'] = r_html
        response['elements'] = r_elements
        response['prepend'] = True
        return HttpResponse(json.dumps(response), content_type="application/json")
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