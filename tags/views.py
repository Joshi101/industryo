from django.shortcuts import render, redirect
from tags.forms import CreateTagForm
from tags.models import Tags


def create_tag(request):
    form = CreateTagForm(request.POST)
    if request.method == 'POST':
        if not form.is_valid():
            print("form invalid")
            return render(request, 'tags/create.html', {'form': form})
        else:
            tag = form.cleaned_data.get('tag')
            description = form.cleaned_data.get('description')

            t, created = Tags.objects.get_or_create(tag=tag, description=description)
            if not created:
                t.number = 99

            t.save()

            return render(request, 'tags/create.html', {'form': form})
    else:
        return render(request, 'tags/create.html', {'form': CreateTagForm()})


def search_tag(request):
    if request.method == 'GET':
        t = request.GET['the_query']
        create = request.GET['the_create']
        # term = request.GET(tag)
        o = Tags.objects.filter(tag__icontains=t)[:6]
        # o = Tags.objects.get(name=t)

        return render(request, 'tags/list.html', {'o': o, 'create': create})
    else:
        return render(request, 'tags/list.html')




# Create your views here.
