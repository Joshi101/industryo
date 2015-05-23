from django.shortcuts import render
from workplace.models import Workplace
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







# Create your views here.
