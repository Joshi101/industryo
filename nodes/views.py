from django.shortcuts import render, redirect, HttpResponseRedirect, HttpResponse
from django.template.loader import render_to_string
from nodes.forms import *
from nodes.models import *
from workplace.models import Workplace
from activities.models import Activity, Notification
import json
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from products.models import Products, Category
from threading import Thread


@login_required
def post(request):
    form = UploadImageForm(request.POST, request.FILES)
    if request.method == 'POST':
        response = {}
        r_html = {}
        r_elements = []
        post = request.POST.get('post')
        tid = request.POST.get('tid')
        user = request.user
        type = user.userprofile.primary_workplace.workplace_type
        # node = Node.objects.create(post=post, user=user, w_type=type)
        image0 = request.FILES.get('image0', None)
        image1 = request.FILES.get('image1', None)
        image2 = request.FILES.get('image2', None)
        if not image0:
            if post:
                node = Node.objects.create(post=post, user=user, w_type=type)
        else:
            node = Node.objects.create(post=post, user=user, w_type=type)
        if image0:
            i = Images()
            a = i.upload_image(image=image0, user=user)
            node.images.add(a)
        if image1:
            i = Images()
            a = i.upload_image(image=image1, user=user)
            node.images.add(a)
        if image2:
            i = Images()
            a = i.upload_image(image=image2, user=user)
            node.images.add(a)
        if tid:
            node.set_tag(tid)

        r_elements = ['feeds']
        r_html['feeds'] = render_to_string('nodes/one_node.html', {'node': node})
        response['html'] = r_html
        response['elements'] = r_elements
        response['prepend'] = True
        return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        return redirect('/')

@login_required
def edit(request, id):
    node = Node.objects.get(id=id)
    if request.method == 'POST':
        node.post = request.POST.get('post')
        node.title = request.POST.get('title')
        user = request.user
        tags = request.POST['tags']
        anonymous = request.POST.get('anonymous')
        if anonymous == 'true':
            node.anonymous = True
        node.save()
        image0 = request.FILES.get('image0', None)
        image1 = request.FILES.get('image1', None)
        image2 = request.FILES.get('image2', None)
        if image0:
            i = Images()
            a = i.upload_image(image=image0, user=user)
            node.images.add(a)
        if image1:
            i = Images()
            a = i.upload_image(image=image1, user=user)
            node.images.add(a)
        if image2:
            i = Images()
            a = i.upload_image(image=image2, user=user)
            node.images.add(a)
        # node.set_tags(tags)
        return redirect('/nodes/articles')
    return render(request, 'nodes/edit.html', locals())

@login_required
def write(request):                 ## Write an article
    if request.method == 'POST':
        post = request.POST.get('post')
        title = request.POST.get('title')
        user = request.user
        tags = request.POST['tag']
        anonymous = request.POST.get('anonymous')
        draft = request.POST.get('draft')

        # if anonymous & draft:
        #     node = Node(post=post, title=title, category='A', user=user, anonymous=True, is_active=False)
        if draft:

            node = Node(post=post, title=title, category='A', user=user, is_active=False)
        elif anonymous=='true':
            node = Node(post=post, title=title, category='A', user=user, anonymous=True)
        else:
            node = Node(post=post, title=title, category='A', user=user)
        node.save()
        image0 = request.FILES.get('image0', None)
        image1 = request.FILES.get('image1', None)
        image2 = request.FILES.get('image2', None)
        if image0:
            i = Images()
            a = i.upload_image(image=image0, user=user)
            node.images.add(a)
        if image1:
            i = Images()
            a = i.upload_image(image=image1, user=user)
            node.images.add(a)
        if image2:
            i = Images()
            a = i.upload_image(image=image2, user=user)
            node.images.add(a)
        node.set_tags(tags)
        return redirect('/nodes/'+node.slug)
    else:
        return render(request, 'nodes/write.html', locals())

@login_required
def remove_anonymity(request):
    id = request.GET['id']
    article = Node.objects.get(id=id)
    article.is_active = True
    article.anonymous = False
    article.save()
    return redirect('/nodes/'+article.slug)

@login_required
def publish(request):
    id = request.GET['id']
    article = Node.objects.get(id=id)
    article.is_active = True
    # article.anonymous = False
    article.save()
    return redirect('/nodes/'+article.slug)



@login_required
def upload_image(request):
    form = UploadImageForm(request.POST, request.FILES)
    if request.method == 'POST':
        if not form.is_valid():
            return render(request, 'nodes/upload.html', {'form': form})
        else:
            user = request.user
            image = form.cleaned_data.get('image')
            caption = form.cleaned_data.get('caption')
            Images.objects.create(image=image, user=user, caption=caption, image_thumbnail=image)
        return redirect('/')
    else:
        return render(request, 'nodes/upload.html', {'form': form})

@login_required
def set_logo(request):
    form = SetLogoForm(request.POST, request.FILES)
    user = request.user
    workplace = user.userprofile.primary_workplace
    if request.method == 'POST':
        if not form.is_valid():
            return render(request, 'nodes/set_logo.html', {'form': form})
        else:
            image = form.cleaned_data.get('image')
            i = Images.objects.create(image=image, user=user, image_thumbnail=image)
            workplace.logo = i
            workplace.save()
        return redirect('/workplace/edit')
    else:
        return render(request, 'nodes/upload.html', {'form': form})

