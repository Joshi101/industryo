from django.shortcuts import render, redirect, render_to_response, HttpResponse
from tags.forms import CreateTagForm
from tags.models import Tags
from forum.models import Question
from workplace.models import WpTags
from nodes.models import Node
from nodes.forms import SetTagLogoForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required


def create_tag(request):
    form = CreateTagForm(request.POST)
    if request.method == 'POST':
        if not form.is_valid():
            return render(request, 'tags/create.html', {'form': form})
        else:
            tag = form.cleaned_data.get('tag')
            description = form.cleaned_data.get('description')

            t, created = Tags.objects.get_or_create(tag=tag, description=description)
            t.count += 1
            t.save()

            return render(request, 'tags/create.html', {'form': form})
    else:
        return render(request, 'tags/create.html', {'form': CreateTagForm()})


def search_tag(request):
    if request.method == 'GET':
        tag = request.GET['the_query']
        type = request.GET['the_type']
        if len(tag) >= 2:
            if type == 'All':
                o = Tags.objects.filter(tag__icontains=tag)[:6]
            else:
                o = Tags.objects.filter(type=type, tag__icontains=tag)[:6]
            return render(request, 'tags/list.html', {'objects': o})
        else:
            return render(request, 'tags/list.html', {'objects': 'short'})
    else:
        return render(request, 'tags/list.html')


def search_interests(request):                  # for searching the workplace
    if request.method == 'GET':
        n = request.GET['the_query']
        if len(n) >= 2:
            o = Tags.objects.filter(tag__icontains=n)[:6]
            create = request.GET['the_create']
            return render(request, 'tags/list.html', {'o': o, 'create': create})
        else:
            return HttpResponse('Keep Typing..')
    else:
        return render(request, 'tags/list.html')


def get_tag(request, slug):
    tag = Tags.objects.get(slug=slug)
    questions = Question.objects.filter(tags=tag)
    workplaces = tag.wptags.all()
    articles = Node.article.filter(tags=tag)
    tag_logo_form = SetTagLogoForm()
    wptags = WpTags.objects.filter(tags=tag)

    return render(request, 'tags/tag.html', locals())


def get_all_tags(request):
    all_tags = Tags.objects.all()
    paginator = Paginator(all_tags, 5)
    page = request.GET.get('page')
    try:
        tags = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        tags = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        tags = paginator.page(paginator.num_pages)

    return render_to_response('tags/list1.html', {"tags": tags})
    # return render(request, 'tags/list1.html', locals())


def search_n_tags(request):
    tag = request.GET['the_query']
    type = request.GET['the_type']
    o = Tags.objects.filter(type=type, tag__icontains=tag)
    create = request.GET['the_create']
    return render(request, 'tags/list.html', {'o': o, 'create': create})


@login_required
def describe_tag(request):          # edit description
    print('tag describe dp')
    if request.method == 'POST':
        id = request.POST.get('id')
        tag = Tags.objects.get(id=id)
        description = request.POST['description']
        tag.description = description
        print(tag.description)
        tag.save()
        return HttpResponse()
    else:
        return redirect('/tags/')


# new function to add a follow button to a tag adding it to interests
@login_required
def follow_tag(request):
    user = request.user
    if request.method == 'POST':
        tag = Tags.objects.get(id=request.POST['tag_id'])
        user.useprofile.interest.add(tag)
        return HttpResponse()
    else:
        return redirect('/tags/')



# Create your views here.
