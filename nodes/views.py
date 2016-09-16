from django.core.urlresolvers import reverse
from PIL import Image
from django.conf import settings
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
from activities.views import create_notifications, delete_notifications


@login_required
def post(request):
    form = UploadImageForm(request.POST, request.FILES)
    if request.method == 'POST':
        response = {}
        r_html = {}
        r_elements = []
        post = request.POST.get('post')
        tag = request.POST.get('tag')
        user = request.user
        type = user.userprofile.primary_workplace.workplace_type
        # node = Node.objects.create(post=post, user=user, w_type=type)
        image0 = request.FILES.get('image0', None)
        image1 = request.FILES.get('image1', None)
        image2 = request.FILES.get('image2', None)
        if not image0:
            if post:
                print('a')
                node = Node.objects.create(post=post, user=user, w_type=type)
        else:
            print('b')
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
        if tag:
            node.set_tags(tag)

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
    user = request.user
    if request.is_ajax():
        dictionary = {}
        direct = [f.name for f in Node._meta.get_fields()]
        direct.remove('title')
        for key in request.POST:
            if key in direct:
                try:
                    dictionary[key] = request.POST[key]
                except:
                    tb = traceback.format_exc()
            else:
                print('unknown key ' + key)
        for key in dictionary:
            setattr(node, key, dictionary[key])
        node.save()
        return HttpResponse()
    if request.method == 'POST':
        node.post = request.POST.get('post')
        node.title = request.POST.get('title')
        tags = request.POST.get('tag')
        anonymous = request.POST.get('anonymous')
        if anonymous == 'true':
            node.anonymous = True
        node.save()
        node.set_tags(tags)
        # add some function to remove unused images from node.images
        return redirect(reverse('nodes:node', kwargs={'slug': node.slug}))
    return render(request, 'nodes/edit.html', locals())

@login_required
def write(request):                 # Write an article
    user = request.user
    if request.is_ajax():
        untitled = Node.objects.get(title='untitled', user=user, category='A')
        dictionary = {}
        direct = [f.name for f in Node._meta.get_fields()]
        direct.remove('title')
        for key in request.POST:
            if key in direct:
                try:
                    dictionary[key] = request.POST[key]
                except:
                    tb = traceback.format_exc()
            else:
                print('unknown key ' + key)
        for key in dictionary:
            setattr(untitled, key, dictionary[key])
        untitled.save()
        return HttpResponse()
    elif request.method == 'POST':
        post = request.POST.get('post')
        title = request.POST.get('title')
        tags = request.POST['tag']
        anonymous = request.POST.get('anonymous')
        draft = request.POST.get('draft')
        untitled = Node.objects.get(title='untitled', user=user, category='A')
        if draft:
            node = Node(post=post, title=title, category='A', user=user, is_active=False)
        elif anonymous=='true':
            node = Node(post=post, title=title, category='A', user=user, anonymous=True)
        else:
            node = Node(post=post, title=title, category='A', user=user)
        node.save()
        images = untitled.images.all()
        for i in images:
            node.images.add(i)
        node.set_tags(tags)
        untitled.delete()
        return redirect(reverse('nodes:node', kwargs={'slug': node.slug}))
    else:
        # new = request.GET.get('new')
        try:
            untitled = Node.objects.get(title='untitled', user=user, category='A')
        except:
            untitled = None
        if untitled:
            untitled.delete()
        node = Node.objects.create(title='untitled', user=user, category='A')
        return render(request, 'nodes/write.html', locals())

@login_required
def remove_anonymity(request):
    id = request.GET['id']
    article = Node.objects.get(id=id)
    article.is_active = True
    article.anonymous = False
    article.save()
    return redirect(reverse('nodes:node', kwargs={'slug': node.slug}))

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
            delete_notifications(from_user=user, to_user=node.user, typ='L', node=node)
        except Exception:
            lik = Activity.objects.create(user=user, node=node, activity='L')
            lik.save()
            create_notifications(from_user=user, to_user=node.user, typ='L', node=node)
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
        com = request.POST['comment']
        c = Comments.objects.create(user=user, node=node, comment=com)
        create_notifications(from_user=user, to_user=node.user, typ='C', node=node)
        # create_notifications(from_user=user, to_user=node.user, typ='S', node=node) # also commented
        r_elements = ['comments']
        r_html['comments'] = render_to_string('snippets/comment.html', {'comment':c})
        response['html'] = r_html
        response['elements'] = r_elements
        response['append'] = True
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


def add_image(request):
    if request.is_ajax():
        user = request.user
        image = request.FILES.get('image', None)
        untitled = Node.objects.get(title='untitled', user=user, category='A')
        file = Image.open(image)
        i = Images()
        i.upload_image_new(file=file, user=user, name=image.name)
        link = i.get_full_image()
        untitled.images.add(i)
        # print(len(untitled.images.all()))
        response = {'link': link, 'success': 'Uploaded'}
        return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        return HttpResponse()

def change_image(request, id):
    if request.is_ajax():
        user = request.user
        image = request.FILES.get('image', None)
        node = Node.objects.get(id=id)
        file = Image.open(image)
        i = Images()
        i.upload_image_new(file=file, user=user, name=image.name)
        link = i.get_full_image()
        node.images.add(i)
        # print(len(untitled.images.all()))
        response = {'link': link, 'success': 'Uploaded'}
        return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        return HttpResponse()



# Create your views here.