@login_required
def set_tag_logo(request, slug):
    form = SetTagLogoForm(request.POST, request.FILES)
    user = request.user
    tag = Tags.objects.get(slug=slug)
    if request.method == 'POST':
        if not form.is_valid():
            return redirect('/tags/'+slug)
        else:
            image = form.cleaned_data.get('image')
            i = Images.objects.create(image=image, user=user, image_thumbnail=image)
            tag.logo = i
            tag.save()
            return redirect('/tags/'+tag.slug)
    else:
        return render(request, 'nodes/set_logo.html', {'form': form})


@login_required
def set_category_logo(request, slug):
    form = SetCategoryLogoForm(request.POST, request.FILES)
    user = request.user
    category = Category.objects.get(slug=slug)
    if request.method == 'POST':
        if not form.is_valid():
            return redirect('/internal/category/'+slug)
        else:
            image = form.cleaned_data.get('image')
            i = Images.objects.create(image=image, user=user, image_thumbnail=image)
            category.image = i
            category.save()
            return redirect('/internal/category/'+category.slug)
    else:
        return render(request, 'nodes/set_logo.html', {'form': form})

@login_required
def set_profile_image(request):
    form = SetProfileImageForm(request.POST, request.FILES)
    if request.method == 'POST':
        if not form.is_valid():
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
        return redirect('/')


@login_required
def set_product_image(request, slug):
    form = UploadImageForm(request.POST, request.FILES)
    if request.method == 'POST':
        if not form.is_valid():
            return render(request, 'nodes/set_logo.html', {'form': form})
        else:
            user = request.user
            userprofile = user.userprofile
            product = Products.objects.get(slug)
            image = form.cleaned_data.get('image')
            i = Images.objects.create(image=image, user=user, image_thumbnail=image)
            product.image = i
            userprofile.save()
        return redirect('/products/'+product.slug)
    else:
        return redirect('/')


@login_required
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

@login_required
def comment(request):
    if request.method == 'POST':
        response = {}
        r_html = {}
        r_elements = []
        node_id = request.POST['id']
        user = request.user
        node = Node.objects.get(pk=node_id)
        # tram = node.user
        post = request.POST['comment']
        c = Comments(user=user, node=node, comment=post)
        c.save()
        user.userprofile.notify_n_commented(node)
        user.userprofile.notify_also_n_commented(node)
        r_elements = ['comments']
        r_html['comments'] = render_to_string('snippets/comment.html', {'comment':c})
        response['html'] = r_html
        response['elements'] = r_elements
        response['prepend'] = True
        return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        node_id = request.GET.get('node')
        node = Node.objects.get(pk=node_id)
        return render(request, 'feeds/partial_feed_comments.html', {'node': node})


def node(request, slug):
    node = Node.objects.get(slug=slug)
    t = Thread(target=no_hits, args=(node.id,))
    t.start()
    return render(request, 'nodes/node.html', {'node': node})


def no_hits(id):        # dont know ehy not working
    q = Node.objects.get(id=id)
    q.hits +=1
    q.save()


def articles(request):
    articles = Node.article.all()           # here we can use prefetch_related to get tags
    user = request.user
    if user.is_authenticated():
        if user.userprofile.primary_workplace:
            t = user.userprofile.primary_workplace.workplace_type
            workplaces = Workplace.objects.filter(workplace_type=t).order_by('?')[:5]           # change it soon
        else:
            workplaces = Workplace.objects.all().order_by('?')[:5]          # change it soon
    else:
        workplaces = Workplace.objects.all().order_by('?')[:5]          # change it soon

    paginator = Paginator(articles, 5)
    page = request.GET.get('page')

    try:
        result_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        result_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        return
    if page:
        return render(request, 'nodes/five_nodes.html', {'result_list': result_list})
    else:
        # return render(request, 'home.html', {'result_list': result_list})
        return render(request, 'nodes/articles.html', {'result_list': result_list, 'workplaces':workplaces})


def delete(request):
    id = request.GET.get('id')
    node = Node.objects.get(id=id)
    if request.user == node.user:
        node.delete()
    return redirect('/')


def edit_node(request):
    id = request.GET.get('id')
    node = Node.objects.get(id=id)
    if request.method == 'POST':
        user = request.user
        node.post = request.POST['post']
        node.title = request.POST['title']
        node.save()
        image0 = request.FILES.get('image0', None)
        image1 = request.FILES.get('image1', None)
        image2 = request.FILES.get('image2', None)
        if image0:
            i = Images()
            a = i.upload_image(image=image0, user=user)
            node.images.add(a)
        if image1:
            i = Images()
            a = i.upload_image(image=image1, user=user)
            node.images.add(a)
        if image2:
            i = Images()
            a = i.upload_image(image=image2, user=user)
            node.images.add(a)
        tags = request.POST.get('tag')
        node.set_tags(tags)
        slug = node.slug
        return HttpResponseRedirect('/nodes/'+slug)
    else:
        return render(request, 'nodes/articles.html', locals())


def delete_node_image(request):
    nid = request.GET.get('nid')
    pid = request.GET.get('pid')
    image = Images.objects.get(id=pid)
    question = Node.objects.get(id=nid)
    question.images.remove(image)


# def



# Create your views here.