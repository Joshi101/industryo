from django.shortcuts import render, redirect, HttpResponse
from django.template.loader import render_to_string
from nodes.forms import SetLogoForm
from products.models import *
from workplace.models import Workplace
from userprofile.models import UserProfile
from django.contrib.auth.models import User
from tags.models import Tags
import json
from nodes.models import Images
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.csrf import csrf_exempt
from activities.models import Enquiry
from datetime import datetime, timedelta, time, date
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from nodes.models import Node
from operator import itemgetter
from home.tasks import execute_view
import traceback
from inbox.unified import enquire as unified_inquire


@login_required
def set_tags_short(request, slug):
    if request.method == 'POST':
        p = Products.objects.get(slug=slug)
        response = {}
        r_html = {}
        r_elements = []
        user = request.user
        wp = user.userprofile.primary_workplace
        value = request.POST.get('tag')
        t = p.set_tags(value)

        new_interest = t
        r_elements = ['info_field_value']
        r_html['info_field_value'] = render_to_string(
            'snippets/tag_short.html', {'tags': new_interest})
        response['html'] = r_html
        response['elements'] = r_elements
        response['prepend'] = False
        return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        return redirect('/user/' + request.user.username)


@login_required
def set_details(request, id):
    p = Products.objects.get(id=id)
    user = request.user
    workplace = user.userprofile.primary_workplace
    if request.method == 'POST':
        if p.producer == workplace:
            desc = request.POST.get('desc')
            cost = request.POST.get('cost')
            tags = request.POST.get('prod_tag')
            p.description = desc
            p.cost = cost
            if tags:
                p.set_tags(tags)
            p.save()
            return HttpResponse()
    else:
        return redirect('/products/' + id)


@login_required
def new_category(request):
    if request.method == 'POST':
        id = request.POST.get('new_category_1')
        c2 = request.POST.get('new_category_2')
        c3 = request.POST.get('new_category_3')
        if not c3:
            id = request.POST.get('new_category_1')
            c = Category.objects.get(id=id)
            try:
                a = Category.objects.get(name__iexact=c2)
            except Exception:
                a = Category.objects.create(name=c2, level=2)
            c.sub_cat.add(a)
        elif c3:
            id = request.POST.get('new_category_2')
            c = Category.objects.get(id=id)
            try:
                a = Category.objects.get(name__iexact=c3, level=2)
                if a:
                    change_category(a.slug, c.slug)
            except Exception:
                try:
                    a = Category.objects.get(name__iexact=c3)
                except Exception:
                    a = Category.objects.create(name=c3, level=3)
                c.sub_cat.add(a)
        response = {}
        response['id'] = a.id
        response['name'] = a.name
        return HttpResponse(json.dumps(response), content_type="application/json")


def change_category(a, b):
    cat = Category.objects.get(slug=a)
    cat.level = 3
    cat.save()
    cat2 = Category.objects.get(slug=b)
    cat2.sub_cat.add(a)
    ps = Product_Categories.objects.filter(category=cat)
    for p in ps:
        p.level = 3
        p.save()
        Product_Categories.objects.create(
            product=p.product, level=2, category=cat2)


@login_required
def edit_category(request, id):
    p = Products.objects.get(id=id)
    user = request.user
    workplace = user.userprofile.primary_workplace
    if request.method == 'POST':
        if p.producer == workplace:
            response = {}
            r_html = {}
            r_elements = []
            li = []
            c1 = request.POST.get('category1')
            if c1:
                li.append(c1)
            c2 = request.POST.get('category2')
            if c2:
                li.append(c2)
            c3 = request.POST.get('category3')
            if c3:
                li.append(c3)
            categories = Category.objects.filter(pk__in=li)
            q = Product_Categories.objects.filter(product=p)
            if q:
                q.delete()
            for c in categories:
                Product_Categories.objects.create(
                    product=p, category=c, level=c.level)
            return HttpResponse()
    else:
        return redirect('/products/' + id)


def product(request, slug):
    c1_all = Category.objects.filter(level=1)
    product = Products.objects.get(slug=slug)
    producer = product.producer
    members = producer.get_members()
    tagss = product.tags.all()
    prod_img_form = SetLogoForm()
    # categories = Product_Categories.objects.filter(product_id=product.id).order_by('level')
    categories = product.categories.all()
    all = Products.objects.filter(producer=producer)
    all_list = list(all)
    c = all_list.index(product)
    if not len(all_list) == c + 1:
        next = all_list[c + 1]
    if not c == 0:
        previous = all_list[c - 1]
    return render(request, 'products/product.html', locals())


