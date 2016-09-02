from operator import attrgetter
from itertools import chain
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from nodes.models import Node
from workplace.models import Workplace, WpTags, Connections
from forum.models import Question
from tags.models import Tags
from leads.models import Leads
from products.models import Products, Category
from activities.views import create_notifications
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@login_required
@user_passes_test(lambda u: u.userprofile.workplace_type != 'N', login_url='/set')
def network(request):
    workplace = request.user.userprofile.primary_workplace
    tags = workplace.get_tags()
    if len(tags['city']) == 0 or len(tags['segments']) == 0:
        add_tags = True
    return render(request, 'network.html', locals())


def network_companies(request):
    data = request.POST.get('data').split(',')
    tags = Tags.objects.filter(tag__in=data)
    user = request.user
    t = user.userprofile.primary_workplace.workplace_type
    workplaces = []
    connections = user.userprofile.primary_workplace.get_connection_list()
    # connections = [850, 2, 235, 701]
    if t in ['A', 'B']:
        li = ['A', 'B']
    else:
        li = ['C', 'O']
    for tag in tags:
        wps = tag.wptags.filter(workplace_type__in=li)
        for w in wps:
            if not w in workplaces:
                workplaces.append(w)
    paginator = Paginator(workplaces, 20)
    page = request.GET.get('page')
    try:
        result_list = paginator.page(page)
    except PageNotAnInteger:
        result_list = paginator.page(1)
    except EmptyPage:
        return
    if page:
        return render(request, 'network/companies.html', {'workplaces': result_list, 'connections': connections})
    else:
        return render(request, 'network/20_companies.html', {'workplaces': result_list, 'connections': connections})


def network_feeds(request):
    data = request.POST.get('data').split(',')
    tags = Tags.objects.filter(tag__in=data)
    user = request.user
    t = user.userprofile.primary_workplace.workplace_type
    companies = Workplace.objects.filter(id=0)
    if t in ['A', 'B']:
        li = ['A', 'B']
    else:
        li = ['C', 'O']
    for tag in tags:
        wps = tag.wptags.filter(workplace_type__in=li)
        companies = companies | wps
    related_node = Node.objects.filter(user__userprofile__primary_workplace__in=companies)\
        .select_related('user__userprofile')
    question = Question.objects.filter(user__userprofile__primary_workplace__in=companies)\
        .select_related('user__userprofile')
    all_result_list = sorted(
        chain(related_node, question),
        key=attrgetter('date'), reverse=True)
    paginator = Paginator(all_result_list, 10)

    page = request.GET.get('page')
    try:
        result_list = paginator.page(page)
    except PageNotAnInteger:
        result_list = paginator.page(1)
    except EmptyPage:
        return
    if page:
        return render(request, 'network/feed_list.html', locals())
    else:
        return render(request, 'network/feed_list.html', locals())


def network_products(request):
    data = request.POST.get('data').split(',')
    tags = Tags.objects.filter(tag__in=data)
    user = request.user
    t = user.userprofile.primary_workplace.workplace_type
    companies = Workplace.objects.filter(id=0)
    if t in ['A', 'B']:
        li = ['A', 'B']
    else:
        li = ['C', 'O']
    for tag in tags:
        wps = tag.wptags.filter(workplace_type__in=li)
        companies = companies | wps
    products1 = Products.objects.filter(producer__in=companies, product_type='C')
    products2 = Products.objects.filter(producer__in=companies, product_type__in=['A', 'B'])

    return render(request, 'network/products.html', locals())


def tag_list(request):
    user = request.user
    t = request.GET.get('what')
    tags = Tags.objects.filter(type=t).order_by('-count')
    return render(request, 'network.html', locals())


def side_overview(request):
    data = request.POST.get('data').split(',')
    locations = Tags.objects.filter(tag__in=data)
    segments = Tags.objects.filter(tag__in=data)
    return render(request, 'network/side_over.html', locals())


@csrf_exempt
def add_tag(request):
    if request.method == 'POST':
        user = request.user
        wp = user.userprofile.primary_workplace
        tid = request.POST.get('id')
        tag = Tags.objects.get(id=tid)
        ttype = request.POST.get('type')
        wp.set_tags(tags=tag.tag, typ=ttype, primary=False)
        return HttpResponse()


def search_tags(request):
    if request.method == 'POST':
        name = request.POST.get('query')
        tags1 = Tags.objects.filter(type__in=['C', 'I'], tag__icontains=name).order_by('-count')[20]
        tags2 = Tags.objects.filter(type__in=['S', 'O'], tag__icontains=name).order_by('-count')[20]
    else:
        tags1 = Tags.objects.filter(type__in=['C', 'I']).order_by('-count')[:20]
        tags2 = Tags.objects.filter(type__in=['S', 'O']).order_by('-count')[:20]
    return render(request, 'network/add_tags_list.html', locals())


def connect(request):
    if request.method == 'POST':
        user = request.user
        wp = user.userprofile.primary_workplace
        wid = request.POST.get('id')
        other = Workplace.objects.get(id=wid)
        ctype = request.POST.get('type')
        try:
            c = Connections.objects.get(my_company=wp, other_company=other)
        except Exception:
            Connections.objects.create(my_company=wp, other_company=other, type=ctype)
        create_notifications(from_user=user, to_users=wp.get_members_user(), workplace=wp, typ='N')
        return HttpResponse()
