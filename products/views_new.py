from django.shortcuts import render, redirect, HttpResponse
from django.template.loader import render_to_string
from products.models import Category, Product_Categories, Products
from nodes.models import Images, Document
from django.contrib.auth.decorators import login_required, user_passes_test
from operator import itemgetter
import json
from PIL import Image
from django.db.models import Q
from django.contrib.auth.models import User


@login_required
def add_image(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        n = request.POST.get('index')
        user = request.user
        # path = request.META.get('HTTP_REFERER')
        # if 'internal' in path:
        #     user = User.objects.get(username='jainamshah777')
        # p = Products.objects.filter(user=user).last()
        transformation = request.POST.get('transformation')
        i = Images()
        x = i.upload_image_new(image=image, user=user, trans=transformation)
        ii = Images.objects.filter(user=user, temp_key=n)
        if ii:
            ii.delete()
        x.temp_key = n
        x.save()
    return HttpResponse()


@login_required
def change_image(request, id):
    if request.method == 'POST':
        image = request.FILES.get('image')
        user = request.user
        p = Products.objects.filter(id=id)
        transformation = request.POST.get('transformation')
        i = Images()
        x = i.upload_image_new(image=image, user=user, name=p.product, trans=transformation)
        p.image = x
        p.save()
    return HttpResponse()


@login_required
def add_product(request):
    path = request.get_full_path()
    user = request.user
    # if 'internal' in path:
    #     internal = True
    #     user = User.objects.get(username='jainamshah777')
    workplace = user.userprofile.primary_workplace
    response = {}
    if request.method == 'POST':
        n = int(request.POST.get('index'))
        if request.POST.get('product'):
            last = Products.objects.filter(Q(user=user) | Q(producer=workplace)).last()
            if last:
                dd = last.delivery_details
                dc = last.delivery_charges
                minimum = last.minimum
            else:
                dd = None
                dc = None
                minimum = None
            if request.POST.get('delivery_details'):
                dd = request.POST.get('delivery_details')
            if request.POST.get('delivery_charges'):
                dc = request.POST.get('delivery_charges')
            if request.POST.get('minimum'):
                minimum = request.POST.get('minimum')
            p = Products.objects.create(product=request.POST['product'], user=user, producer=workplace, minimum=minimum,
                                        delivery_details=dd, delivery_charges=dc, description=request.POST['description'])
            li = [request.POST.get('category1'), request.POST.get('category2'), request.POST.get('category3')]
            p.set_categories(li)
            # if li.count('') == len(li):
            #     # c = Product_Categories.objects.filter(product=last.id).order_by('level')
            #     pass
            # else:
            #     p.set_categories(li)
            # ii = Images.objects.filter(user=user, temp_key=n)
            i = Images.objects.filter(user=user, temp_key=n).first()
            if i:
                p.image = i
                i.temp_key = None
                i.save()
            p.save()
            user.userprofile.add_points(5)
            response['p_id'] = p.id
            # return HttpResponse(json.dumps(response))
            n = request.POST.get('index')
            n = int(n) + 5
            product = Products.objects.filter(producer=workplace)[0]
            response['last_p'] = render_to_string('products/small_product.html', {'product': p})
            response['new_form'] = render_to_string('products/add_multi_form.html', {'n': n})
            return HttpResponse(json.dumps(response), content_type="application/json")
        else:
            return HttpResponse()
    else:
        # show the add products page
        p = Products.objects.filter(producer=workplace).last()
        # last added products
        previous_prods = Products.objects.filter(producer=workplace)[:1]
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
        first_time = False
        return render(request, 'products/add_multi.html', locals())


@login_required
def add_products_file(request):
    if request.method == 'POST':
        user = request.user
        file = request.FILES.get('product_list', None)
        d = Document()
        x = d.upload_product_doc(doc=file, user=user)
        return HttpResponse()
    else:
        return render(request, 'products/upload_bulk.html')


@login_required
def manage(request):
    products = Products.objects.filter(producer=request.user.userprofile.primary_workplace)
    return render(request, 'products/manage.html', locals())


# def change_owner(request):
#


THUMB_SIZES = [
    (233, 233),
    (89, 89),
    (34, 34)
]

from django.core.files.base import ContentFile
from io import BytesIO


def crawl_images():
    """
    Crawls the model for all the image files
    """
    images = Images.objects.all()
    for i in images:
        if not i.image:
            print('** Image not available for id : '+str(i.id))
            i.delete()
        else:
            if not i.image_thumbnail_xs:
                try:
                    file = Image.open(i.image)
                    name = i.image.name
                    if '/' in name:
                        name = name.split('/')[-1]
                    f_format = file.format
                    i.image_format = f_format
                    thumb = []
                    for size in THUMB_SIZES:
                        f_thumb = file
                        f_thumb.thumbnail(size, resample=2)
                        thumb_io = BytesIO()
                        if f_format == 'JPEG':
                            f_thumb.save(thumb_io, f_format, optimize=True, progressive=True)
                        else:
                            f_thumb.save(thumb_io, f_format, optimize=True)
                        thumb.append(thumb_io)
                    i.image_thumbnail.save(name, content=ContentFile(thumb[0].getvalue()))
                    i.image_thumbnail_sm.save(name, content=ContentFile(thumb[1].getvalue()))
                    i.image_thumbnail_xs.save(name, content=ContentFile(thumb[2].getvalue()))
                    i.save()
                    print('++ Images created for id : '+str(i.id))
                    print('   '+name)
                except FileNotFoundError:
                    print('-- File not found for id : '+str(i.id))
            else:
                print(">> All good for id: "+str(i.id))