def delete(request):
    id = request.GET.get('id')
    product = Products.objects.get(id=id)
    if request.user.userprofile.primary_workplace == product.producer:

        product.delete()
    return redirect('/workplace/add_products')


@login_required
def edit_desc(request, id):
    p = Products.objects.get(id=id)
    user = request.user
    workplace = user.userprofile.primary_workplace
    if request.method == 'POST':
        if p.producer == workplace:
            desc = request.POST.get('description')
            p.description = desc
            p.save()
            return redirect('/products/' + p.slug)
    else:
        return redirect('/products/' + p.slug)


@login_required
def change_image(request, id):
    form = SetLogoForm(request.POST, request.FILES)
    p = Products.objects.get(id=id)
    user = request.user
    workplace = user.userprofile.primary_workplace
    if request.method == 'POST':
        if p.producer == workplace:
            image = request.FILES.get('image')
            i = Images.objects.create(
                image=image, user=user, image_thumbnail=image)
            p.image = i
            p.save()
            return redirect('/products/' + p.slug)
    else:
        return redirect('/products/' + p.slug)


def random(request):
    if request.user.is_authenticated():
        user = request.user
        if user.userprofile.primary_workplace:
            a = user.userprofile.primary_workplace.workplace_type
            products = Products.objects.all().order_by('?')[:6]
        else:
            products = Products.objects.all().order_by('?')[:6]
    else:
        products = Products.objects.all().order_by('?')[:6]
    return render(request, 'snippets/right/products.html', {'products': products})


@login_required
def enquiry_all(request):
    return redirect('/inbox')


@login_required
def int_add_product(request):
    c1_all = Category.objects.filter(level=1)
    if request.method == 'POST':
        pro = request.POST.get('product')
        description = request.POST.get('description')
        cost = request.POST.get('cost')
        tags = request.POST.get('tag')
        status = request.POST.get('status')
        u = request.POST.get('person')
        user = User.objects.get(username=u)
        workplace = user.userprofile.primary_workplace
        li = []
        c1 = request.POST.get('category1')
        if c1:
            li.append(c1)
        c2 = request.POST.get('category2')
        if c2:
            li.append(c2)
        c3 = request.POST.get('category3')
        if c3:
            li.append(c3)
        index = request.POST.get('i')
        categories = Category.objects.filter(pk__in=li)
        image0 = request.FILES.get('image0', None)
        p = {}
        if len(pro) > 3:
            product = pro
            p = Products.objects.create(
                product=product, producer=workplace, description=description, user=user, cost=cost)
            p.set_tags(tags)
        if image0:
            i = Images()
            x = i.upload_image(image=image0, user=user)
            p.image = x
            p.save()

        for c in categories:
            Product_Categories.objects.create(
                product=p, category=c, level=c.level)

        return redirect('/internal/add_product')
    else:
        p = Products.objects.last()

        c1_all = Category.objects.filter(level=1)

        return render(request, 'activities/p/add_product.html', {'c1_all': c1_all, 'p': p})


@login_required
def int_product(request, slug):
    c1_all = Category.objects.filter(level=1)
    product = Products.objects.get(slug=slug)
    members = UserProfile.objects.filter(
        primary_workplace=product.user.userprofile.primary_workplace.pk)
    tagss = product.tags.all()
    prod_img_form = SetLogoForm()
    categories = product.categories.all()
    return render(request, 'activities/p/product.html', locals())


@login_required
def int_change_image(request, id):
    form = SetLogoForm(request.POST, request.FILES)
    p = Products.objects.get(id=id)
    user = p.user
    if request.method == 'POST':
        image = request.FILES.get('image')
        i = Images.objects.create(
            image=image, user=user, image_thumbnail=image)
        p.image = i
        p.save()
        return redirect('/internal/products/' + p.slug)
    else:
        return redirect('/products/' + p.slug)


@login_required
def int_edit_desc(request, id):
    p = Products.objects.get(id=id)
    if request.method == 'POST':
        desc = request.POST.get('description')
        p.description = desc
        p.save()
        return redirect('/internal/products/' + p.slug)
    else:
        return redirect('/products/' + p.slug)


