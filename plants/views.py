import random
import string
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
from .models import Plant, RichPlant, Log, Attribute, Action
from .forms import PlantForm


def index(request):
    current_user = request.user
    owning_plants = Log.objects.filter(data__owner=current_user.id).values_list('plant', flat=True)
    rich_plants_attrs = []
    for plant_id in owning_plants:
        plant = Plant.objects.filter(id=plant_id)[0]
        rich_plant = RichPlant.new_from(plant)
        values = rich_plant.get().actual_attrs_values()
        # add uid to first place
        values.insert(0, rich_plant.uid)
        rich_plants_attrs.append(values)
    attrs_summary = Attribute.keys.get_all_keys()

    context = {
        'rp_attrs': rich_plants_attrs, 
        'attrs_summary': attrs_summary,
        'title': 'Мои растения',
    }
    template = loader.get_template('plants/index.html')
    return HttpResponse(template.render(context, request))


def plant_view(request, plant_id):
    #current_user = request.user

    plant = Plant.objects.filter(id=plant_id)[0]
    rich_plant = RichPlant.new_from(plant)
    rp_values_dic = rich_plant.get().actual_attrs()
    attr_names = Attribute.keys.get_all_keys()

    #TODO добавить историю 

    context = {
        'plant': rich_plant,
        'rp_values': rp_values_dic,
        'attr_names': attr_names,
        'title': 'Профиль растения',
    }
    template = loader.get_template('plants/view.html')
    return HttpResponse(template.render(context, request))


def plant_edit(request, plant_id):
    #current_user = request.user
    return plant_id


def plant_create(request):
    if request.method == 'POST':
        print(request.POST)
        form = PlantForm(request.POST)
        if form.is_valid():

            ### CREATING NEW PLANT
            
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
            
            ### CREATING LOGS 
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

            return HttpResponseRedirect(f'/plants/view/{ new_plant.id }')

    else:
        form = PlantForm()

    template = loader.get_template('plants/create.html')
    context = {
        'form': form,
        'title': 'Добавить растение',
    }
   
    return HttpResponse(template.render(context, request))


def plant_update(request, plant_id):
    return HttpResponse("Plants here will be")

