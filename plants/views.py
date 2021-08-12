import random
import string
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.template import loader
from .models import Plant, RichPlant, Log, Attribute, Action
from .forms import PlantForm, AttributeForm, PhotoForm
from django.utils.translation import gettext as _
from django.utils.translation import activate
from django.utils import translation


def index(request):
    """List of User Plants"""

    # TODO: add ability to view not only my plants, but other users (friends for ex.)

    ## I18N
    # TODO: choose, save and read user setting for current language
    cur_language = translation.get_language()
    activate(cur_language)

    ## DETECT USER
    # TODO: login required friend | owner
    #       can see only my list or friend list anon
    current_user = request.user

    ## GET USER'S RICH PLANTS (WITH FILTERS)
    # TODO: filter by genus, sp.
    #       replace folowing code with service
    #       Pavlick thinks REPOZOTORIY should be used
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

    ## DATA FOR TEMPLATE
    context = {
        #'rp_attrs': rich_plants_attrs, 
        'rich_plants': rich_plants, 
        'attrs_summary': attrs_summary,
        'title': _('MyPlants'),
    }
    template = loader.get_template('plants/index.html')
    return HttpResponse(template.render(context, request))


def plant_view(request, plant_id):
    """Plant Profile with History Timeline"""

    ## I18N
    # TODO: choose, save and read user setting for current language
    cur_language = translation.get_language()
    activate(cur_language)

    ## DETECT USER
    # TODO: anonymous | autorized | fiend | owner
    #current_user = request.user

    ## GET RICH PLANT 
    plant = Plant.objects.filter(id=plant_id)[0]
    rich_plant = RichPlant.new_from(plant)
    rich_plant.get_attrs_dics()
    rich_plant.get_logs()

    ## GET HISTORY
    # TODO add plant history
    # history = []
    # for log in rich_plant.logs():

    ## TODO:  add buttons: 
    #                       - add photo
    #                       - acton 

    ## DATA FOR TEMPLATE
    context = {
        'plant': rich_plant,
        'title': _('PlantProfile'),
    }
    template = loader.get_template('plants/view.html')
    return HttpResponse(template.render(context, request))


def plant_create(request, plant_id=None):
    """Plant Creation"""

    ## I18N
    # TODO: choose, save and read user setting for current language
    cur_language = translation.get_language()
    activate(cur_language)

    ## DETECT USER
    # TODO: anonymous | autorized 
    #       ask authorize if not
    #       check if user has owning rights for plant (with plant_id)

    ## GET RICH PLANT
    # TODO: Why??
    #       there is no need to edit plant!
    if plant_id:
        plant = get_object_or_404(Plant, id=plant_id)
        rich_plant = RichPlant.new_from(plant)
        if rich_plant.get_owner() != request.user: # works?
            return HttpResponseForbidden()
        rich_plant.get_attrs_dics()
        attrs = rich_plant.attrs_dics
    else: 
        attrs = {}

    ## PROCESSING DATA FROM USER
    if request.method == 'POST':
        form = PlantForm(attrs, request.POST)
        if form.is_valid():

            ## CREATING NEW PLANT
            # TODO: replace to services
            
            # Create UID
            # TODO: UID generation algorithm may be improved
            #       should be replaced to services
            while True: 
                # Example: '798670'
                random_string = ''.join(random.choices(string.digits, k=6))
                
                # Check uniqueness
                if Plant.objects.filter(uid=random_string).count() == 0:
                    uid = random_string
                    break
            
            # TODO: fix it: user detection block is above
            current_user = request.user
            new_plant = Plant(uid=uid, creator=current_user)
            new_plant.save()
            
            ### CREATING LOGS 
            # TODO: replace to services
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

            # TODO: fix redirect path
            return HttpResponseRedirect(f'/plants/view/{ new_plant.id }')

    else:
        form = PlantForm(attrs)

    ## DATA FOR TEMPLATE
    template = loader.get_template('plants/create.html')
    context = {
        'form': form,
        'title': _('AddPlant'),
    }
    return HttpResponse(template.render(context, request))


def edit_plant_attr(request, plant_id=None, attr_key=None):
    """Plant Attribute Editing"""

    ## I18N
    # TODO: choose, save and read user setting for current language
    cur_language = translation.get_language()
    activate(cur_language)

    ## DETECT USER
    # TODO: anonymous | autorized 
    #       ask authorize if not
    #       check if user has owning rights for plant (with plant_id)
    current_user = request.user

    ## GET RICH PLANT
    if plant_id and attr_key:
        plant = get_object_or_404(Plant, id=plant_id)
        rich_plant = RichPlant.new_from(plant)
        if rich_plant.get_owner() != request.user.id:
            return HttpResponseForbidden()
        rich_plant.get_attrs_dics()
    else: 
        pass #TODO 404
    
    ## PROCESSING DATA FROM USER
    if request.method == 'POST':
        form = AttributeForm()
        #print(request.POST)

        # TODO: Check:
        #               if current user is owner
        #               if attr key in attrs
        #               is changes actually was made (was value changed?)
        if True:
            new_value = request.POST[attr_key]

            ### CREATING LOGS 
            # TODO: replace to services
            new_log = Log(
                action_type = 2,  # changed
                user = current_user, 
                plant = Plant.objects.filter(id=plant_id)[0], 
                data = {attr_key: new_value},
            )
            new_log.save()

        # TODO: fix path
        return HttpResponseRedirect(f'/plants/view/{ plant_id }')

    else:
        value = rich_plant.attrs_dics[attr_key]
        label = Attribute.objects.filter(key=attr_key)[0].name
        form = AttributeForm(label, attr_key, value)

    ## DATA FOR TEMPLATE
    template = loader.get_template('plants/edit_attr.html')
    context = {
        'attr_key': attr_key,
        'plant_id': plant_id,
        'form': form,
        'title': _('EditAttr'),
    }
    return HttpResponse(template.render(context, request))

def upload_photo(request, plant_id):
    """Photo Uploading"""

    ## I18N
    # TODO: choose, save and read user setting for current language
    cur_language = translation.get_language()
    activate(cur_language)

    ## DETECT USER
    # TODO: anonymous | autorized 
    #       ask authorize if not
    #       check if user has owning rights for plant (with plant_id)
    #current_user = request.user

    ## PROCESSING DATA FROM USER
    if request.method == 'POST':
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # TODO: fix url
            #return reverse('plant_view', kwargs={'plant_id': plant_id})
            return HttpResponseRedirect(f'/plants/view/{ plant_id }')

            ### CREATING LOGS 
            # TODO: replace to services
            #       create new log
    else:
        form = PhotoForm()

    ## DATA FOR TEMPLATE
    template = loader.get_template('plants/upload_photo.html')
    context = {
        'form': form,
        'plant_id': plant_id,
        'title': _('UploadPhoto'),
    }
    return HttpResponse(template.render(context, request))