@login_required
def set_int_details(request, id):
    p = Products.objects.get(id=id)
    user = p.user
    if request.method == 'POST':
        desc = request.POST.get('desc')
        cost = request.POST.get('cost')
        tags = request.POST.get('prod_tag')
        p.description = desc
        p.cost = cost
        if tags:
            p.set_tags(tags)
        p.save()
        return HttpResponse()
    else:
        return redirect('/products/' + id)


@login_required
def int_edit_category(request, id):
    p = Products.objects.get(id=id)
    if request.method == 'POST':
        li = []
        c1 = request.POST.get('category1')
        if c1:
            li.append(c1)
        c2 = request.POST.get('category2')
        if c2:
            li.append(c2)
        c3 = request.POST.get('category3')
        if c3:
            li.append(c3)
        categories = Category.objects.filter(pk__in=li)
        q = Product_Categories.objects.filter(product=p)
        if q:
            q.delete()
        for c in categories:

            Product_Categories.objects.create(
                product=p, category=c, level=c.level)
        return HttpResponse()
    else:
        return redirect('/internal/products/' + id)


def home(request):
    pass


def all_products(request):
    lvl = 1
    q = q1 = q2 = None
    if 'q' in request.GET:
        q = request.GET.get('q')
        q = Category.objects.get(id=q)
        curr_cat = q
        lvl = 2
        p = Products.objects.filter(categories=curr_cat).order_by('-date')
        if 'q1' in request.GET:
            q1 = request.GET.get('q1')
            q1 = Category.objects.get(id=q1)
            curr_cat = q1
            lvl = 3
            p = Products.objects.filter(categories=curr_cat).order_by('-date')
            if len(p) < 3:
                # curr_cat = curr_cat.get_parent_cat()[0]
                related = curr_cat.related_categories()
                for cat in related:
                    p1 = Products.objects.filter(categories=cat)
                    p = p | p1

            if 'q2' in request.GET:
                q2 = request.GET.get('q2')
                q2 = Category.objects.get(id=q2)
                curr_cat = q2
                lvl = 4
                p = Products.objects.filter(
                    categories=curr_cat).order_by('-date')
                if len(p) < 3:
                    related = curr_cat.related_categories()
                    for cat in related:
                        p1 = Products.objects.filter(categories=cat)
                        p = p | p1
        if lvl > 3:
            c1_all = c1_some = None
        else:
            c1_all = curr_cat.get_sub()
            c1_some = c1_all[:6]
    else:
        p = Products.objects.all().order_by('-date')
        c1_all = Category.objects.filter(level=1)
        c1_some = c1_all[:6]
    paginator = Paginator(p, 20)
    page = request.GET.get('page')
    try:
        result_list = paginator.page(page)
    except PageNotAnInteger:
            # If page is not an integer, deliver first page.
        result_list = paginator.page(1)
    except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of
                # results.
        return
        # result_list = paginator.page(paginator.num_pages)
    if page:
        return render(request, 'marketplace/20_products.html', {'result_list': result_list})
    else:
        return render(request, 'marketplace/marketplace.html',
                      {'result_list': result_list, 'c1_all': c1_all,
                       'c1_some': c1_some, 'lvl': lvl, 'q': q, 'q1': q1,
                       'q2': q2, })


