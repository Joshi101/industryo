from django.shortcuts import render, redirect, render_to_response, HttpResponse
from tags.forms import CreateTagForm
from tags.models import Tags
from forum.models import Question
from workplace.models import WpTags
from nodes.models import Node
from nodes.forms import SetTagLogoForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from itertools import chain
from operator import attrgetter


def create_tag(request):
    form = CreateTagForm(request.POST)
    if request.method == 'POST':
        if not form.is_valid():
            return render(request, 'tags/create.html', {'form': form})
        else:
            tag = form.cleaned_data.get('tag')
            description = form.cleaned_data.get('description')

            t, created = Tags.objects.get_or_create(tag=tag, description=description)
            t.count += 1
            t.save()

            return render(request, 'tags/create.html', {'form': form})
    else:
        return render(request, 'tags/create.html', {'form': CreateTagForm()})


def search_tag(request):
    if request.method == 'GET':
        tag = request.GET['the_query']
        type = request.GET['the_type']
        if type == 'All':
            o = Tags.objects.filter(tag__icontains=tag)[:6]
        else:
            o = Tags.objects.filter(type=type, tag__icontains=tag)[:6]
        return render(request, 'tags/list.html', {'objects': o})
    else:
        return render(request, 'tags/list.html')


def search_interests(request):                  # for searching the workplace
    if request.method == 'GET':
        n = request.GET['the_query']
        if len(n) >= 2:
            o = Tags.objects.filter(tag__icontains=n)[:6]
            create = request.GET['the_create']
            return render(request, 'tags/list.html', {'o': o, 'create': create})
        else:
            return HttpResponse('Keep Typing..')
    else:
        return render(request, 'tags/list.html')


def get_tag(request, slug):
    tag = Tags.objects.get(slug=slug)
    questions = Question.objects.filter(tags=tag)

    workplaces = tag.wptags.all()
    nodes = Node.feed.filter(tags=tag)
    articles = Node.article.filter(tags=tag)
    tag_logo_form = SetTagLogoForm()
    wptags = WpTags.objects.filter(tags=tag)
    all_result_list = sorted(
        chain(nodes, questions),
        key=attrgetter('date'), reverse=True)
    paginator = Paginator(all_result_list, 5)
    page = request.GET.get('page')
    try:
        result_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        result_list = paginator.page(1)
    except EmptyPage:
                # If page is out of range (e.g. 9999), deliver last page of results.
        return
                # result_list = paginator.page(paginator.num_pages)
    if page:
        return render(request, 'nodes/five_nodes.html', {'result_list': result_list, 'wptags':wptags})
    else:
        return render(request, 'tags/tag.html', locals())


def get_all_tags(request):
    all_tags = Tags.objects.all()
    paginator = Paginator(all_tags, 5)
    page = request.GET.get('page')
    try:
        tags = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        tags = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        tags = paginator.page(paginator.num_pages)

    return render_to_response('tags/list1.html', {"tags": tags})
    # return render(request, 'tags/list1.html', locals())


def search_n_tags(request):
    tag = request.GET['the_query']
    type = request.GET['the_type']
    o = Tags.objects.filter(type=type, tag__icontains=tag)
    create = request.GET['the_create']
    return render(request, 'tags/list.html', {'o': o, 'create': create})


@login_required
def describe_tag(request):          # edit description
    if request.method == 'POST':
        id = request.POST.get('id')
        tag = Tags.objects.get(id=id)
        description = request.POST['description']
        tag.description = description
        tag.save()
        return HttpResponse()
    else:
        return redirect('/tags/')


# new function to add a follow button to a tag adding it to interests
@login_required
def follow_tag(request):
    user = request.user
    if request.method == 'POST':
        tag = Tags.objects.get(id=request.POST['tag_id'])
        user.useprofile.interest.add(tag)
        return HttpResponse()
    else:
        return redirect('/tags/')


