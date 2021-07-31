from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
from .models import Plant, Attribute, Action
from .forms import PlantForm

def index(request):
    return HttpResponse("Plants here will be")


def plant_view(request, plant_id):
    return HttpResponse("Plants here will be")


def plant_create(request):
    attributes = Attribute.objects.all()
    template = loader.get_template('plants/create.html')

    if request.method == 'POST':
        print(request.POST)
        form = PlantForm(request.POST)
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponse(type(form.cleaned_data))
            #return HttpResponseRedirect('/view/')
            #return HttpResponseRedirect('/view/')

    else:
        form = PlantForm()

    context = {
        'attributes': attributes,
        'form': form,
    }

    return HttpResponse(template.render(context, request))
    #return render(request, 'name.html', {'form': form})



def plant_update(request, plant_id):
    return HttpResponse("Plants here will be")