def all_products_old(request):
    tags = []
    tags2 = []
    tags3 = []
    n = None
    m = None
    li1 = [590, 591, 581, 582, 586, 587, 243, 218, 621, 512]
    tags = Tags.objects.filter(pk__in=li1)
    i = 0
    for t in tags:
        p = Products.sell.filter(tags=t, target_segment__contains='C')
        t2 = Tags.objects.filter(products__in=p).distinct().exclude(id__in=li1)
        tags2.append(t2)
    if 'q' in request.GET:
        querystring = request.GET.get('q')
        if querystring == 'A':
            p = Products.sell.filter(target_segment__contains='A')
        if querystring == 'B':
            if 't' in request.GET:
                i = request.GET.get('t')
                t = Tags.objects.get(id=i)
                n = i
                p = Products.sell.filter(tags=t)
                tags3 = Tags.objects.filter(
                    products__in=p).distinct().exclude(id__in=li1)
            else:
                p = Products.sell.filter(target_segment__contains='B')
        if querystring == 'C':
            li1 = [590, 591, 581, 582, 586, 587, 243, 218, 621, 512]
            tags = Tags.objects.filter(pk__in=li1)
            if 't' in request.GET:
                i = request.GET.get('t')
                t = Tags.objects.get(id=i)
                n = i
                p = Products.sell.filter(tags=t)
                tags3 = Tags.objects.filter(
                    products__in=p).distinct().exclude(id__in=li1)
                if 'q3' in request.GET:
                    j = request.GET.get('q3')
                    t1 = Tags.objects.filter(id__in=[j])
                    m = j
                    p = Products.sell.filter(
                        tags=t1, target_segment__contains='C')
            else:
                p = Products.sell.filter(tags__in=tags).distinct()
        if querystring == 'O':
            p = Products.sell.filter(target_segment__contains='O')
        if querystring == 'N':
            p = Products.objects.all().order_by('-modified')

    else:
        if request.user.is_authenticated():
            if request.user.userprofile.primary_workplace:
                a = request.user.userprofile.workplace_type
            else:
                a = None
        else:
            a = None
        if a:
            p = Products.sell.filter(target_segment__contains=a)
        else:
            p = Products.sell.all()

    paginator = Paginator(p, 20)
    page = request.GET.get('page')
    try:
        result_list = paginator.page(page)
    except PageNotAnInteger:
            # If page is not an integer, deliver first page.
        result_list = paginator.page(1)
    except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of
                # results.
        return
        # result_list = paginator.page(paginator.num_pages)
    if page:
        return render(request, 'marketplace/20_products.html', {'result_list': result_list, 'tags': tags,
                                                                'tags2': tags2, 'n': n, 'm': m})
    else:
        return render(request, 'marketplace/marketplace.html', {'result_list': result_list,
                                                                'tags': tags, 'tags2': tags2, 'n': n, 'm': m})


@login_required
# @user_passes_test(lambda u: u.userprofile.workplace_type != 'N', login_url='/set')
def add_product(request):
    # return redirect('/products/edit_add/new')
    c1_all = Category.objects.filter(level=1)
    user = request.user
    workplace = request.user.userprofile.primary_workplace
    if request.method == 'POST':
        # email of the uploader, only for the first product
        product_email = request.POST.get('u_email')
        # phone of the uploader, only for the first product
        product_phone = request.POST.get('u_phone')
        up = user.userprofile
        up.set_product_contacts(
            product_email=product_email, product_phone=product_phone)
        pro = request.POST.get('product')
        description = request.POST.get('description')
        cost = request.POST.get('cost')
        tags = request.POST.get('tag')
        status = request.POST.get('status')

        up.points += 5
        up.save()
        li = []
        c1 = request.POST.get('category1')
        if c1:
            li.append(c1)
        c2 = request.POST.get('category2')
        if c2:
            li.append(c2)
        c3 = request.POST.get('category3')
        if c3:
            li.append(c3)
        index = request.POST.get('i')
        categories = Category.objects.filter(pk__in=li)
        workplace = request.user.userprofile.primary_workplace
        image0 = request.FILES.get('image0', None)
        p = {}
        if len(pro) > 3:
            product = pro
            p = Products.objects.create(
                product=product, producer=workplace, description=description, user=user, cost=cost)
        if image0:
            i = Images()
            x = i.upload_image(image=image0, user=user)
            p.image = x
            p.save()

        for c in categories:
            Product_Categories.objects.create(
                product=p, category=c, level=c.level)
        todaydate = date.today()
        startdate = todaydate + timedelta(days=1)
        enddate = startdate - timedelta(days=1)
        node = '''We have just listed a few products on behalf of <a href="/workplace/{0}">{1}</a>. Have a look at our profile for more details.'''.format(
            workplace.slug, workplace)
        pp = Products.objects.filter(
            date__range=[enddate, startdate], user=user)
        if len(pp) < 2:
            n = Node.objects.create(
                post=node, user=user, category='D', w_type=workplace.workplace_type)
            if image0:
                n.images = [x]
        response = {}
        response['alert'] = render_to_string(
            'products/add_prod_alert.html', {'p': p})
        return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        p = Products.objects.filter(producer=workplace).last()
        if user.userprofile.product_email:
            no_prod_con = False
        else:
            no_prod_con = True

        c = {}
        if p:
            c = Product_Categories.objects.filter(
                product=p.id).order_by('level')
        c1_all = Category.objects.filter(level=1)
        c1_1 = itemgetter(0, 1, 2)(c1_all)
        c1_2 = itemgetter(3, 4, 13)(c1_all)
        c1_3 = itemgetter(2, 5)(c1_all)
        c1_4 = itemgetter(6, 7, 12, 13)(c1_all)
        c1_5 = itemgetter(9, 8, 6)(c1_all)
        c1_6 = itemgetter(10, 11)(c1_all)
        # c1_7 = itemgetter(6, 7, 12)(c1_all)
        c1_8 = itemgetter(13, 14, 15)(c1_all)

        return render(request, 'products/add_product.html', {'c1_all': c1_all, 'c1_1': c1_1, 'c1_2': c1_2,
                                                             'c1_3': c1_3, 'c1_4': c1_4, 'c1_5': c1_5, 'c1_6': c1_6,
                                                             'c1_8': c1_8, 'p': p, 'c': c, 'first_time': False, })


