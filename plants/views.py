import random
import string
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
from .models import Plant, Attribute, Action
from .forms import PlantForm
from logger.models import Log



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

            # CREATING NEW PLANT
            
            # Create UID
            # TODO: UID generation algorithm may be improved
            while True:
                # Example: '798670'
                random_string = ''.join(random.choices(string.digits, k=6))
                # Check uniqueness
                if Plant.objects.filter(uid=random_string).count() == 0:
                    uid = random_string
                    break
            
            current_user = request.user
            new_plant = Plant(uid=uid, creator=current_user)
            new_plant.save()
            
            # CREATING LOGS 
           
            data = {}
            # owner of plant
            data['owner'] = current_user.id
            # attributes
            for post_key in form.cleaned_data:
                data[post_key] = form.cleaned_data[post_key]

            new_log = Log(
                action_type = 1,
                user = current_user, 
                plant = new_plant, 
                data = data,
            )
            new_log.save()

            return HttpResponse('Saved ok')
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

