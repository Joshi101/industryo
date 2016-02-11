from django.shortcuts import render, redirect, HttpResponse
from django.template.loader import render_to_string
from nodes.forms import SetLogoForm
from products.models import Products, Category
from userprofile.models import UserProfile
from django.contrib.auth.models import User
from tags.models import Tags
import json
from nodes.models import Images
from django.contrib.auth.decorators import login_required
from activities.models import Enquiry
from datetime import datetime, timedelta, time, date
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.core.mail import get_connection, send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


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


def product(request, slug):

    product = Products.objects.get(slug=slug)
    producer = product.producer
    members = UserProfile.objects.filter(primary_workplace=product.user.userprofile.primary_workplace.pk)
    tagss = product.tags.all()
    prod_img_form = SetLogoForm()
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
            user = request.user
            message = request.POST.get('message')
            phone = request.POST.get('phone')
            prod = Products.objects.get(id=p)
            e = Enquiry.objects.filter(user=user, date__gt=yesterday)
            if e.count() < 5:
                e = Enquiry.objects.create(product=prod, user=user, message=message, phone_no = phone)
                user.userprofile.notify_inquired(e)
                send_enq_mail(e)

        else:
            email = request.POST.get('email')
            name = request.POST.get('name')
            company = request.POST.get('company')
            p = request.POST.get('pid')
            message = request.POST.get('message')
            phone = request.POST.get('phone')
            prod = Products.objects.get(id=p)
            e = Enquiry.objects.filter(email=email, date__gt=yesterday)
            if e.count() < 5:
                e = Enquiry.objects.create(product=prod, name=name, company=company, email=email, message=message, phone_no = phone)
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
    # company = user.userprofile.primary_workplace
    # enquiries = Enquiry.objects.filter(product__producer=company)
    enquiry = Enquiry.objects.get(id=iid)
    enquiry.seen = True
    enquiry.save()

    return render(request, 'enquiry/enquiry_details.html', {
        'enquiry': enquiry,
        })


def send_enq_mail(e):
    user = e.product.user
    user_email = user.email
    product = e.product
    name = user.userprofile
    # product_url = 'www.corelogs.com/products/'+product.slug
    # enquiry_url = 'www.corelogs.com/products/enquiry_all'
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


def int_add_product(request):
    if request.method == 'POST':

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
        u = request.POST.get('person')
        user = User.objects.get(username=u)
        workplace = user.userprofile.primary_workplace
        image0 = request.FILES.get('image0', None)
        if len(pro) > 3:
            product = pro
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
        return redirect('/')
        # return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        return render(request, 'activities/p/add_product.html')


def int_product(request, slug):

    product = Products.objects.get(slug=slug)
    members = UserProfile.objects.filter(primary_workplace=product.user.userprofile.primary_workplace.pk)
    tagss = product.tags.all()
    prod_img_form = SetLogoForm()
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

    else:
        if request.user.is_authenticated():
            if request.user.userprofile.primary_workplace:
                a = request.user.userprofile.primary_workplace.workplace_type
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
        return render(request, 'marketplace/marketplace.html', {'result_list': result_list, 'tags':tags, 'tags2':tags2, 'n':n, 'm':m})


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
        c1 = request.POST.get('c1')
        c2 = request.POST.get('c2')
        index = request.POST.get('i')
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

        if c1:
            print("C1 AAYA")
        if c2:
            print("C2 AAYA")

        workplace = request.user.userprofile.primary_workplace
        image0 = request.FILES.get('image0', None)
        if len(pro) > 3:
            product = pro
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
        r_html['products_list'] = render_to_string('products/one_product.html', {'product': p, 'index': index})
        response['html'] = r_html
        response['elements'] = r_elements
        response['prepend'] = True
        # return redirect('/products/'+p.slug)
        # url = '/workplace/products/'+workplace.slug
        # return HttpResponseRedirect(url)
        return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        tags1 = []
        tags12 = []
        li1 = [590, 591, 581, 582, 586, 587, 243, 218, 621, 512]
        li2 = [11, 12, 32, 543, 42, 99, 67]
        li3 = [111, 121, 321, 545, 422, 199, 167]
        li4 = [171, 131, 351, 75, 425, 194, 17]
        tags1 = Tags.objects.filter(pk__in=li1)
        tags2 = Tags.objects.filter(pk__in=li2)
        tags3 = Tags.objects.filter(pk__in=li3)
        tags4 = Tags.objects.filter(pk__in=li4)

        c1 = Category.objects.filter(level=1)
        for t in tags1:
            p = Products.sell.filter(tags=t, target_segment__contains='C')
            t2 = Tags.objects.filter(products__in=p).distinct().exclude(id__in=li1)
            tags12.append(t2)
        return render(request, 'products/add_product.html', {'tags1': tags1, 'tags2': tags2, 'tags3': tags3, 'tags4': tags4,
                                                             'tags12': tags12, 'tags22': tags12, 'tags32': tags12, 'tags42': tags12})


