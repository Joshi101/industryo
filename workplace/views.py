from django.shortcuts import render, redirect, HttpResponse
from django.template.loader import render_to_string
from workplace.forms import WorkplaceForm, SetWorkplaceForm, SetTeamTypeForm, SetSegmentForm
from workplace.models import *
from nodes.models import Node
from forum.models import Question, Answer
from nodes.forms import SetLogoForm
from userprofile.models import User, UserProfile
import json


def workplace_register(request):
    form = WorkplaceForm(request.POST)
    if request.method == 'POST':
        response = {}
        r_value = {}
        r_inputs = []
        r_html = {}
        r_elements = []
        if not form.is_valid():
            #do some error handling
            return HttpResponse(json.dumps(response), content_type="application/json")
        else:
            name = form.cleaned_data.get('name')
            workplace_type = form.cleaned_data.get('workplace_type')
            t, created = Workplace.objects.get_or_create(name=name, workplace_type=workplace_type)
            if created:
                welcome = u'{0} is now in the network, have a look at its profile.'.format(name)
                node = Node(user=User.objects.get(pk=1), post=welcome)
                node.save()
                r_elements = ['message']
                r_html['message'] = render_to_string('snippets/create_wp_alert.html', {'name':name})
            r_inputs = ['id_workplace']
            r_value['id_workplace'] = name
            response['html'] = r_html
            response['elements'] = r_elements
            response['value'] = r_value
            response['inputs'] = r_inputs
            return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        return redirect('/set/')


def set_workplace(request):
    form = SetWorkplaceForm(request.POST)
    form_2 = WorkplaceForm(request.POST)
    if request.method == 'POST':
        if not form.is_valid():
            return render(request, 'userprofile/set.html', {'form_set_workplace': form,'form_create_workplace':form_2})
        else:
            user = request.user
            workplace = form.cleaned_data.get('workplace')
            primary_workplace = Workplace.objects.get(name=workplace)
            job_position = form.cleaned_data.get('job_position')
            userprofile = UserProfile.objects.get(user=user)
            userprofile.primary_workplace = primary_workplace
            userprofile.job_position = job_position
            userprofile.save()
            t = userprofile.primary_workplace.workplace_type

            welcome = u'{0} has started working in {1}.'.format(user, primary_workplace)
            node = Node(user=User.objects.get(pk=1), post=welcome)   #, tags=t
            node.save()
            if user.first_name:
                return redirect('/')
            else:
                return redirect('/details/')
    else:
        return render(request, 'userprofile/set.html', {'form_set_workplace': SetWorkplaceForm(), 'form_create_workplace': WorkplaceForm()})


def search_workplace(request):                  # for searching the workplace
    if request.method == 'GET':
        w = request.GET['the_query']
        o = Workplace.objects.filter(name__icontains=w)
        create = request.GET['the_create']
        return render(request, 'tags/list.html', {'o': o, 'create': create})
    else:
        return render(request, 'tags/list.html')

#
# def search_segment(request):
#     if request.method == 'GET':
#         t = request.GET['the_query']
#         create = request.GET['the_create']
#         o = Segment.objects.filter(tag__icontains=t)[:6]
#
#         return render(request, 'tags/list.html', {'o': o, 'create': create})
#     else:
#         return render(request, 'tags/list.html')

## best way to create workplace profile: send informations in different segments as different functions

