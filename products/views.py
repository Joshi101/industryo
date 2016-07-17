from django.shortcuts import render, redirect, HttpResponse
from django.template.loader import render_to_string
from nodes.forms import SetLogoForm
from products.models import *
from userprofile.models import UserProfile
from django.contrib.auth.models import User
from tags.models import Tags
import json
from nodes.models import Images
from django.contrib.auth.decorators import login_required, user_passes_test
from activities.models import Enquiry
from datetime import datetime, timedelta, time, date
from django.core.mail import EmailMultiAlternatives
from django.core.mail import get_connection, send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from nodes.models import Node
from itertools import chain
from operator import itemgetter
from chat.views import create_message_enquiry
from home.tasks import execute_view


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
        r_html['info_field_value'] = render_to_string('snippets/tag_short.html', {'tags': new_interest})
        response['html'] = r_html
        response['elements'] = r_elements
        response['prepend'] = False
        return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        return redirect('/user/'+request.user.username)

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
        # for key in request.POST:
        #     value = request.POST[key]
        #     # for key in request.POST.iteritems():
        #     print(key)
        #     print(value)
        id = request.POST.get('new_category_1')
        c2 = request.POST.get('new_category_2')
        c3 = request.POST.get('new_category_3')
        if not c3:
            id = request.POST.get('new_category_1')
            c = Category.objects.get(id=id)
            a, created = Category.objects.get_or_create(name=c2, level=2)
            c.sub_cat.add(a)
        elif c3:
            id = request.POST.get('new_category_2')
            c = Category.objects.get(id=id)
            a, created = Category.objects.get_or_create(name=c3, level=3)
            c.sub_cat.add(a)
        response = {}
        response['id'] = a.id
        response['name'] = a.name
        return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        print("FTFTFTF")

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
                Product_Categories.objects.create(product=p, category=c, level=c.level)
            return HttpResponse()
    else:
        return redirect('/products/' + id)


def product(request, slug):
    c1_all = Category.objects.filter(level=1)
    product = Products.objects.get(slug=slug)
    producer = product.producer
    members = UserProfile.objects.filter(primary_workplace=product.user.userprofile.primary_workplace.pk)
    tagss = product.tags.all()
    prod_img_form = SetLogoForm()
    # categories = Product_Categories.objects.filter(product_id=product.id).order_by('level')
    categories = product.categories.all()
    all = Products.objects.filter(producer=producer)
    all_list = list(all)
    c = all_list.index(product)
    if not len(all_list) == c+1:
        next = all_list[c+1]
    if not c == 0:
        previous = all_list[c-1]
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
            return redirect('/products/'+p.slug)
    else:
        return redirect('/products/'+p.slug)


@login_required
def change_image(request, id):
    form = SetLogoForm(request.POST, request.FILES)
    p = Products.objects.get(id=id)
    user = request.user
    workplace = user.userprofile.primary_workplace
    if request.method == 'POST':
        if p.producer == workplace:
            image = request.FILES.get('image')
            i = Images.objects.create(image=image, user=user, image_thumbnail=image)
            p.image = i
            p.save()
            return redirect('/products/'+p.slug)
    else:
        return redirect('/products/'+p.slug)


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


def enquire(request):
    yesterday = date.today() - timedelta(days=1)
    if request.method == 'POST':
        if request.user.is_authenticated():
            p = request.POST.get('pid')
            w = request.POST.get('wid')
            user = request.user
            message = request.POST.get('message')
            phone = request.POST.get('phone')
            e = Enquiry.objects.filter(user=user, date__gt=yesterday)
            if p:
                prod = Products.objects.get(id=p)
                if e.count() < 5:
                    e = Enquiry.objects.create(product=prod, user=user, message=message, phone_no=phone)
                    users = e.product.producer.get_members()
                    create_message_enquiry(message, user, users)
                    user.userprofile.notify_inquired(e, users)
                    # send_enq_mail(e)
                    execute_view('check_no_inquiry', e.id, schedule=timedelta(seconds=30))
                return redirect('/products/'+prod.slug)

            if w:
                workplace = Workplace.objects.get(id=w)
                if e.count() < 5:
                    # Checking if the same person has created more than 5 inquiries that day
                    e = Enquiry.objects.create(workplace=workplace, user=user, message=message, phone_no=phone)
                    users = workplace.get_members()
                    create_message_enquiry(message, user, users)
                    user.userprofile.notify_inquired(e, users)
                    execute_view('check_no_inquiry', e.id, schedule=timedelta(seconds=30))
                return redirect('/workplace/'+workplace.slug)
        else:
            email = request.POST.get('email')
            name = request.POST.get('name')
            company = request.POST.get('company')
            p = request.POST.get('pid')
            w = request.POST.get('wid')
            message = request.POST.get('message')
            phone = request.POST.get('phone')
            e = Enquiry.objects.filter(email=email, date__gt=yesterday)

            if p:
                prod = Products.objects.get(id=p)
                if e.count() < 5:
                    # Checking if the same person has created more than 5 inquiries that day
                    e = Enquiry.objects.create(product=prod, name=name, company=company, email=email, message=message, phone_no=phone)
                    up = prod.user.userprofile
                    # up.notify_inquired(e)
                    # send_enq_mail(e)
                    execute_view('check_no_inquiry', e.id, schedule=timedelta(seconds=30))
                return redirect('/products/'+prod.slug)
            if w:
                workplace = Workplace.objects.get(id=w)
                if e.count() < 5:
                    e = Enquiry.objects.create(workplace=workplace, name=name, company=company, message=message, phone_no=phone)
                    # up.notify_inquired(e)
                    execute_view('check_no_inquiry', e.id, schedule=timedelta(seconds=30))
                return redirect('/workplace/'+workplace.slug)