def initial_category(request):
    pass


def c_r(request):
    id = request.GET.get('id')
    pro = Products.objects.get(id=id)
    wp = pro.producer
    # ppp = Product_Categories.objects.filter(product__producer=wp)
    # if len(ppp)>0:
    #
    #     pc = ppp.reverse()[0]
    #     p = pc.product
    #     q = Product_Categories.objects.filter(product=p)
    #
    #     for t in q:
    #         Product_Categories.objects.create(product=pro, category=t.category, level=t.level)
    #     return redirect('/internal/activity/?q=p')
    # else:
    #     pass
    pp = Product_Categories.objects.last()
    p = pp.product
    q = Product_Categories.objects.filter(product=p)
    for t in q:
        Product_Categories.objects.create(
            product=pro, category=t.category, level=t.level)
    return redirect('/internal/activity/?q=p')


def int_category(request, slug):
    category = Category.objects.get(slug=slug)
    # products = Products.objects.filter()
    return render(request, 'activities/category.html', locals())


def all_category(request):
    cats = Category.objects.all()
    # return render(request, 'activities/category.html', locals())
    paginator = Paginator(cats, 20)
    page = request.GET.get('page')
    try:
        categories = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        categories = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        categories = paginator.page(paginator.num_pages)
    # return render_to_response('tags/list1.html', {"tags": tags})
    if page:
        return render(request, 'products/20_categories.html', {'categories': categories})
    else:
        return render(request, 'products/all_categories.html', {'categories': categories})


def category(request, slug):        # Products
    category = Category.objects.get(slug=slug)
    products = Products.objects.filter(categories=category)
    content_url = "products/snip_cat.html"
    content_head_url = "products/snip_category_head.html"
    if request.is_ajax():
        return render(request, content_url, locals())
    else:
        meta = True
        return render(request, 'products/category.html', locals())


def category_prod(request, slug):        # Products
    category = Category.objects.get(slug=slug)
    products = Products.objects.filter(categories=category)
    # if len(products) < 3:
    related_categories = category.related_categories()[:5]
    products2 = Products.objects.filter(id__lte=0)
    for c in related_categories:
        pros = Products.objects.filter(categories=c)
        products2 = products2 | pros
    content_url = "products/snip_products.html"
    content_head_url = "products/snip_products_head.html"
    if len(products) < 5:
        products = products | products2
    paginator = Paginator(products, 20)
    page = request.GET.get('page')
    try:
        result_list = paginator.page(page)
    except PageNotAnInteger:
            # If page is not an integer, deliver first page.
        result_list = paginator.page(1)
    except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of
                # results.
        return
        # result_list = paginator.page(paginator.num_pages)
    if request.is_ajax():
        if page:
            return render(request, {'products': result_list})
        else:
            return render(request, content_url, {'content_head_url': content_head_url,
                                                 'products': result_list, 'category': category})
        # return render(request, 'products/category.html', locals())
        # return render(request, content_url, locals())
    else:
        meta = True
        if page:
            return render(request, {'products': result_list})
        else:
            return render(request, 'products/category.html', {'content_head_url': content_head_url, 'meta': meta,
                                                              'content_url': content_url, 'products': result_list,
                                                              'category': category})
        # return render(request, 'products/category.html', locals())


def category_wp(request, slug):        # Workplace
    category = Category.objects.get(slug=slug)
    products = Products.objects.filter(
        categories=category).select_related('producer')
    workplaces = []
    for p in products:
        if p.producer not in workplaces:
            workplaces.append(p.producer)
        else:
            pass
    content_url = "products/snip_workplace.html"
    content_head_url = "products/snip_companies_head.html"
    if request.is_ajax():
        return render(request, content_url, locals())
    else:
        meta = True
        return render(request, 'products/category.html', locals())


