from django.shortcuts import render
from workplaceprofile.models import *
from workplaceprofile.forms import *


def edit_workplace_profile(request):
    w = request.user.userprofile.primary_workplace
    type = w.workplace_type
    if type == 'C':
        form = EditTeamForm(request.POST)
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

                area, created = Area.objects.get_or_create(name=city)
                institution, created = Institution.objects.get_or_create(name=institution_name, area=area)

                wp = WorkplaceProfile.objects.get(workplace=w)
                wp.area = area   # get or create models
                wp.address = address
                wp.contact = contact
                wp.about = about
                wp.institution = institution   # get or create on models
                wp.create_participation(parti)
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
        o = Asset.objects.filter(tag__icontains=t)[:6]

        return render(request, 'workplace/list.html', {'o': o, 'create': create})
    else:
        return render(request, 'workplace/list.html')


def search_operation(request):
    if 'the_query' in request.GET:
        t = request.GET['the_query']
        create = request.GET['the_create']
        o = Operation.objects.filter(tag__icontains=t)[:6]

        return render(request, 'tags/list.html', {'o': o, 'create': create})
    else:
        return render(request, 'tags/list.html')


def search_material(request):
    if 'the_query' in request.GET:
        t = request.GET['the_query']
        create = request.GET['the_create']
        o = Material.objects.filter(tag__icontains=t)[:6]

        return render(request, 'tags/list.html', {'o': o, 'create': create})
    else:
        return render(request, 'tags/list.html')




# Create your views here.