@login_required
def enquiry_all(request):
    user = request.user
    company = user.userprofile.primary_workplace

    enquiries = Enquiry.objects.filter(product__producer=company)
    e = Enquiry.objects.filter(workplace=company)
    enquiries_sent = Enquiry.objects.filter(user=user)

    return render(request, 'enquiry/enquiry.html', {
        'enquiries': enquiries, 'enquiries_sent': enquiries_sent, 'e':e,
        })


def enquiry(request, id):
    iid = int(id)
    user = request.user
    # company = user.userprofile.primary_workplace
    # enquiries = Enquiry.objects.filter(product__producer=company)
    enquiry = Enquiry.objects.get(id=iid)
    enquiry.seen = True
    enquiry.save()
    if enquiry.workplace:
        return render(request, 'enquiry/enquiry_details_wp.html', {'enquiry': enquiry})
    else:
        return render(request, 'enquiry/enquiry_details.html', {'enquiry': enquiry})


def enquiry_sent(request, id):
    iid = int(id)
    user = request.user
    # company = user.userprofile.primary_workplace
    # enquiries = Enquiry.objects.filter(product__producer=company)
    enquiry = Enquiry.objects.get(id=iid)
    enquiry.seen = True
    enquiry.save()
    if enquiry.workplace:
        return render(request, 'enquiry/enquiry_details_wp_sent.html', {'enquiry': enquiry})
    else:
        return render(request, 'enquiry/enquiry_details_sent.html', {'enquiry': enquiry})


