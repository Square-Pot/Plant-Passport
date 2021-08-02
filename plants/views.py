import random
import string
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import loader
from .models import Plant, Attribute, Action
from .forms import PlantForm
from logger.models import Log


class RichPlant:
    """
    Class, based on Plant-class, enriched with attributes
    """
    def __init__(self, plant: Plant, attrs: dict, required_keys: list, placeholder: str):
        self.uid = plant.uid
        self.creation_date = plant.creation_date
        self.creator = plant.creator
        self.is_deleted = plant.is_deleted
        self.required_keys = required_keys
        self.placeholder = placeholder
        self.attrs = attrs
        self.owner = None
        self.attrs_as_dic = {}
        self.attrs_values = ()

    def add_attrs(self):
        for key in self.required_keys:
            if key in self.attrs:
                if key == 'owner':
                    self.owner = self.attrs[key]
                else:
                    self.attrs_as_dic[key] = self.attrs[key]
                    self.attrs_values += (self.attrs[key],)
            else: 
                self.attrs_as_dic[key] = self.placeholder
                self.attrs_values += (self.placeholder,)


    def get_attrs_as_dic(self) -> dict:
        return self.attrs_as_dic

    def get_attrs_values(self) -> tuple:
        return self.attrs_values


def index(request):
    current_user = request.user

    # Get owning plant from logs TODO: need to review this algorithm
    logs_with_owning = Log.objects.filter(data__owner = current_user.id)
    owning_plants = []
    for log in logs_with_owning:
        owning_plants.append(log.plant)
    
    # Get actual attributes for plants
    plants_attrs = []
    for plant in owning_plants:

        # get all logs for plant
        logs_for_plant = Log.objects.filter(plant=plant)

        # playback logs for plant
        plant_attrs = {}
        for log in logs_for_plant:
            for key in log.data:
                plant_attrs[key] = log.data[key]
        plants_attrs.append([plant, plant_attrs])

    # Get summary list of attributes
    attrs_summary = []
    for plant, attrs in plants_attrs:
        for key in attrs: 
            if key != 'owner' and key not in attrs_summary:
                attrs_summary.append(key)

    # Enrichments plants
    rich_plants = []
    placeholder = '-'
    for plant, attrs in plants_attrs:
        rich_plant = RichPlant(plant, attrs, attrs_summary, placeholder)
        rich_plant.add_attrs()
        rich_plants.append(rich_plant)


    template = loader.get_template('plants/index.html')
    context = {
        'rich_plants': rich_plants, 
        'attrs_summary': attrs_summary,
        'title': 'Мои растения',
    }
    return HttpResponse(template.render(context, request))


def plant_view(request, plant_id):
    return HttpResponse("Plants here will be")


def plant_create(request):
    attributes = Attribute.objects.all()

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

            return HttpResponse('Saved ok')
            #return HttpResponseRedirect('/view/')

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

