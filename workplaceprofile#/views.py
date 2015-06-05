from django.shortcuts import render, redirect
from workplaceprofile.models import *
from workplaceprofile.forms import *
from nodes.models import *


def edit_workplace_profile(request):
    w = request.user.userprofile.primary_workplace
    type = w.workplace_type
    if type == 'C':
        form = EditTeamForm(request.POST, request.FILES)
        if request.method == 'POST':
            if not form.is_valid():
                print("fuck")
                return render(request, 'workplace/set_segment.html', {'form': form})
            else:
                city = form.cleaned_data.get('city')
                address = form.cleaned_data.get('address')
                contact = form.cleaned_data.get('contact')
                about = form.cleaned_data.get('about')
                institution_name = form.cleaned_data.get('institution_name')
                parti = form.cleaned_data.get('participation')
                logo = form.cleaned_data.get('logo')

                area, created = Area.objects.get_or_create(name=city)
                institution, created = Institution.objects.get_or_create(name=institution_name, area=area)

                wp = WorkplaceProfile.objects.get(workplace=w)
                wp.area = area   # get or create models
                wp.address = address
                wp.contact = contact
                wp.about = about
                wp.institution = institution   # get or create on models
                wp.create_participation(parti)
                user = request.user
                wp.set_logo(image=logo, user=user)
                # wp.set_logo(logo, user)

                wp.save()

            return render(request, 'workplace_profile/edit.html', {'form': form})
        else:
            return render(request, 'workplace_profile/edit.html', {'form': form})

    elif type == 'B':
        form = EditSMEForm(request.POST)
        if request.method == 'POST':
            if not form.is_valid():
                print("fuck")
                return render(request, 'workplace/set_segment.html', {'form': form})
            else:
                city = form.cleaned_data.get('city')
                address = form.cleaned_data.get('address')
                contact = form.cleaned_data.get('contact')
                about = form.cleaned_data.get('about')
                materials = form.cleaned_data.get('materials')
                assets = form.cleaned_data.get('assets')
                operations = form.cleaned_data.get('operations')
                product_details = form.cleaned_data.get('product_details')
                capabilities = form.cleaned_data.get('capabilities')

                area, created = Area.objects.get_or_create(name=city)

                wp = WorkplaceProfile.objects.get(workplace=w)
                wp.area = area
                wp.address = address
                wp.contact = contact
                wp.about = about
                wp.product_details = product_details
                wp.capabilities = capabilities

                wp.set_materials(materials)
                wp.set_assets(assets)
                wp.set_operations(operations)

                wp.save()

            return render(request, 'workplace_profile/edit.html', {'form': form})
        else:
            return render(request, 'workplace_profile/edit.html', {'form': form})


def search_asset(request):
    if 'the_query' in request.GET:
        t = request.GET['the_query']
        create = request.GET['the_create']
        o = Tags.objects.filter(tag__icontains=t, type='assets')[:6]

        return render(request, 'workplace/list.html', {'o': o, 'create': create})
    else:
        return render(request, 'workplace/list.html')


def search_operation(request):
    if 'the_query' in request.GET:
        t = request.GET['the_query']
        create = request.GET['the_create']
        o = Tags.objects.filter(tag__icontains=t, type='operations')[:6]

        return render(request, 'tags/list.html', {'o': o, 'create': create})
    else:
        return render(request, 'tags/list.html')


def search_material(request):
    if 'the_query' in request.GET:
        t = request.GET['the_query']
        create = request.GET['the_create']
        o = Tags.objects.filter(tag__icontains=t, type="materials")[:6]

        return render(request, 'tags/list.html', {'o': o, 'create': create})
    else:
        return render(request, 'tags/list.html')


def set_materials(request):
    form = SetMaterialForm(request.POST)
    if request.method == 'POST':
        if not form.is_valid():
            print("fuck")
            return redirect('/')
        else:
            user = request.user
            workplace = user.userprofile.primary_workplace
            wp = WorkplaceProfile.objects.get(workplace=workplace)
            materials = form.cleaned_data.get('materials')
            wp.set_materials(materials)
            return render(request, 'workplace/set_materials.html', {'form': form})
    else:
        return render(request, 'workplace/set_materials.html', {'form': form})


def set_operations(request):
    form = SetOperationForm(request.POST)
    if request.method == 'POST':
        if not form.is_valid():
            print("fuck")
            return redirect('/')
        else:
            user = request.user
            workplace = user.userprofile.primary_workplace
            wp = WorkplaceProfile.objects.get(workplace=workplace)
            operations = form.cleaned_data.get('operations')
            wp.set_operations(operations)
            return render(request, 'workplace/set_operations.html', {'form': form})
    else:
        return render(request, 'workplace/set_operations.html', {'form': form})


def set_assets(request):
    form = SetAssetForm(request.POST)
    if request.method == 'POST':
        if not form.is_valid():
            print("fuck")
            return redirect('/')
        else:
            user = request.user
            workplace = user.userprofile.primary_workplace
            wp = WorkplaceProfile.objects.get(workplace=workplace)
            assets = form.cleaned_data.get('assets')
            wp.set_assets(assets)
            return render(request, 'workplace/set_assets.html', {'form': form})
    else:
        return render(request, 'workplace/set_assets.html', {'form': form})


def set_area(request):
    form = SetMaterialForm(request.POST)
    if request.method == 'POST':
        if not form.is_valid():
            print("fuck")
            return redirect('/')
        else:
            user = request.user
            workplace = user.userprofile.primary_workplace

            area = form.cleaned_data.get('areas')
            workplace.set_materials(area)
            return render(request, 'workplace/set_materials.html')
    else:
        return render(request, 'workplace/set_materials.html', {'form': form})

# def workplace_profile():


# Create your views here.
