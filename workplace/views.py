from django.shortcuts import render, redirect
from workplace.forms import WorkplaceForm, SetWorkplaceForm
from workplace.models import *
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
            node = Node(user=User.objects.get(pk=3), post=welcome)
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

            welcome = u'{0} has started working in {1}.'.format(user, primary_workplace)
            node = Node(user=User.objects.get(pk=3), post=welcome)
            node.save()
            return redirect('/')
    else:
        return render(request, 'userprofile/set.html', {'form': SetWorkplaceForm()})

        

# Create your views here.
