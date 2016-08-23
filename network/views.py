from operator import attrgetter
from itertools import chain
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from nodes.models import Node
from nodes.forms import UploadImageForm
from userprofile.models import UserProfile
from workplace.models import Workplace, WpTags
from forum.models import Question
from tags.models import Tags
from leads.models import Leads
from products.models import Products, Category


@login_required
@user_passes_test(lambda u: u.userprofile.workplace_type != 'N', login_url='/set')
def network(request):
    workplace = request.user.userprofile.primary_workplace
    tags = workplace.get_tags()
    return render(request, 'home.html', locals())


def network_companies(request):
    tags = request.POST.get('tags')
    user = request.user
    t = user.workplace_type
    companies = Workplace.objects.filter(id=0)
    if t in ['A', 'B']:
        li = ['A', 'B']
    else:
        li = ['C', 'O']
    for tag in tags:
        wps = tag.wptags.filter(workplace_type__in=li)
        companies = companies | wps
    return render(request, 'home.html', locals())


def network_feeds(request):
    tags = request.POST.get('tags')
    user = request.user
    t = user.workplace_type
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


def network_products(request):
    tags = request.POST.get('tags')
    user = request.user
    t = user.workplace_type
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
    return render(request, 'home.html', locals())


def side_overview(request):
    pass


def tag_list(request):
    user = request.user

    t = request.GET.get('what')
    tags = Tags.objects.filter(type=t).order_by('-count')
    return render(request, 'home.html', locals())