from PIL import Image
from django.shortcuts import render, redirect, HttpResponse
from workplace.models import *
from nodes.models import Node
from products.models import Products
from forum.models import Question
from nodes.forms import SetLogoForm
from activities.models import Enquiry
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from itertools import chain
from operator import attrgetter
from workplace.views import no_hits
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from nodes.models import Images
from threading import Thread


def workplace_profile(request, slug):
    workplace_logo_form = SetLogoForm()
    workplace = Workplace.objects.get(slug=slug)
    if request.user.is_authenticated():
        usrprofile = request.user.userprofile
        if workplace.id == usrprofile.primary_workplace_id:
            member = True
    content_url = "workplace/snip_about.html"
    content_head_url = "workplace/snip_about_head.html"
    if request.is_ajax():
        return render(request, content_url, locals())
    else:
        t = Thread(target=no_hits, args=(workplace.id,))
        t.start()
        meta = True
        return render(request, 'workplace/profile.html', locals())


def dashboard(request, slug):
    workplace = Workplace.objects.get(slug=slug)
    if request.user.is_authenticated():
        workplace_logo_form = SetLogoForm()
        if request.user.is_authenticated():
            if request.user.userprofile in workplace.userprofile_set.all():
                member = True
        content_url = "workplace/snip_dashboard.html"
        content_head_url = "workplace/snip_dashboard_head.html"
        member_count = workplace.userprofile_set.all().count()
        products = Products.objects.filter(producer=workplace.pk)
        inquiry_count = Enquiry.objects.filter(product__in=products).count()
        new_inq_count = Enquiry.objects.filter(product__in=products, seen=False).count()
        com_mail = request.user.userprofile.product_email

        node_count = Node.objects.filter(user__userprofile__primary_workplace=workplace).count()

        completion_score = (workplace.get_tags_score() + workplace.get_product_score() + workplace.get_info_score() +
                            (workplace.points)/(10*member_count) + workplace.get_member_score())/5
        if request.is_ajax():
            return render(request, content_url, locals())
        else:
            t = Thread(target=no_hits, args=(workplace.id,))
            t.start()
            meta = True
            return render(request, 'workplace/profile.html', locals())
    else:
        return redirect('/workplace/'+workplace.slug)


def activity(request, slug):
    workplace = Workplace.objects.get(slug=slug)
    workplace_logo_form = SetLogoForm()
    if request.user.is_authenticated():
        if request.user.userprofile in workplace.userprofile_set.all():
            member = True
    questions = Question.objects.filter(user__userprofile__primary_workplace=workplace).select_related('user')
    answers = Question.objects.filter(answer__user__userprofile__primary_workplace=workplace).select_related('user')
    feeds = Node.objects.filter(user__userprofile__primary_workplace=workplace, category__in=['F', 'D']).select_related('user')
    articles = Node.objects.filter(user__userprofile__primary_workplace=workplace, category='A').select_related('user')
    all_result_list = sorted(
        chain(feeds, questions, answers, articles),
        key=attrgetter('date'), reverse=True)
    paginator = Paginator(all_result_list, 5)
    page = request.GET.get('page')
    try:
        result_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        result_list = paginator.page(1)
    except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
        return
        # result_list = paginator.page(paginator.num_pages)
    if page:
        return render(request, 'nodes/five_nodes.html', {'result_list': result_list})
    else:
        content_url = "workplace/snip_activity.html"
        content_head_url = "workplace/snip_activity_head.html"
        if request.is_ajax():
            return render(request, content_url, locals())
        else:
            t = Thread(target=no_hits, args=(workplace.id,))
            t.start()
            meta = True
            return render(request, 'workplace/profile.html', locals())


def products(request, slug):
    workplace = Workplace.objects.get(slug=slug)
    workplace_logo_form = SetLogoForm()
    if request.user.is_authenticated():
        if request.user.userprofile in workplace.userprofile_set.all():
            member = True
    content_url = "workplace/snip_products.html"
    content_head_url = "workplace/snip_products_head.html"
    products = workplace.products_set.all()
    if request.is_ajax():
        return render(request, content_url, locals())
    else:
        t = Thread(target=no_hits, args=(workplace.id,))
        t.start()
        meta = True
        return render(request, 'workplace/profile.html', locals())


def members(request, slug):
    workplace = Workplace.objects.get(slug=slug)
    workplace_logo_form = SetLogoForm()
    if request.user.is_authenticated():
        if request.user.userprofile in workplace.userprofile_set.all():
            member = True
    content_url = "workplace/snip_members.html"
    content_head_url = "workplace/snip_members_head.html"
    if request.is_ajax():
        return render(request, content_url, locals())
    else:
        t = Thread(target=no_hits, args=(workplace.id,))
        t.start()
        meta = True
        return render(request, 'workplace/profile.html', locals())


@login_required
def set_logo(request):
    user = request.user
    workplace = user.userprofile.primary_workplace
    if request.method == 'POST':
        image = request.FILES.get('image')
        transformation = request.POST.get('transformation')
        trans = transformation.split(',')
        x = float(trans[4])
        y = float(trans[5])
        scale = float(trans[0])
        x1 = -x/scale
        y1 = -y/scale
        x2 = (-x+250)/scale
        y2 = (-y+250)/scale
        box = (x1, y1, x2, y2)
        image1 = Image.open(image)
        img = image1.crop(box)
        i = Images()
        x = i.upload_image1(image=img, user=user, name=image.name, image1=image)
        x.save()
        workplace.logo = x
        workplace.save()
        return HttpResponse()
    else:
        return render(request, reverse('workplace:edit'))
