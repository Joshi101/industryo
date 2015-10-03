from django.shortcuts import render, redirect, HttpResponse
from django.template.loader import render_to_string
from products.models import Products
import json


def add_product(request):
    if request.method == 'POST':
        response = {}
        r_value = {}
        r_inputs = []
        r_html = {}
        r_elements = []
        product = request.POST.get('product')
        description = request.POST.get('description')
        tags = request.POST.get('tags')
        li = request.POST.get('target_segments')
        user = request.user
        workplace = request.user.userprofile.primary_workplace
        p = Products.objects.create(product=product, producer=workplace, description=description, user=user)
        p.set_tags(tags)
        p.set_target_segments(li)
        r_elements = ['products_list']
        r_html['products_list'] = render_to_string('workplace/one_product.html', {'product': p})
        response['html'] = r_html
        response['elements'] = r_elements
        response['prepend'] = True
        return HttpResponse(json.dumps(response), content_type="application/json")


def product(request, slug):
    product = Products.objects.get(slug=slug)
    tags = product.tags.all()

    return render(request, 'nodes/articles.html', locals())


def delete(request):
    id = request.GET.get('id')
    product = Products.objects.get(id=id)
    if request.user.userprofile.primary_workplace == product.producer:

        product.delete()
    return redirect('/workplace/add_products')

# Create your views here.