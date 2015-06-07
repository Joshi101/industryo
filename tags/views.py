from django.shortcuts import render, redirect, render_to_response
from tags.forms import CreateTagForm
from tags.models import Tags
from forum.models import Question
from workplace.models import Workplace
from nodes.models import Node
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def create_tag(request):
    form = CreateTagForm(request.POST)
    if request.method == 'POST':
        if not form.is_valid():
            print("form invalid")
            return render(request, 'tags/create.html', {'form': form})
        else:
            tag = form.cleaned_data.get('tag')
            description = form.cleaned_data.get('description')

            t, created = Tags.objects.get_or_create(tag=tag, description=description)
            t.number += 1
            t.save()

            return render(request, 'tags/create.html', {'form': form})
    else:
        return render(request, 'tags/create.html', {'form': CreateTagForm()})


def search_tag(request):
    if request.method == 'GET':
        t = request.GET['the_query']
        create = request.GET['the_create']
        # term = request.GET(tag)
        o = Tags.objects.filter(tag__icontains=t)[:6]
        # o = Tags.objects.get(name=t)

        return render(request, 'tags/list.html', {'o': o, 'create': create})
    else:
        return render(request, 'tags/list.html')

def search_interests(request):                  # for searching the workplace
    if request.method == 'GET':
        n = request.GET['the_query']
        o = Tags.objects.filter(tag__icontains=n)[:6]
        create = request.GET['the_create']
        return render(request, 'tags/list.html', {'o': o, 'create': create})
    else:
        return render(request, 'tags/list.html')

def get_tag(request, slug):
    tag = Tags.objects.get(slug=slug)
    if tag:

        questions = Question.objects.filter(tags=tag)
        workplaces = Workplace.objects.filter(tags=tag)
        articles = Node.article.filter(tags=tag)

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


# Create your views here.
