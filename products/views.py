from django.shortcuts import render, redirect, HttpResponse
from django.template.loader import render_to_string
from products.models import Products
import json
from nodes.models import Images


def add_product(request):
    if request.method == 'POST':
        response = {}
        r_value = {}
        r_inputs = []
        r_html = {}
        r_elements = []
        product = request.POST.get('product')
        description = request.POST.get('description')
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
        print(li)
        user = request.user
        workplace = request.user.userprofile.primary_workplace
        image0 = request.FILES.get('image0', None)
        p = Products.objects.create(product=product, producer=workplace, description=description, user=user)
        print(tags)
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
        return redirect('/products/'+p.slug)
        # return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        return render(request, 'products/add_product.html')


def product(request, slug):
    product = Products.objects.get(slug=slug)

    tags = product.tags.all()

    return render(request, 'products/one_product.html', locals())


def delete(request):
    id = request.GET.get('id')
    product = Products.objects.get(id=id)
    if request.user.userprofile.primary_workplace == product.producer:

        product.delete()
    return redirect('/workplace/add_products')


def change_image(request, id):
    p = Products.objects.get(id=id)
    user = request.user
    workplace = user.userprofile.primary_workplace
    if p.producer == workplace:
        image0 = request.FILES.get('image0', None)
        if image0:
            i = Images()
            x = i.upload_image(image=image0, user=user)
            p.image = x
            p.save()
    else:
        return redirect('/')
    return redirect('/products/'+p.slug)


def random(request):
    user = request.user
    if user.userprofile.primary_workplace:
        a = user.userprofile.primary_workplace.workplace_type
        print(a)
        products = Products.objects.all().order_by('?')[:6]
    else:
        products = Products.objects.all().order_by('?')[:6]
    print(products)
    return render(request, 'snippets/right/products.html', {'products': products})


# Create your views here.