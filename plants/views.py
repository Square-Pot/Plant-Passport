import random
import string
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.template import loader
from .models import Plant, RichPlant, Log, Attribute, Action
from .forms import PlantForm
from django.utils.translation import gettext as _
from django.utils.translation import activate
from django.utils import translation


def index(request):
    cur_language = translation.get_language()
    activate(cur_language)

    current_user = request.user
    owning_plants = Log.objects.filter(data__owner=current_user.id).values_list('plant', flat=True)
    rich_plants_attrs = []
    rich_plants = []
    for plant_id in owning_plants:
        plant = Plant.objects.filter(id=plant_id)[0]
        rich_plant = RichPlant.new_from(plant)
        rich_plant.get_attrs_values()
        rich_plants.append(rich_plant)
        #values = rich_plant.get().actual_attrs_values()
        # add uid to first place
        #values.insert(0, rich_plant.uid)
        #rich_plants_attrs.append(values)
    #attrs_summary = Attribute.keys.get_all_keys()
    attrs_summary = Attribute.keys.get_all_names()

    #TODO: filter by genus, sp.

    context = {
        #'rp_attrs': rich_plants_attrs, 
        'rich_plants': rich_plants, 
        'attrs_summary': attrs_summary,
        'title': _('MyPlants'),
    }
    template = loader.get_template('plants/index.html')
    return HttpResponse(template.render(context, request))


def plant_view(request, plant_id):
    cur_language = translation.get_language()
    activate(cur_language)

    #current_user = request.user

    plant = Plant.objects.filter(id=plant_id)[0]
    rich_plant = RichPlant.new_from(plant)
    rich_plant.get_attrs_dics()
    #rp_values_dic = rich_plant.attrs_dics()
    attr_names = Attribute.keys.get_all_names()

    #TODO add plant history

    #history = []
    #for log in rich_plant.logs():




    context = {
        'plant': rich_plant,
        #'rp_values': rp_values_dic,
        'attr_names': attr_names,
        'title': _('PlantProfile'),
    }
    template = loader.get_template('plants/view.html')
    return HttpResponse(template.render(context, request))


#def plant_edit(request, plant_id):
    #current_user = request.user
#    return plant_id

#@login_required
def plant_create(request, plant_id=None):
    cur_language = translation.get_language()
    activate(cur_language)
    print('AAAA', plant_id)
    if plant_id:
        plant = get_object_or_404(Plant, id=plant_id)
        #plant = Plant.objects.filter(id=plant_id)[0]
        rich_plant = RichPlant.new_from(plant)
        # if rich_plant.get_owner() != request.user:
        #     return HttpResponseForbidden()
        rich_plant.get_attrs_dics()
        attrs = rich_plant.attrs_dics
    else: 
        attrs = {}

    if request.method == 'POST':
        form = PlantForm(attrs, request.POST)
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
        form = PlantForm(attrs)

    template = loader.get_template('plants/create.html')
    context = {
        'form': form,
        'title': _('AddPlant'),
    }
   
    return HttpResponse(template.render(context, request))


def plant_update(request, plant_id):
    return HttpResponse("Plants here will be")