def send_enq_mail(e):
    user = e.product.user
    user_email = user.email
    product = e.product
    name = user.userprofile
    my_host = 'smtp.zoho.com'
    my_port = 587
    my_username = 'admin@corelogs.com'
    my_password = 'AD@zoho.09'
    my_use_tls = True
    connection = get_connection(host=my_host,
                                port=my_port,
                                username=my_username,
                                password=my_password,
                                use_tls=my_use_tls)
    template = u'''<div id=":kc" class="a3s" style="overflow: hidden;"><div dir="ltr"><div style="color:rgb(0,0,0);font-family:HelveticaNeue,'Helvetica Neue',Helvetica,Arial,'Lucida Grande',sans-serif;font-size:16px">Hi {0},</div><div style="color:rgb(0,0,0);font-family:HelveticaNeue,'Helvetica Neue',Helvetica,Arial,'Lucida Grande',sans-serif;font-size:16px"><br></div><div style="color:rgb(0,0,0);font-family:HelveticaNeue,'Helvetica Neue',Helvetica,Arial,'Lucida Grande',sans-serif;font-size:16px">You have received an inquiry about a product&nbsp;<a href="http://www.corelogs.com/products/{1}" target="_blank">{2}</a>&nbsp;that you have listed on your workplace profile&nbsp;<a href="http://www.corelogs.com/workplace/{3}" target="_blank">{4}</a>.</div><div style="color:rgb(0,0,0);font-family:HelveticaNeue,'Helvetica Neue',Helvetica,Arial,'Lucida Grande',sans-serif;font-size:16px"><br></div><div style="color:rgb(0,0,0);font-family:HelveticaNeue,'Helvetica Neue',Helvetica,Arial,'Lucida Grande',sans-serif;font-size:16px">You can see the details of the inquiry and the person who is interested in buying your product in this link.</div><div dir="ltr" style="color:rgb(0,0,0);font-family:HelveticaNeue,'Helvetica Neue',Helvetica,Arial,'Lucida Grande',sans-serif;font-size:16px">Enquiry Details:&nbsp;<a href="http://www.corelogs.com/products/enquiry_all" target="_blank">www.corelogs.com/<wbr>products/enquiry_all</a>.&nbsp;</div><div dir="ltr" style="color:rgb(0,0,0);font-family:HelveticaNeue,'Helvetica Neue',Helvetica,Arial,'Lucida Grande',sans-serif;font-size:16px"><br></div><div style="color:rgb(0,0,0);font-family:HelveticaNeue,'Helvetica Neue',Helvetica,Arial,'Lucida Grande',sans-serif;font-size:16px">We wish you a successful sale. Just keep us updated with your products. Add products easily in your workplace profile and find a great market ready to purchase.</div><div style="color:rgb(0,0,0);font-family:HelveticaNeue,'Helvetica Neue',Helvetica,Arial,'Lucida Grande',sans-serif;font-size:16px"><br></div><div><div><div dir="ltr"><div><b>--<br>Admin</b></div><div><a href="http://www.corelogs.com" target="_blank"><b>CoreLogs</b></a><div class="yj6qo"></div><div class="adL"><br><br></div></div></div></div></div><div class="adL">
</div></div><div class="adL">
</div></div>
    '''

    html_content = template.format(name, product.slug, product, product.producer.slug, product.producer)
    subject, from_email, to = u'''[CoreLogs] Enquiry about {0}'''.format(product), 'admin@corelogs.com', user_email
    text_content = 'You have got an enquiry about a product. Visit www.corelogs.com'
    connection.open()
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to], connection=connection)
    msg.attach_alternative(html_content, "text/html")
    msg.send()
    connection.close()

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
            p = Products.objects.create(product=product, producer=workplace, description=description, user=user, cost=cost)
            p.set_tags(tags)
        if image0:
            i = Images()
            x = i.upload_image(image=image0, user=user)
            p.image = x
            p.save()

        for c in categories:
            Product_Categories.objects.create(product=p, category=c, level=c.level)

        return redirect('/internal/add_product')
    else:
        p = Products.objects.last()

        c1_all = Category.objects.filter(level=1)

        return render(request, 'activities/p/add_product.html', {'c1_all': c1_all, 'p': p})

@login_required
def int_product(request, slug):
    c1_all = Category.objects.filter(level=1)
    product = Products.objects.get(slug=slug)
    members = UserProfile.objects.filter(primary_workplace=product.user.userprofile.primary_workplace.pk)
    tagss = product.tags.all()
    prod_img_form = SetLogoForm()
    categories = product.categories.all()
    # category1 = product.get_category1()
    # category2 = product.get_category2()
    # category3 = product.get_category3()
    return render(request, 'activities/p/product.html', locals())

@login_required
def int_change_image(request, id):
    form = SetLogoForm(request.POST, request.FILES)
    p = Products.objects.get(id=id)
    user = p.user
    # workplace = user.userprofile.primary_workplace
    if request.method == 'POST':
        image = request.FILES.get('image')
        i = Images.objects.create(image=image, user=user, image_thumbnail=image)
        p.image = i
        p.save()
        return redirect('/internal/products/'+p.slug)
    else:
        return redirect('/products/'+p.slug)

@login_required
def int_edit_desc(request, id):
    p = Products.objects.get(id=id)
    if request.method == 'POST':
        desc = request.POST.get('description')
        p.description = desc
        p.save()
        return redirect('/internal/products/'+p.slug)
    else:
        return redirect('/products/'+p.slug)

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

                Product_Categories.objects.create(product=p, category=c, level=c.level)
            return HttpResponse()
    else:
        return redirect('/internal/products/' + id)


def home(request):
    tags = []
    tags2 = []
    if 'q' in request.GET:
        querystring = request.GET.get('q')
        if querystring == 'A':
            li1 = [590, 591, 581, 582, 586, 587, 243, 218, 621, 512]
            tags = Tags.objects.filter(pk__in=li1)
            for t in tags:
                p = Products.sell.filter(tags=t, target_segment__contains='C')
                t2 = Tags.objects.filter(products__in=p).distinct().exclude(id__in=li1)
                tags2.append(t2)
        elif querystring == 'B':
            return redirect('/marketplace?q=B&t=701')
            # li1 = [701]
            # tags = Tags.objects.filter(pk__in=li1)
            # for t in tags:
            #     p = Products.sell.filter(tags=t, target_segment__contains='C')
            #     t2 = Tags.objects.filter(products__in=p).distinct().exclude(id__in=li1)
            #     tags2.append(t2)
        elif querystring == 'C':
            return redirect('/marketplace?q=B')
            # li1 = []
            # tags = Tags.objects.filter(pk__in=li1)
            # for t in tags:
            #     p = Products.sell.filter(tags=t, target_segment__contains='C')
            #     t2 = Tags.objects.filter(products__in=p).distinct().exclude(id__in=li1)
            #     tags2.append(t2)
        elif querystring == 'D':
            return redirect('/marketplace?q=B')

        elif querystring == 'E':
            return redirect('/marketplace?q=B&t=35')

        elif querystring == 'N':
            return redirect('/marketplace?q=N')

        return render(request, 'marketplace/cover.html', {'tags': tags, 'tags2': tags2})
    else:
        li1 = [590, 591, 581, 582, 586, 587, 243, 218, 621, 512]
        tags = Tags.objects.filter(pk__in=li1)
        for t in tags:
            p = Products.sell.filter(tags=t, target_segment__contains='C')
            t2 = Tags.objects.filter(products__in=p).distinct().exclude(id__in=li1)
            tags2.append(t2)

        return render(request, 'marketplace/cover_pre.html', {'tags': tags, 'tags2': tags2})


