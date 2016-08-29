from django.shortcuts import render, redirect, render_to_response, HttpResponse
from tags.forms import CreateTagForm
from tags.models import Tags, TagRelations
from forum.models import Question
from workplace.models import WpTags
from nodes.models import Node
from nodes.forms import SetTagLogoForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from itertools import chain
from operator import attrgetter
from products.models import Products
from leads.models import Leads
from django.db.models import Q
from django.contrib.auth.models import User


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
        if type == 'All':
            o = Tags.objects.filter(tag__icontains=tag)[:6]
        else:
            o = Tags.objects.filter(type=type, tag__icontains=tag)[:6]
        return render(request, 'tags/list.html', {'objects': o})
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
    wptag = tag.wptags.all()
    questions = Question.objects.filter(tags=tag)
    workplaces = tag.wptags.all()
    nodes1 = Node.objects.filter(tags=tag)
    nodes2 = Node.objects.filter(user__userprofile__primary_workplace__in=wptag)
    nodes = nodes1 | nodes2
    articles = Node.article.filter(tags=tag)
    tag_logo_form = SetTagLogoForm()
    wptags = WpTags.objects.filter(tags=tag)
    all_result_list = sorted(
        chain(nodes, questions),
        key=attrgetter('date'), reverse=True)
    paginator = Paginator(all_result_list, 5)
    page = request.GET.get('page')
    try:
        result_list = paginator.page(page)
    except PageNotAnInteger:
        result_list = paginator.page(1)
    except EmptyPage:
        return
    if page:
        return render(request, 'nodes/five_nodes.html', {'result_list': result_list, 'wptags':wptags})
    else:
        content_url = "tags/snip_activity.html"
        content_head_url = "tags/snip_activity_head.html"
        if request.is_ajax():
            return render(request, content_url, locals())
        else:
            meta = True
            return render(request, 'tags/tag.html', locals())


def tag_products(request, slug):
    tag = Tags.objects.get(slug=slug)
    wptags = tag.wptags.all()
    products = Products.objects.filter(producer__in=wptags)
    content_url = "tags/snip_products.html"
    content_head_url = "tags/snip_products_head.html"
    if request.is_ajax():
        return render(request, content_url, locals())
    else:
        meta = True
        return render(request, 'tags/tag.html', locals())


def tag_companies(request, slug):
    tag = Tags.objects.get(slug=slug)
    workplaces = tag.wptags.all()
    content_url = "tags/snip_companies.html"
    content_head_url = "tags/snip_companies_head.html"
    if request.is_ajax():
        return render(request, content_url, locals())
    else:
        meta = True
        return render(request, 'tags/tag.html', locals())


def tag_leads(request, slug):
    tag = Tags.objects.get(slug=slug)
    leads = Leads.objects.filter(tags=tag)
    content_url = "tags/snip_leads.html"
    content_head_url = "tags/snip_leads_head.html"
    if request.is_ajax():
        return render(request, content_url, locals())
    else:
        meta = True
        return render(request, 'tags/tag.html', locals())


def get_all_tags(request):
    all_tags = Tags.objects.all()
    paginator = Paginator(all_tags, 20)
    page = request.GET.get('page')
    try:
        tags = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        tags = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        tags = paginator.page(paginator.num_pages)
    if page:
        return render_to_response('tags/20_tags.html', {"tags": tags})
    else:
        return render(request, 'tags/all_tags.html', {"tags": tags})
    # return render(request, 'tags/list1.html', locals())


def search_n_tags(request):
    tag = request.GET['the_query']
    type = request.GET['the_type']
    o = Tags.objects.filter(type=type, tag__icontains=tag)
    create = request.GET['the_create']
    return render(request, 'tags/list.html', {'o': o, 'create': create})


@login_required
def describe_tag(request):          # edit description
    if request.method == 'POST':
        id = request.POST.get('id')
        tag = Tags.objects.get(id=id)
        description = request.POST['description']
        tag.description = description
        tag.save()
        return HttpResponse()
    else:
        return redirect('/tags/')


@login_required
def follow_tag(request):
    user = request.user
    id = request.GET.get('id')
    tag = Tags.objects.get(id=id)
    t = user.userprofile.set_interests(tag.tag)
    if request.GET.get('wp'):
        if user.userprofile.workplace_type != 'N':
            wp = user.userprofile.primary_workplace
            type = tag.type
            if type in ['C', 'I']:
                wp.set_city(tag.tag)
            if type == 'S':
                wp.set_segments(tag.tag)
            if type == 'O':
                wp.set_operations(tag.tag)
            if type == 'A':
                wp.set_assets(tag.tag)
            if type == 'M':
                wp.set_materials(tag.tag)

    return redirect('/network')


def create(request):
    pass


def merge_tags(remain, destroy):
    remain = Tags.objects.get(id=remain)
    destroy = Tags.objects.get(id=destroy)

    ws = WpTags.objects.filter(tags=destroy)
    for w in ws:
        ee = WpTags.objects.filter(tags=remain, workplace=w.workplace).first()
        if ee:
            w.delete()
        else:
            w.tags = remain
            w.save()
    remain.count += destroy.count
    if remain.other_names:
        remain.other_names = remain.other_names + ','+destroy.tag
    else:
        remain.other_names = destroy.tag
    remain.save()

    us = User.objects.filter(userprofile__interests=destroy)
    for u in us:
        u.userprofile.set_interests(remain.tag)

    ts1 = TagRelations.objects.filter(tag1=destroy)
    ts2 = TagRelations.objects.filter(tag2=destroy)
    for t in ts1:
        if not t.tag2 == remain:
            i = TagRelations.objects.filter(Q(tag1=remain, tag2=t.tag2) | Q(tag2=remain, tag1=t.tag2)).first()
            if i:
                i.count += 1
                i.save()
            else:
                t.tag1 = remain
                t.save()
        else:
            t.delete()
    for t in ts2:
        if not t.tag1 == remain:
            i = TagRelations.objects.filter(Q(tag1=remain, tag2=t.tag1) | Q(tag2=remain, tag1=t.tag1)).first()
            if i:
                i.count += 1
                i.save()
            else:
                t.tag2 = remain
                t.save()
        else:
            t.delete()
    destroy.delete()





# Create your views here.