#
# def workplace_profile(request, slug):
#     o = Workplace.objects.get(slug=slug)
#     members = UserProfile.objects.filter(primary_workplace=o.id).order_by('-points')
#     return render(request, 'workplace_profile/profile.html', locals())
#
#
# def edit_workplace_profile(request):
#     w = request.user.userprofile.primary_workplace
#     type = w.workplace_type
#     if type == 'C':
#         form = EditTeamForm(request.POST, request.FILES)
#         if request.method == 'POST':
#             if not form.is_valid():
#                 print("fuck")
#                 return render(request, 'workplace/set_segment.html', {'form': form})
#             else:
#                 city = form.cleaned_data.get('city')
#                 address = form.cleaned_data.get('address')
#                 contact = form.cleaned_data.get('contact')
#                 about = form.cleaned_data.get('about')
#                 institution_name = form.cleaned_data.get('institution_name')
#                 parti = form.cleaned_data.get('participation')
#                 logo = form.cleaned_data.get('logo')
#
#                 area, created = Area.objects.get_or_create(name=city)
#                 institution, created = Institution.objects.get_or_create(name=institution_name, area=area)
#
#                 wp = WorkplaceProfile.objects.get(workplace=w)
#                 wp.area = area   # get or create models
#                 wp.address = address
#                 wp.contact = contact
#                 wp.about = about
#                 wp.institution = institution   # get or create on models
#                 wp.create_participation(parti)
#                 user = request.user
#                 wp.set_logo(image=logo, user=user)
#                 # wp.set_logo(logo, user)
#
#                 wp.save()
#
#             return render(request, 'workplace_profile/edit.html', {'form': form})
#         else:
#             return render(request, 'workplace_profile/edit.html', {'form': form})
#
#     elif type == 'B':
#         form = EditSMEForm(request.POST)
#         if request.method == 'POST':
#             if not form.is_valid():
#                 print("fuck")
#                 return render(request, 'workplace/set_segment.html', {'form': form})
#             else:
#                 city = form.cleaned_data.get('city')
#                 address = form.cleaned_data.get('address')
#                 contact = form.cleaned_data.get('contact')
#                 about = form.cleaned_data.get('about')
#                 materials = form.cleaned_data.get('materials')
#                 assets = form.cleaned_data.get('assets')
#                 operations = form.cleaned_data.get('operations')
#                 product_details = form.cleaned_data.get('product_details')
#                 capabilities = form.cleaned_data.get('capabilities')
#
#                 area, created = Area.objects.get_or_create(name=city)
#
#                 wp = WorkplaceProfile.objects.get(workplace=w)
#                 wp.area = area
#                 wp.address = address
#                 wp.contact = contact
#                 wp.about = about
#                 wp.product_details = product_details
#                 wp.capabilities = capabilities
#
#                 wp.set_materials(materials)
#                 wp.set_assets(assets)
#                 wp.set_operations(operations)
#
#                 wp.save()
#
#             return render(request, 'workplace_profile/edit.html', {'form': form})
#         else:
#             return render(request, 'workplace_profile/edit.html', {'form': form})


# @login_required
def set_tags(request):
    if request.method == 'POST':
        response = {}
        r_html = {}
        r_elements = []
        user = request.user
        wp = user.userprofile.primary_workplace
        assets = request.POST.get('asset')
        operations = request.POST.get('operation')
        materials = request.POST.get('material')
        industrial_area = request.POST.get('industrial_area')
        city = request.POST.get('city')
        institution = request.POST.get('institution')
        events = request.POST.get('event')
        if assets:
            t = wp.set_assets(assets)
        if materials:
            t = wp.set_materials(materials)
        if operations:
            t = wp.set_operations(operations)
        if industrial_area:
            t = wp.set_industrial_area(industrial_area)
        if city:
            t = wp.set_city(city)
        if institution:
            t = wp.set_institution(institution)
        if events:
            t = wp.set_events(events)
        new_interest = t
        r_elements = ['detail_body']
        r_html['detail_body'] = render_to_string('snippets/one_interest.html', {'interest': new_interest})
        response['html'] = r_html
        response['elements'] = r_elements
        response['prepend'] = True
        return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        return redirect('/user/'+request.user.username)


def workplace_profile(request, slug):
    workplace = Workplace.objects.get(slug=slug)
    members = UserProfile.objects.filter(primary_workplace=workplace.id).order_by('-points')
    workplace_logo_form = SetLogoForm()
    questions = Question.objects.filter(user__userprofile__primary_workplace=workplace)
    answers = Answer.objects.filter(user__userprofile__primary_workplace=workplace)
    feeds = Node.feed.filter(user__userprofile__primary_workplace=workplace)
    articles = Node.article.filter(user__userprofile__primary_workplace=workplace)
    return render(request, 'workplace/profile.html', locals())