def all_products(request):
    lvl = 1
    q = q1 = q2 = None
    if 'q' in request.GET:
        p = Products.objects.all().order_by('-date')
        q = request.GET.get('q')
        q = Category.objects.filter(id=q).get()
        curr_cat = q
        lvl = 2
        if 'q1' in request.GET:
            q1 = request.GET.get('q1')
            q1 = Category.objects.filter(id=q1).get()
            curr_cat = q1
            lvl = 3
            p = Products.objects.filter(categories=curr_cat).order_by('-date')
            if 'q2' in request.GET:
                q2 = request.GET.get('q2')
                q2 = Category.objects.filter(id=q2).get()
                curr_cat = q2
                lvl = 4
                pp = Products.objects.filter(categories=curr_cat).order_by('-date')
                if len(pp) > 0:
                    p = pp
                else:
                    curr_cat = q1
                    p = Products.objects.filter(categories=curr_cat).order_by('-date')
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
                # If page is out of range (e.g. 9999), deliver last page of results.
        return
        # result_list = paginator.page(paginator.num_pages)
    if page:
        return render(request, 'marketplace/20_products.html', {'result_list': result_list})
    else:
        return render(request, 'marketplace/marketplace.html', {'result_list': result_list, 'c1_all': c1_all,
                                                                'c1_some': c1_some, 'lvl': lvl, 'q': q, 'q1': q1,
                                                                'q2': q2,})


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
                tags3 = Tags.objects.filter(products__in=p).distinct().exclude(id__in=li1)
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
                tags3 = Tags.objects.filter(products__in=p).distinct().exclude(id__in=li1)
                if 'q3' in request.GET:
                    j = request.GET.get('q3')
                    t1 = Tags.objects.filter(id__in=[j])
                    m = j
                    p = Products.sell.filter(tags=t1, target_segment__contains='C')
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
                # If page is out of range (e.g. 9999), deliver last page of results.
        return
        # result_list = paginator.page(paginator.num_pages)
    if page:
        return render(request, 'marketplace/20_products.html', {'result_list': result_list, 'tags':tags, 'tags2':tags2, 'n':n, 'm':m})
    else:
        return render(request, 'marketplace/marketplace.html', {'result_list': result_list, 'c1_all':c1_all, 'tags':tags, 'tags2':tags2, 'n':n, 'm':m})

