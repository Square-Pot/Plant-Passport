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

    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = PlantForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
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

