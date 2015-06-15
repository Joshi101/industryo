from django.shortcuts import render, redirect
from products.models import Products


def add_product(request):
    if request.method == 'POST':
        product = request.POST.get('product')
        user = request.user
        workplace = request.user.userprofile.primary_workplace
        p = Products.objects.create(product=product, workplace=workplace,)
        image = request.FILES.get('image', None)
        if image:
            p.add_image(image, user)
        tags = request.POST.get('tags')
        if tags:
            pass

        return redirect('/workplace/products')
    else:
        return redirect('/workplace/add_products')




# Create your views here.