@login_required
# @user_passes_test(lambda u: u.userprofile.workplace_type != 'N', login_url='/set')
def add_product(request):
    return redirect('/products/edit_add/new')
    # c1_all = Category.objects.filter(level=1)
    # user = request.user
    # workplace = request.user.userprofile.primary_workplace
    # if request.method == 'POST':
    #     product_email = request.POST.get('u_email')     # email of the uploader, only for the first product
    #     product_phone = request.POST.get('u_phone')     # phone of the uploader, only for the first product
    #     up = user.userprofile
    #     up.set_product_contacts(product_email=product_email, product_phone=product_phone)
    #     pro = request.POST.get('product')
    #     description = request.POST.get('description')
    #     cost = request.POST.get('cost')
    #     tags = request.POST.get('tag')
    #     status = request.POST.get('status')
    #
    #     up.points += 5
    #     up.save()
    #     li = []
    #     c1 = request.POST.get('category1')
    #     if c1:
    #         li.append(c1)
    #     c2 = request.POST.get('category2')
    #     if c2:
    #         li.append(c2)
    #     c3 = request.POST.get('category3')
    #     if c3:
    #         li.append(c3)
    #     index = request.POST.get('i')
    #     categories = Category.objects.filter(pk__in=li)
    #     workplace = request.user.userprofile.primary_workplace
    #     image0 = request.FILES.get('image0', None)
    #     p = {}
    #     if len(pro) > 3:
    #         product = pro
    #         p = Products.objects.create(product=product, producer=workplace, description=description, user=user, cost=cost)
    #     if image0:
    #         i = Images()
    #         x = i.upload_image(image=image0, user=user)
    #         p.image = x
    #         p.save()
    #
    #     for c in categories:
    #         Product_Categories.objects.create(product=p, category=c, level=c.level)
    #     todaydate = date.today()
    #     startdate = todaydate + timedelta(days=1)
    #     enddate = startdate - timedelta(days=1)
    #     node = '''We have just listed a few products on behalf of <a href="/workplace/{0}">{1}</a>. Have a look at our profile for more details.'''.format(workplace.slug, workplace)
    #     pp = Products.objects.filter(date__range=[enddate, startdate], user=user)
    #     if len(pp) < 2:
    #         n = Node.objects.create(post=node, user=user, category='D', w_type=workplace.workplace_type)
    #         if image0:
    #             n.images = [x]
    #     response = {}
    #     response['alert'] = render_to_string('products/add_prod_alert.html', {'p': p})
    #     return HttpResponse(json.dumps(response), content_type="application/json")
    # else:
    #     p = Products.objects.filter(producer=workplace).last()
    #     if user.userprofile.product_email:
    #         no_prod_con = False
    #     else:
    #         no_prod_con = True
    #
    #     c = {}
    #     if p:
    #         c = Product_Categories.objects.filter(product=p.id).order_by('level')
    #     c1_all = Category.objects.filter(level=1)
    #     c1_1 = itemgetter(0, 1, 2)(c1_all)
    #     c1_2 = itemgetter(3, 4, 13)(c1_all)
    #     c1_3 = itemgetter(2, 5)(c1_all)
    #     c1_4 = itemgetter(6, 7, 12, 13)(c1_all)
    #     c1_5 = itemgetter(9, 8, 6)(c1_all)
    #     c1_6 = itemgetter(10, 11)(c1_all)
    #     # c1_7 = itemgetter(6, 7, 12)(c1_all)
    #     c1_8 = itemgetter(13, 14, 15)(c1_all)
    #
    #     return render(request, 'products/add_product.html', {'c1_all': c1_all, 'c1_1': c1_1, 'c1_2': c1_2,
    #                                                          'c1_3': c1_3, 'c1_4': c1_4, 'c1_5': c1_5, 'c1_6': c1_6,
    #                                                          'c1_8': c1_8, 'p': p, 'c': c, 'first_time': True,
    #                                                          'no_prod_con': no_prod_con})