def category_update(request):
    category = Category.objects.all()
    for c in category:
        name = c.name
        subs = c.get_sub()
        parents = c.get_parent_cat()
        text = ''
        if subs:
            for s in subs:
                n = s.name + ', '
                text += n
        if parents:
            for s in parents:
                n = s.name + ','
                text += n

        c.meta_des = text[:150]
        c.save()
    return redirect('/')


from io import StringIO, BytesIO

@login_required
# @user_passes_test(lambda u: u.userprofile.workplace_type != 'N', login_url='/set')
def edit_add_product(request, id):
    user = request.user
    wp = user.userprofile.primary_workplace
    workplace = wp
    response = {}
    c = {}
    pl = Products.objects.filter(producer=workplace).last()
    if pl:
        c = Product_Categories.objects.filter(product=pl.id).order_by('level')
        dd = pl.delivery_details
        dc = pl.delivery_charges
        minimum = pl.minimum
    else:
        dd = ''
        dc = ''
        minimum = ''
    c1_all = Category.objects.filter(level=1)
    c1_1 = itemgetter(0, 1, 2)(c1_all)
    c1_2 = itemgetter(3, 4, 13)(c1_all)
    c1_3 = itemgetter(2, 5)(c1_all)
    c1_4 = itemgetter(6, 7, 12, 13)(c1_all)
    c1_5 = itemgetter(9, 8, 6)(c1_all)
    c1_6 = itemgetter(10, 11)(c1_all)
    # c1_7 = itemgetter(6, 7, 12)(c1_all)
    c1_8 = itemgetter(13, 14, 15)(c1_all)

    if id == 'new':
        return redirect('/products/add_product/')
        # dictionary = {}
        # ps = Products()
        # p = None
        # if request.method == 'POST':
        #     if request.POST.get('product'):
        #         p = Products.objects.create(product=request.POST['product'], user=user, producer=wp,
        #                                     delivery_details=dd, delivery_charges=dc, minimum=minimum)
        #         if c:
        #             p.set_prod_category(c)
        #         up = user.userprofile
        #         up.points += 5
        #         up.save()
        #         response['p_id'] = p.id
        #     image1 = request.FILES.get('photo', None)
        #     if image1:
        #         image = StringIO()
        #         image1.save(image, image1.name.split('.')[-1])
        #         # i = Images()
        #         # x = i.upload_image(image=image1, user=user)
        #         # p.image = x
        #         # p.save()
        #     response['p_id'] = p.id
        #     # else:
        #     #     p_t = Products()
        #     #
        #     # return HttpResponse(json.dumps(response),
        #     # content_type="application/json")
        # if user.userprofile.product_email:
        #     no_prod_con = False
        # else:
        #     no_prod_con = True
        # return render(request, 'products/edit.html', {'c1_all': c1_all, 'c1_1': c1_1, 'c1_2': c1_2,
        #                                               'c1_3': c1_3, 'c1_4': c1_4, 'c1_5': c1_5, 'c1_6': c1_6,
        #                                               'c1_8': c1_8, 'p': p, 'c': c, 'first_time': True,
        #                                               'no_prod_con': no_prod_con, 'delivery_details': dd,
        #                                               'delivery_charges': dc, 'minimum': minimum})
    else:
        p = Products.objects.get(id=id)
        dictionary = {}
        direct = [f.name for f in Products._meta.get_fields()]
        if request.method == 'POST' and user.userprofile.primary_workplace == p.producer:
            for key in request.POST:
                if key in direct:
                    try:
                        dictionary[key] = request.POST[key]
                    except:
                        tb = traceback.format_exc()
                else:
                    li = []
                    li.append(request.POST.get('category1'))
                    li.append(request.POST.get('category2'))
                    li.append(request.POST.get('category3'))
                    p.set_categories(li)
            for key in dictionary:
                setattr(p, key, dictionary[key])
            p.save()
            image1 = request.FILES.get('photo', None)
            if image1:
                i = Images()
                x = i.upload_image(image=image1, user=user)
                p.image = x
                p.save()
            response['p_id'] = p.id
            return HttpResponse(json.dumps(response), content_type="application/json")
        else:
            c = Product_Categories.objects.filter(
                product=p.id).order_by('level')
            dictionary = {'c1_all': c1_all, 'c1_1': c1_1, 'c1_2': c1_2, 'c1_3': c1_3, 'c1_4': c1_4, 'c1_5': c1_5,
                          'c1_6': c1_6, 'c1_8': c1_8, 'product': p, 'c': c, 'first_time': True}
            return render(request, 'products/edit.html', dict(list(p.__dict__.items()) + list(dictionary.items())))
