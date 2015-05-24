from django.shortcuts import render, redirect
from workplace.forms import WorkplaceForm, SetWorkplaceForm, SetTeamTypeForm, SetSegmentForm
from workplace.models import *
from workplaceprofile.models import WorkplaceProfile
from nodes.models import *
from userprofile.models import *


def workplace_register(request):
    form = WorkplaceForm(request.POST)
    if request.method == 'POST':
        if not form.is_valid():
            print("form invalid")
            return render(request, 'workplace/register.html', {'form': form})
        else:
            name = form.cleaned_data.get('name')
            workplace_type = form.cleaned_data.get('workplace_type')
            Workplace.objects.create(name=name, workplace_type=workplace_type)

            welcome = u'{0} is now in the network, have a look at its profile.'.format(name)
            node = Node(user=User.objects.get(pk=1), post=welcome)
            node.save()
            return redirect('/')
    else:
        return render(request, 'workplace/register.html', {'form': WorkplaceForm()})


def set_workplace(request):
    form = SetWorkplaceForm(request.POST)
    if request.method == 'POST':
        if not form.is_valid():
            print("form invalid")
            return render(request, 'userprofile/set.html', {'form': form})
        else:
            user = request.user
            primary_workplace = form.cleaned_data.get('primary_workplace')
            job_position = form.cleaned_data.get('job_position')
            userprofile = UserProfile.objects.get(user=user)
            userprofile.primary_workplace = primary_workplace
            userprofile.job_position = job_position
            userprofile.save()

            t = userprofile.primary_workplace.workplace_type

            welcome = u'{0} has started working in {1}.'.format(user, primary_workplace)
            node = Node(user=User.objects.get(pk=1), post=welcome)   #, tags=t
            node.save()
            return redirect('/')
    else:
        return render(request, 'userprofile/set.html', {'form': SetWorkplaceForm()})


def search_workplace(request):                  # for searching the workplace
    if request.method == 'GET':
        w = request.GET['the_query']
        o = Workplace.objects.filter(name__icontains=w)
        create = request.GET['the_create']
        return render(request, 'tags/list.html', {'o': o, 'create': create})
    else:
        return render(request, 'tags/list.html')


def workplace_profile(request, slug):
    o = Workplace.objects.get(slug=slug)
    profile = WorkplaceProfile.objects.get(workplace=o.id)
    return render(request, 'workplace_profile/profile.html', locals())


def set_segment(request):
    type = request.user.userprofile.primary_workplace.workplace_type
    if type=='C':
        form = SetTeamTypeForm(request.POST)
        if request.method == 'POST':

            if not form.is_valid():
                print("form invalid")
                return render(request, 'workplace/set_segment.html', {'form': form})
            else:
                segments = form.cleaned_data.get('segments')
                workplace = request.user.userprofile.primary_workplace
                for segment in segments:
                    SegmentTags.objects.get_or_create(segment=segment, workplace=workplace)
            return render(request, 'workplace/set_segment.html', {'form': form})
        else:
            return render(request, 'workplace/set_segment.html', {'form': form})
    else:
        form = SetSegmentForm(request.POST)
        if request.method == 'POST':
            if not form.is_valid():
                print("form invalid")
                return render(request, 'workplace/set_segment.html', {'form': form})
            else:
                segments = form.cleaned_data.get('segments')
                workplace = request.user.userprofile.primary_workplace
                for segment in segments:
                    SegmentTags.objects.get_or_create(segment=segment, workplace=workplace)
            return render(request, 'workplace/set_segment.html', {'form': form})
        else:
            return render(request, 'workplace/set_segment.html', {'form': form})


def search_segment(request):
    if request.method == 'GET':
        t = request.GET['the_query']
        create = request.GET['the_create']
        o = Segment.objects.filter(tag__icontains=t)[:6]

        return render(request, 'tags/list.html', {'o': o, 'create': create})
    else:
        return render(request, 'tags/list.html')







        

# Create your views here.