def initial_category(request):
    li = ['SAE Teams & Related Items', 'Electronics & RC Items for enthusiasts', 'Products for Racing Enthusiasts', 'Automobile & Aerospace Parts', 'Mechanical Parts & Assemblies', 'Electrial & Electronics Products', 'Industry Supplies & Raw Materials', 'Industrial Machinery & Parts', 'Construction Materials & Equipments', 'Chemicals,  Dies, Paints', 'Agricultural & Agrotech products', 'Textiles & Clothings', 'Labs & Industry Equipments', 'Engineering & Industrial Consultancy Services', 'Internet & Software Based Services', 'Other Services']
    li2 = ['SAE Teams & Related Items', 'Safety Equipment', 'Racing Accessories', 'Suspension Parts', 'Powertrain Parts', 'Wheel Assembly', 'Rollcage, Pipes & Tubes', 'Brake Components', 'Steering System', 'Electricals & Electronics', 'Aesthetics', 'Electronics & RC Items for enthusiasts', 'RC Items', 'Arduino kits & Raspberry Pi', 'Electronics Components', 'DC Motors', 'Products for Racing Enthusiasts', 'Cars & Bike Accessories', 'Performance Boosters', 'Automobile & Aerospace Parts', 'Brake Components', 'Plastics & Polymer Components', 'Fasteners, Nuts Bolts, Rivets, Clamps', 'Engine Components', 'Chassis & Body Building', 'Gears, Gearboxes and Related Components', 'Elecrical & Electronics Items', 'Sheet Metal Components', 'Bearing, Bushes & Related Items', 'Joints, Shafts, Couplings', 'Fiber Parts', 'Jigs & Fixtures', 'Other OEM Parts', 'Mechanical Parts & Assemblies', 'Pumps & Turbines', 'Hydraulic Machines', 'Pneumatic Machines', 'Gears, Gearboxes and Related Components', 'Joints, Shafts, Couplings', 'Jigs & Fixtures', 'Bearing, Bushes & Related Items', 'Fasteners, Nuts Bolts, Rivets, Clamps', 'Boilers & Tanks', 'Motors & Generators & Parts', 'Electrial & Electronics Products', 'Motors & Generators & Parts', 'Pumps & Turbines', 'Electrical Fitting Items', 'Consumer Electronics Products', 'Electronics Products', 'Instruments', 'Actuators & Sensors', 'Industry Supplies & Raw Materials', 'Industrial Chemicals', 'Metallic Raw Materials', 'Non Metallic raw material', 'Machining Fluids', 'Packaging Materials', 'Measuring Equipments', 'Plastics & Rubbers', 'Welding Setup', 'Jigs & Fixtures', 'Pipes & Tubes', 'Industrial Machinery & Parts', 'Machine Tools', 'CNC Machines', 'Material Handling Equipments', 'Special Purpose Machines', 'Plastic Processing Machines', 'Jigs & Fixtures', 'Power Tools', 'Hand Tools', 'Construction Materials & Equipments', 'Steel Parts', 'Aluminium Parts', 'Cement & Bricks', 'Scaffoldings & Accessories', 'Consruction Machinery', 'Plumbing Items', 'Safety Items', 'Wood & Furniture', 'Coatings & Finishing', 'Interior Items', 'Chemicals,  Dies, Paints', 'Industrial Chemicals', 'Pigments', 'Paint', 'Dies', 'Food Chemical & Preservatives', 'Agricultural & Agrotech products', 'Agricultural Equipments', 'Agricultural Machinery', 'Insecticides & Pesticides', 'Edible Agricultural Products', 'Fertilizers & soil Additives', 'Seeds', 'Oils', 'Textiles & Clothings', 'Finished Clothes', 'Cloth raw material', 'Leather Products', 'Machinery', 'Labs & Industry Equipments', 'Measuring Equipments', 'Laboratory equipments', 'Material Handling Equipments & Parts', 'Welding Setup', 'Hand Tools', 'Power Tools', 'Engineering & Industrial Consultancy Services', 'Designing', 'Industrial Services', 'Environmental Planning', 'Simulation & Analysis Services', 'Planning & Implementation', 'Internet & Software Based Services', 'Web Designing Services', 'Software solutions', 'Online Marketing solutions', 'Other Services', 'Installation, Maintenance etc.', 'Transportation & Courier services', 'Training & Hiring Services', 'Online Marketing solutions', 'Household services', 'Construction Services', 'Repairing Services']
    li3 = ['Safety Equipment', 'Helmet', 'Driver Suit', 'Other Wearables', 'Gloves', 'Racing Accessories', 'Seats', 'Seat Belts & Harnesses', 'Driver Suit', 'Other Wearables', 'Fire Extinguishers', 'Suspension Parts', 'Dampers', 'Shock Absorbers', 'Knuckles & Hubs', 'Powertrain Parts', 'Engine Accessories', 'Exhaust', 'Spares', 'Engine', 'Gearbox', 'CVT', 'DC Motor', 'Wheel Assembly', 'Tubes & Tyres', 'Rims & Tyres', 'ATV Tyres', 'Formula Tyres', 'Knuckle & Hub', 'Rollcage, Pipes & Tubes', 'AISI 1018', 'AISI 4130 Chromoly', 'AISI 4340', 'Carbon Fiber', 'Pipes & Tubes', 'Alloy Steel', 'Brake Components', 'Calipers', 'Brake Lines', 'Master Cylinder', 'Brake Pedal & Assembly', 'Steering System', 'Steering Rack', 'Steering Wheels', 'Tie Rods', 'Electricals & Electronics', 'Switches', 'Lights', 'Transponders', 'Aesthetics', 'RC Items', 'RC Cars', 'RC Monster trucks', 'RC Helicopter & Plane', 'RC Ship', 'Quadcopters & Parts', 'Arduino kits & Raspberry Pi', 'Raspberry pi & spares', 'Arduino sheilds', 'Electronics Components', 'Resistors & Capacitors', 'Wireless', 'ICs', 'LCD Screens', 'Sensors', 'DC Motors', 'Stepper Motors', 'Servo motors', 'Geared Motors', 'Cars & Bike Accessories', 'Performance Boosters', 'Custom Exhaust', 'Brake Components', 'Discs & Drums', 'Calipers', 'Brake Shoe', 'Pedal Assembly', 'Brake Oil', 'Plastics & Polymer Components', 'Tires & Tubes', 'Body Panel', 'Instruments Panel', 'Plastic molded parts', 'Fasteners, Nuts Bolts, Rivets, Clamps', 'Nut & Bolt', 'Washers', 'Clamps', 'Rivets', 'Clamping Devices', 'Engine Components', 'Engine Block', 'Piston', 'Timing Chains', 'Crankshaft & Camshaft', 'Cams', 'Flywheel', 'Chassis & Body Building', 'Trailers', 'Cab & Cowl', 'Bus Body', 'Truck Body', 'Interior Parts', 'Seats', 'Gears, Gearboxes and Related Components', 'Spur Gears', 'Worm Gears', 'Gearbox Casing', 'Helical Gears', 'Sprockets', 'Elecrical & Electronics Items', 'Battery', 'Starter Motors', 'Sheet Metal Components', 'Bearing, Bushes & Related Items', 'Joints, Shafts, Couplings', 'Joints', 'Rigid Couplingd', 'Flexible Couplings', 'Shafts', 'Fiber Parts', 'Body Panel', 'Jigs & Fixtures', 'Jigs', 'Fixtures', 'Clamping Devices', 'Bushes', 'Other OEM Parts', 'Bearings', 'Valves', 'Carburettor', 'Pumps & Turbines', 'Blades', 'Casing & Body', 'Hydraulic Machines', 'Pneumatic Machines', 'Gears, Gearboxes and Related Components', 'Spur Gears', 'Worm Gears', 'Gearbox Casing', 'Helical Gears', 'Sprockets', 'Joints, Shafts, Couplings', 'Jigs & Fixtures', 'Jigs', 'Fixtures', 'Clamping Devices', 'Bushes', 'Bearing, Bushes & Related Items', 'Fasteners, Nuts Bolts, Rivets, Clamps', 'Boilers & Tanks', 'Plastic Tanks', 'Boilers', 'Motors & Generators & Parts', 'DC Motors', 'AC Motors', 'Generators', 'Inverters', 'Motors & Generators & Parts', 'DC Motors', 'AC Motors', 'Generators', 'Inverters', 'Pumps & Turbines', 'Electrical Fitting Items', 'Wires', 'Insulators', 'Switches', 'Consumer Electronics Products', 'Electronics Products', 'Instruments', 'Actuators & Sensors', 'Industrial Chemicals', 'Metallic Raw Materials', 'Steel', 'Aluminium', 'Non Metallic raw material', 'Machining Fluids', 'Coolants', 'Lubricants', 'Packaging Materials', 'Measuring Equipments', 'Plastics & Rubbers', 'Welding Setup', 'Jigs & Fixtures', 'Pipes & Tubes', 'Machine Tools', 'Milling Machines & Components', 'Lathe & Components', 'CNC Machines', 'Material Handling Equipments', 'Conveyors', 'Stackers', 'Feeders', 'Robotic', 'Special Purpose Machines', 'Plastic Processing Machines', 'Extrusion machine', 'Injection maolding Machine', 'Rotomolding Machine', 'Jigs & Fixtures', 'Power Tools', 'Hand Tools', 'Steel Parts', 'Pipes & Tubes', 'Steel Beams', 'Nuts & Bolts', 'Clamps', 'Steel Fabrication', 'Aluminium Parts', 'Aluminium Gates & windows', 'Aluminium Fabrication', 'Aluminium Partitions', 'Cement & Bricks', 'Cement & Concrete', 'Building Bricks', 'Fly Ash Bricks', 'Fire Bricks', 'Concrete Blocks', 'Scaffoldings & Accessories', 'Scaffoldings', 'Scaffolding fittings', 'Ladders', 'Consruction Machinery', 'Cranes', 'Earth Moving Machinery', 'Concrete mixers', 'Impact Crushers', 'Brick Making Machines', 'Plumbing Items', 'Steel pipes', 'Plastic & PVC Pipes', 'Hose Pipes', 'Showers', 'Safety Items', 'Fire Extinguishers', 'Water proofing  System', 'Wood & Furniture', 'Timber & Plywood', 'Doors & Windows', 'Gates & Grills', 'Wooden Furniture', 'Plastic Furniture', 'Metallic Furniture', 'Coatings & Finishing', 'Water proofing  System', 'Curtain Walls', 'Powder Coating', 'Floor Coatings', 'Paints', 'Tiles', 'Interior Items', 'Industrial Chemicals', 'Pigments', 'Paint', 'Food Chemical & Preservatives', 'Agricultural Equipments', 'Agricultural Machinery', 'Insecticides & Pesticides', 'Edible Agricultural Products', 'Fertilizers & soil Additives', 'Seeds', 'Finished Clothes (Wearable)', 'Women Clothing', "Men's Clothing", 'T shirt Printing', 'Finished Clothes (Non Wearable)', 'Cloth raw material', 'Leather Products', 'Machinery', 'Measuring Equipments', 'Laboratory equipments', 'Material Handling Equipments & Parts', 'Welding Setup', 'Hand Tools', 'Power Tools', 'Designing', 'Industrial Services', 'Environmental Planning', 'Simulation & Analysis Services', 'Planning & Implementation', 'Web Designing Services', 'Software solutions', 'Online Marketing solutions', 'Installation, Maintenance etc.', 'Heating, Ventilation & Airconditioning', 'Solar Energy Installations', 'Electrical Installations', 'Machine Tools Installations', 'Transportation & Courier services', 'Export Services', 'Import Services', 'Training & Hiring Services', 'Lean & Six sigma training', 'Industrial Training', 'CAD, CAM, CAE Training', 'Computer & IT training', 'Online Marketing solutions', 'Website Making', 'Profile Management', 'Household services', 'Plumbing & fitting', 'Interior Decoration', 'Electrial Installation', 'Construction Services', 'Machine Repairing', 'Repairing Services']

    for i in li:
        t, created = Category.objects.get_or_create(name=i, level=1)

    for i in li2:
        try:
            a = Category.objects.get(name=i, level=1)
            if a:
                k = [a]
        except Exception:
            b, created = Category.objects.get_or_create(name=i, level=2)
            b.sub_cat = k

    for i in li3:
        try:
            a = Category.objects.get(name=i, level=2)
            if a:
                k = [a]
        except Exception:
            b, created = Category.objects.get_or_create(name=i, level=3)
            b.sub_cat = k

    return redirect('/')


