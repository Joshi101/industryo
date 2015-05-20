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
    if 'q' in request.GET:
        term = request.GET('q')
        o = Tags.objects.filter(name__icontains=term)

        return o




# Create your views here.