def create(request):
    lis = ['Automotive', 'Aerospace', 'Manufacturing', 'Food processing', 'Power', 'Oil & Gas',
           'Industrial Consultancy', 'Engineering Consultancy', 'Designing', 'Material Testing', 'Repairing & Servicing']
    lia = ['Milling Machine', 'Mig Welding Setup', 'Tig Welding Setup', 'CNC Milling Machine', 'Lathe Machine', 'CNC Lathe Machine',
           'Rotomolding Machine', 'Melting Furnace', 'Knurling Machine', 'Press Brake ', 'CNC Press Brake', 'Slotter', 'Shaper',
           'Drilling Machine', 'Hobbing Machine', 'Honing Machine', 'Special Purpose Machines (SPM)', 'Hydraulic Ram', 'Rolling Mill',
           'Crusher', 'Polymer processing Machine', 'Electric Furnace', 'Gas Furnace', 'Rapid Prototyping Machine',
           'Electrical Discharge Machine (EDM)', 'Water Jet Cutter', 'Laser Beam Machine', 'Earth Moving Equipments', 'Industrial Robots']
    lid = ['FMCG (Consumer Goods)', 'Iron & Steel', 'Aluminium sheet', 'Automobile Components(OEM)', 'Automobile Components',
           'Aerospace Components(OEM)', 'Hydraulic Device', 'Pneumatic Device', 'Polymer Components', 'Rubber Items',
           'Plastic Items', 'Agricultural equipments', 'Machine Tools', 'Cutting Tools', 'Power tools', 'Electric tools',
           'Electrical Equipments', 'Hand Tools', 'Material Handling Equipments', 'Boilers', 'Chemicals', 'Paints & Coatings',
           'Raisins', 'Thinners', 'Adhesives', 'Cutting Fluids', 'Coolants', 'Lubricants', 'Furniture', 'Jigs & Fixtures',
           'Die & Punch', 'Consumer Electronics', 'Tubes & Tyres', 'Fasteners', 'Couplings',
           'Sealants', 'Pipes & Tubes', 'Glass', 'Lean Manufacturing Implementation', 'Six Sigma Implementation', 'Construction Materials']
    lim = ['Alloy Steel', 'Aluminium', 'Mild Steel (MS)', 'Alloy Steel', 'Non Ferrous Metals', 'Glass & Ceramics', 'Copper Alloys',
           'Zinc Alloys', 'Wood ', 'Industrial Chemicals', 'Silicon Compounds',
           'Rubber', 'Polymers', 'Plastic', 'Agricultural Products', 'Gases', 'Ores & Minerals', 'Coal & Petroleum', 'Refractories']
    lio = ['Casting', 'Forging', 'Die Design', 'Welding', 'Lathe Machine Operations', 'Heat Treatment', 'Hobbing',
           'Broaching', 'Scrap processing', 'Molding', 'wire drawing', 'Tyre Retreading', 'Hot Rolling',
           'Cold Rolling', 'CNC Operations', 'Design Consultancy', 'Welding', 'Aluminium Welding', 'Electroplating',
           'Rapid Prototyping', 'Injection Molding', 'CNC Programming', 'Punching & Blanking', 'Sheet Metal Operations',
           'induction hardening', 'Superfinishing Operations', 'Rotomolding', 'Phosphating',
           'Body building & Fabrication', 'Precision Job', 'Electroplating', 'Electroforming', 'Powder coating',
           'Mining & Mineral Processing', 'Operations research', 'High Pressure Die Casting (HPDC)',
           'Low Pressure Die Casting (LPDC)', 'laser Cutting']
    lie = ['Baja SAE India', 'Supra SAE India', 'Baja Student India', 'Formula Student India', 'EffiCycle SAE India',
           'SAE Supermileage']
    for o in lis:
        try:
            t = Tags.objects.get(tag=o)
        except Exception:
            t = Tags.objects.create(tag=o, type='S')
    for o in lia:
        try:
            t = Tags.objects.get(tag=o)
        except Exception:
            t = Tags.objects.create(tag=o, type='A')
    for o in lid:
        try:
            t = Tags.objects.get(tag=o)
        except Exception:
            t = Tags.objects.create(tag=o, type='D')
    for o in lim:
        try:
            t = Tags.objects.get(tag=o)
        except Exception:
            t = Tags.objects.create(tag=o, type='M')
    for o in lio:
        try:
            t = Tags.objects.get(tag=o)
        except Exception:
            t = Tags.objects.create(tag=o, type='O')
    for o in lie:
        try:
            t = Tags.objects.get(tag=o)
        except Exception:
            t = Tags.objects.create(tag=o, type='E')
    return redirect('/')


# Create your views here.