def c_r(request):
    id = request.GET.get('id')
    pro = Products.objects.get(id=id)
    wp = pro.producer
    ppp = Product_Categories.objects.filter(product__producer=wp)
    if len(ppp)>0:

        pc = ppp.reverse()[0]
        p = pc.product
        q = Product_Categories.objects.filter(product=p)

        for t in q:
            Product_Categories.objects.create(product=pro, category=t.category, level=t.level)
        return redirect('/internal/activity/?q=p')
    else:
        pass


def int_category(request, slug):
    category = Category.objects.get(slug=slug)
    # products = Products.objects.filter()
    return render(request, 'activities/category.html', locals())


def category(request, slug):        # Products
    category = Category.objects.get(slug=slug)
    products = Products.objects.filter(categories=category)
    return render(request, 'products/category_products.html', locals())


def category_wp(request, slug):        # Workplace
    category = Category.objects.get(slug=slug)
    products = Products.objects.filter(categories=category).select_related('producer')
    workplaces = []
    for p in products:
        if p.producer not in workplaces:
            workplaces.append(p.producer)
        else:
            pass
    return render(request, 'products/category_workplace.html', locals())


def category_update(request):
    category = Category.objects.all()
    for c in category:
        name = c.name
        subs = c.get_sub()
        parents = c.get_parent_cat()
        text = ''
        if subs:
            for s in subs:
                n = s.name+', '
                text += n
        if parents:
            for s in parents:
                n = s.name+','
                text += n

        c.meta_des = text[:150]
        c.save()
    return redirect('/')

