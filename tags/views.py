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
    if 'tag' in request.GET:
        t = request.GET['tag']
        # term = request.GET(tag)
        o = Tags.popular.filter(tag__icontains=t)
        # o = Tags.popular.get(name=t)

        return render(request, 'tags/list.html', locals())
    else:
        return render(request, 'tags/list.html')




# Create your views here.