# def edit_workplace_profile(request):
#     w = request.user.userprofile.primary_workplace
#     type = w.workplace_type
#     if type == 'A':
#         form = EditTeamForm(request.POST, request.FILES)
#         if request.method == 'POST':
#             if not form.is_valid():
#                 print("fuck")
#                 return render(request, 'workplace/set_segment.html', {'form': form})
#             else:
#                 city = form.cleaned_data.get('city')
#                 address = form.cleaned_data.get('address')
#                 contact = form.cleaned_data.get('contact')
#                 about = form.cleaned_data.get('about')
#                 institution_name = form.cleaned_data.get('institution_name')
#                 parti = form.cleaned_data.get('participation')
#                 logo = form.cleaned_data.get('logo')
#
#                 area, created = Area.objects.get_or_create(name=city)
#                 institution, created = Institution.objects.get_or_create(name=institution_name, area=area)
#
#                 wp = WorkplaceProfile.objects.get(workplace=w)
#                 wp.area = area   # get or create models
#                 wp.address = address
#                 wp.contact = contact
#                 wp.about = about
#                 wp.institution = institution   # get or create on models
#                 wp.create_participation(parti)
#                 user = request.user
#                 wp.set_logo(image=logo, user=user)
#                 # wp.set_logo(logo, user)
#
#                 wp.save()
#
#             return render(request, 'workplace_profile/edit.html', {'form': form})
#         else:
#             return render(request, 'workplace_profile/edit.html', {'form': form})
#
#     elif type == 'B':
#         form = EditSMEForm(request.POST)
#         if request.method == 'POST':
#             if not form.is_valid():
#                 print("fuck")
#                 return render(request, 'workplace/set_segment.html', {'form': form})
#             else:
#                 city = form.cleaned_data.get('city')
#                 address = form.cleaned_data.get('address')
#                 contact = form.cleaned_data.get('contact')
#                 about = form.cleaned_data.get('about')
#                 materials = form.cleaned_data.get('materials')
#                 assets = form.cleaned_data.get('assets')
#                 operations = form.cleaned_data.get('operations')
#                 product_details = form.cleaned_data.get('product_details')
#                 capabilities = form.cleaned_data.get('capabilities')
#
#                 area, created = Area.objects.get_or_create(name=city)
#
#                 wp = WorkplaceProfile.objects.get(workplace=w)
#                 wp.area = area
#                 wp.address = address
#                 wp.contact = contact
#                 wp.about = about
#                 wp.product_details = product_details
#                 wp.capabilities = capabilities
#
#                 wp.set_materials(materials)
#                 wp.set_assets(assets)
#                 wp.set_operations(operations)
#
#                 wp.save()
#
#             return render(request, 'workplace_profile/edit.html', {'form': form})
#         else:
#             return render(request, 'workplace_profile/edit.html', {'form': form})


def set_about(request):
    user = request.user
    wp = user.userprofile.primary_workplace
    if request.method == 'POST':
        response = {}
        about = request.POST.get('about')
        wp.about = about
        wp.save()
        w = user.userprofile.primary_workplace
        return HttpResponse()
    else:
        return redirect('/workplace/'+wp.slug)


def set_capabilities(request):
    user = request.user
    wp = user.userprofile.primary_workplace
    if request.method == 'POST':
        print("DSSDF")
        response = {}

        capabilities = request.POST.get('capabilities')
        # print('post aaya')
        wp.about = capabilities
        # print('save aaya')
        wp.save()
        # print('save ho gaya')
        return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        return redirect('/workplace/'+wp.slug)


def set_product_details(request):
    user = request.user
    wp = user.userprofile.primary_workplace
    if request.method == 'POST':
        print("DSSDF")
        response = {}

        product_details = request.POST.get('product_details')
        # print('post aaya')
        wp.product_details = product_details
        # print('save aaya')
        wp.save()
        # print('save ho gaya')
        return HttpResponse(json.dumps(response), content_type="application/json")
    else:
        return redirect('/workplace/'+wp.slug)

# def set_logo(request):
#     if request.method == 'POST':

        

# Create your views here.
