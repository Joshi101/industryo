from django.shortcuts import render, redirect
from products.models import Products


def add_product(request):
    if request.method == 'POST':
        product = request.POST.get('product')
        description = request.POST.get('description')
        tags = request.POST.get('tags')
        # user = request.user
        workplace = request.user.userprofile.primary_workplace
        p = Products.objects.create(product=product, producer=workplace, description=description)
        p.set_tags(tags)
        return redirect('/products/'+p.slug)
    else:
        return redirect('/workplace/add_products')


def product(request, slug):
    product = Products.objects.get(slug=slug)
    tags = product.tags.all()

    return render(request, 'nodes/articles.html', locals())


def delete_product(request):
    id = request.GET.get('id')
    product = Products.objects.get(id=id)
    if request.user.userprofile.primary_workplace == product.producer:

        product.delete()
    return redirect('/workplace/add_products')

# Create your views here.