import traceback

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
        dictionary = {}
        ps = Products()
        p = None
        if request.method == 'POST':
            if request.POST.get('product'):
                p = Products.objects.create(product=request.POST['product'], user=user, producer=wp,
                                            delivery_details=dd, delivery_charges=dc, minimum=minimum)
                if c:
                    for t in c:
                        Product_Categories.objects.create(product=p, category=t.category, level=t.level)
                up = user.userprofile
                up.points += 5
                up.save()
                response['p_id'] = p.id
            # else:
            #     p_t = Products()
            #
            return HttpResponse(json.dumps(response), content_type="application/json")
        else:
            if user.userprofile.product_email:
                no_prod_con = False
            else:
                no_prod_con = True

            return render(request, 'products/edit.html', {'c1_all': c1_all, 'c1_1': c1_1, 'c1_2': c1_2,
                                                          'c1_3': c1_3, 'c1_4': c1_4, 'c1_5': c1_5, 'c1_6': c1_6,
                                                          'c1_8': c1_8, 'p': p, 'c': c, 'first_time': True,
                                                          'no_prod_con': no_prod_con, 'delivery_details': dd,
                                                          'delivery_charges': dc, 'minimum': minimum})
    else:
        p = Products.objects.get(id=id)
        dictionary = {}
        direct = p._meta.get_all_field_names()
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
            c = Product_Categories.objects.filter(product=p.id).order_by('level')
            dictionary = {'c1_all': c1_all, 'c1_1': c1_1, 'c1_2': c1_2, 'c1_3': c1_3, 'c1_4': c1_4, 'c1_5': c1_5,
                          'c1_6': c1_6,'c1_8': c1_8, 'product': p, 'c': c, 'first_time': True}
            return render(request, 'products/edit.html', dict(list(p.__dict__.items()) + list(dictionary.items())))