def add_1_product(request):
    user = request.user
    producer = user.userprofile.primary_workplace

    if request.method == 'POST':
        pro = request.POST.get('product')
        description = request.POST.get('description')
        cost = request.POST.get('cost')
        bulk = request.POST.get('bulk')
        services = request.POST.get('services')

        p = Products.objects.create(product=pro, producer=producer, description=description, cost=cost)
        t = []
        # If Bulk quantity Product

        if bulk:
            tag = Tags.objects.get(id=999)
            t.append(tag)
        elif services:
            tag = Tags.objects.get(id=999)
            t.append(tag)

        target = request.POST.get('target')
        if target == 1:
            # Students, Racing Enthusiasts
            pass
            # list = ['SAE Team Related Items', 'Racing Enthusiasts & Automobile Accessories', ]
        elif target == 2:
            # Industries & SMEs
            pass

    else:
        last_product = Products.objects.filter(producer=producer)[-1]
        tags = last_product.tags.all()
    return redirect('/')


# def add_category(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         pro = request.POST.get('product')


def initial_category(request):
    li = ['SAE Teams & Related Items', 'Electronics & RC Items for enthusiasts', 'Products for Racing Enthusiast', 'Industry Supplies ', 'Raw Materials for Industries', 'Clothes & Textiles', 'Industrial Chemicals', 'Agricultural & Agrotech products', 'Automobile & Aerospace Parts', 'Industrial Machinery & Parts', 'Tools & Equipments', 'Packaging', 'Material Handling Equipment', 'Industrial & Manufacturing Consultancy', 'Transport & Courier Service', 'Internet & Software Based Services', 'Installation Services']
    li2 = ['SAE Teams & Related Items', 'Safety Equipment', 'Racing Accessories', 'Suspension Parts', 'Powertrain Parts', 'Wheel Assembly', 'Rollcage, Pipes & Tubes', 'Brakes', 'Steering System', 'Electricals & Electronics', 'Aesthetics', 'Electronics & RC Items for enthusiasts', 'RC Items', 'Arduino kits & Raspberry Pi', 'Electronics Components', 'DC Motors', 'Products for Racing Enthusiasts', 'Cars & Bike Accessories', 'Performance Boosters', 'Automobile & Aerospace Parts', 'OEM Parts', 'Plastics & Polymer Components', 'Fasteners, Nuts Bolts, Rivets, Clamps', 'Engine Components', 'Chassis & Body Building', 'Gears, Gearboxes and Related Components', 'Elecrical & Electronics Items', 'Sheet Metal Components', 'Bearing, Bushes & Related Items', 'Joints, Shafts, Couplings', 'Fiber Parts', 'Chemicals,  Dies, Paints', 'Industrial Chemicals', 'Pigments', 'Paint', 'Dies', 'Food Chemical & Preservatives', 'Tools & Equipments', 'Power Tools', 'Hand Tools', 'Measuring Equipments', 'Installation Services', 'Heating, Ventilation & Airconditioning', 'Solar Energy Installations', 'Electrical Installations', 'Machine Tools Installations', 'Engineering & Industrial Services', 'Designing ', 'Industrial Services', 'Environmental Planning', 'Simulation & Analysis Services', 'Planning & Implementation', 'Internet & Software Based Services', 'Web Designing Services', 'Software solutions', 'Online Marketing solutions', 'Raw Materials for Industries', 'Plastics & Polymers', 'Metals Metallic Components', 'Chemicals', 'Agricultural & Agrotech products', 'Agricultural Equipments', 'Agricultural Machinery', 'Insecticides & Pesticides', 'Edible Agricultural Products', 'Fertilizers & soil Additives', 'Seeds']
    li3 = ['Safety Equipment', 'Helmet', 'Driver Suit', 'Other Wearables', 'Racing Accessories', 'Suspension Parts', 'Dampers', 'Shock Absorbers', 'Knuckles & Hubs', 'Powertrain Parts', 'Engine Accessories', 'Exhaust', 'Spares', 'Engine', 'Gearbox', 'CVT', 'DC Motor', 'Wheel Assembly', 'Tubes & Tyres', 'Rims & Tyres', 'ATV Tyres', 'Formula Tyres', 'Rollcage, Pipes & Tubes', 'AISI 1018', 'AISI 4130 Chromoly', 'AISI 4340', 'Carbon Fiber', 'Brakes', 'Calipers', 'Brake Lines', 'Master Cylinder', 'Brake Pedal & Assembly', 'Steering System', 'Steering Rack', 'Steering Wheels', 'Tie Rods', 'Electricals & Electronics', 'Switches', 'Lights', 'Aesthetics', 'Electronics & RC Items for enthusiasts', 'RC Items', 'Cars', 'Monster trucks', 'Helicopter', 'Ship', 'Plane', 'Quadcopters & Parts', 'Arduino kits & Raspberry Pi', 'Raspberry pi & spares', 'Arduino sheilds', 'Electronics Components', 'Resistors & Capacitors', 'Wireless', 'ICs', 'LCD Screens', 'Sensors', 'DC Motors', 'Stepper Motors', 'Servo motors', 'Geared Motors']
    for i in li3:
        try:
            a = Category.objects.get(name=i)
            if a:
                k = [a]
        except Exception:
            b = Category.objects.create(name=i, level=3)
            b.sub_cat = k

    return redirect('/')



