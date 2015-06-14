from django.shortcuts import render, redirect, HttpResponse
from django.template.loader import render_to_string
from workplace.forms import WorkplaceForm, SetWorkplaceForm, SetTeamTypeForm, SetSegmentForm
from workplace.models import *
from nodes.models import Node
from forum.models import Question, Answer
from nodes.forms import SetLogoForm
from userprofile.models import User, UserProfile
import json
from django.contrib.auth.decorators import login_required


@login_required
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

@login_required
def set_workplace(request):
    if request.method == 'POST':
        form = SetWorkplaceForm(request.POST)
        if not form.is_valid():
            return render(request, 'userprofile/set.html', {'form_set_workplace': form,'form_create_workplace':WorkplaceForm()})
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


@login_required
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


@login_required
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

@login_required
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
