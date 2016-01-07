from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from django.template.loader import render_to_string
from nodes.forms import SetLogoForm
from products.models import Products
from userprofile.models import UserProfile
from django.contrib.auth.models import User
import json
from nodes.models import Images
from django.contrib.auth.decorators import login_required
from activities.models import Enquiry
from datetime import datetime, timedelta, time, date
from django.core.mail import send_mail


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
        # new_interest = t
        # r_elements = ['tag_container']
        # r_html['tag_container'] = render_to_string('snippets/tag_short.html', {'tag': new_interest, 'ajax':True})
        # response['html'] = r_html
        # response['elements'] = r_elements
        # response['prepend'] = True
        # return HttpResponse(json.dumps(response), content_type="application/json")

        new_interest = t
        r_elements = ['info_field_value']
        r_html['info_field_value'] = render_to_string('snippets/tag_short.html', {'tags': new_interest})
        response['html'] = r_html
        response['elements'] = r_elements
        response['prepend'] = False
        return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        return redirect('/user/'+request.user.username)


def add_product(request):
    if request.method == 'POST':
        response = {}
        r_value = {}
        r_inputs = []
        r_html = {}
        r_elements = []
        pro = request.POST.get('product')
        description = request.POST.get('description')
        cost = request.POST.get('cost')
        tags = request.POST.get('tag')
        status = request.POST.get('status')
        li = []

        a = request.POST.get('A')
        if a:
            li.append('A')
        b = request.POST.get('B')
        if b:
            li.append('B')

        c = request.POST.get('C')
        if c:
            li.append('C')
        o = request.POST.get('O')
        if o:
            li.append('O')
        user = request.user

        workplace = request.user.userprofile.primary_workplace
        image0 = request.FILES.get('image0', None)
        if len(pro)>3:
            product=pro
            p = Products.objects.create(product=product, producer=workplace, description=description, user=user, cost=cost)
            p.set_tags(tags)
            p.set_target_segments(li)

        if image0:
            i = Images()
            x = i.upload_image(image=image0, user=user)
            p.image = x
            p.save()
        if status:
            p.status = status
            p.save()
        r_elements = ['products_list']
        r_html['products_list'] = render_to_string('workplace/one_product.html', {'product': p})
        response['html'] = r_html
        response['elements'] = r_elements
        response['prepend'] = True
        return redirect('/products/'+p.slug)
        # url = '/workplace/products/'+workplace.slug
        # return HttpResponseRedirect(url)
        # return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        return render(request, 'products/add_product.html')


def product(request, slug):

    product = Products.objects.get(slug=slug)
    members = UserProfile.objects.filter(primary_workplace=product.user.userprofile.primary_workplace.pk)
    tagss = product.tags.all()
    prod_img_form = SetLogoForm()
    return render(request, 'products/one_product.html', locals())


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
            user = request.user
            message = request.POST.get('message')
            prod = Products.objects.get(id=p)
            e = Enquiry.objects.filter(user=user, date__gt=yesterday)
            if e.count() < 5:
                e = Enquiry.objects.create(product=prod, user=user, message=message)
                user.userprofile.notify_inquired(e)
                send_enq_mail(e)

        else:
            email = request.POST.get('email')
            name = request.POST.get('name')
            company = request.POST.get('company')
            p = request.POST.get('pid')
            message = request.POST.get('message')
            prod = Products.objects.get(id=p)
            e = Enquiry.objects.filter(email=email, date__gt=yesterday)
            if e.count() < 5:
                e = Enquiry.objects.create(product=prod, name=name, company=company, email=email, message=message)
                up = prod.user.userprofile
                up.notify_inquired(e)
                send_enq_mail(e)

        return redirect('/products/'+prod.slug)


@login_required
def enquiry_all(request):
    user = request.user
    company = user.userprofile.primary_workplace

    enquiries = Enquiry.objects.filter(product__producer=company)

    return render(request, 'enquiry/enquiry.html', {
        'enquiries': enquiries,
        })


def enquiry(request, id):
    iid = int(id)
    user = request.user
    company = user.userprofile.primary_workplace
    enquiries = Enquiry.objects.filter(product__producer=company)
    enquiry = Enquiry.objects.get(id=iid)

    return render(request, 'enquiry/enquiry_details.html', {
        'enquiry': enquiry,
        })


def send_enq_mail(e):
    user = e.product.user
    user_email = user.email
    product = e.product
    name = user.userprofile
    product_url = 'www.corelogs.com/products/'+product.slug
    enquiry_url = 'www.corelogs.com/products/enquiry'
    template = u'''
    Hi {0},

    You have got an enquiry about the product <a href="{1}">{2}</a>.

    To see the details of the enquiry, please visit <a href="{3}">This Link</a>.

    We wish you success. Thanks.

    Team CoreLogs
    '''

    content = template.format(name, product_url, product, enquiry_url)
    subject = u'''[CoreLogs] Enquiry about {0}'''.format(product)
    try:
        send_mail(subject, content, 'sp@corelogs.com', [user_email])
    except Exception:
        pass

    return 'a'


def int_add_product(request):
    if request.method == 'POST':
        response = {}
        r_value = {}
        r_inputs = []
        r_html = {}
        r_elements = []
        pro = request.POST.get('product')
        description = request.POST.get('description')
        cost = request.POST.get('cost')
        tags = request.POST.get('tag')
        li = []

        a = request.POST.get('A')
        if a:
            li.append('A')
        b = request.POST.get('B')
        if b:
            li.append('B')

        c = request.POST.get('C')
        if c:
            li.append('C')
        o = request.POST.get('O')
        if o:
            li.append('O')
        u = request.POST.get('person')
        user = User.objects.get(username=u)
        workplace = user.userprofile.primary_workplace
        image0 = request.FILES.get('image0', None)
        if len(pro)>3:
            product=pro
            p = Products.objects.create(product=product, producer=workplace, description=description, user=user, cost=cost)
            p.set_tags(tags)
            p.set_target_segments(li)
        if image0:
            i = Images()
            x = i.upload_image(image=image0, user=user)
            p.image = x
            p.save()
        r_elements = ['products_list']
        r_html['products_list'] = render_to_string('workplace/one_product.html', {'product': p})
        response['html'] = r_html
        response['elements'] = r_elements
        response['prepend'] = True
        return redirect('/internal/products/'+p.slug)
        # return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        return render(request, 'activities/p/add_product.html')

def int_product(request, slug):

    product = Products.objects.get(slug=slug)
    members = UserProfile.objects.filter(primary_workplace=product.user.userprofile.primary_workplace.pk)
    tags = product.tags.all()
    prod_img_form = SetLogoForm()
    return render(request, 'activities/p/one_product.html', locals())

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
# Create your views here.
