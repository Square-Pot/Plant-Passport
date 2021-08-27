import random
import string
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.template import loader
from django.utils.translation import gettext as _
from django.utils.translation import activate
from django.utils import translation
from django.contrib.auth import authenticate, login
from django.core.exceptions import PermissionDenied
from users.forms import UserCreateForm
from users.models import User
from .models import Plant, Log, Attribute #, Action, RichPlant
from .forms import PlantForm, AttributeForm, PhotoForm
from .services import get_user_richplants, get_attrs_titles_with_transl,\
    check_is_user_friend_of_plant_owner, check_is_user_owner_of_plant,\
    get_filteraible_attr_values, get_filtered_attr_values_from_post, filter_data_update,\
    filter_plants, get_attr_keys_not_showing_in_list, create_log
from users.services import is_friend
from .entities import RichPlant, BrCr


# https://docs.djangoproject.com/en/3.2/topics/auth/default/#the-login-required-decorator
from django.contrib.auth.decorators import login_required


def index(request, user_id=None):
    """List of User/Someones Plants"""

    # get filter data recieved from POST
    post_filter_data = False
    if request.method == 'POST':
        post_filter_data = get_filtered_attr_values_from_post(request.POST)
    
    # Breadcrumbs data
    brcr = BrCr()

    # Show personal plants
    if not user_id: 
        # authenticated
        current_user = request.user
        if current_user.is_authenticated:
            user_id = current_user.id
            rich_plants = get_user_richplants(user_id)
            # Translators: Section name
            section_name = _('MyPlants')
            user_name = current_user.username
            is_owner = True
            brcr.add_level(True, '', section_name)
        # anonymous
        else:
            return redirect('login')

    # Show someone's plants
    else:
        target_user = get_object_or_404(User, id=user_id)
        current_user = request.user
        # for friend
        if current_user.is_authenticated and is_friend(current_user, target_user):
            access = [Plant.AccessTypeChoices.PUBLIC, Plant.AccessTypeChoices.FRIENDS]
            rich_plants = get_user_richplants(user_id, access)
        # for anonymous
        else:
            access = [Plant.AccessTypeChoices.PUBLIC,]
            rich_plants = get_user_richplants(user_id, access)
        section_name = _('PlantsOfUser') 
        user_name = target_user.username
        is_owner = False
        brcr.add_level(True, '', f'{section_name}: {user_name}')
        
    # Attribute titles
    attrs_titles_with_transl = get_attrs_titles_with_transl()
    
    # Not showing attribute keys
    attrs_not_showing = get_attr_keys_not_showing_in_list()
    print(attrs_not_showing)

    # Filter
    filter_data = get_filteraible_attr_values(rich_plants)
    if post_filter_data: 
        filter_data = filter_data_update(filter_data, post_filter_data)
        rich_plants = filter_plants(rich_plants, post_filter_data)

    # Template data
    context = {
        'rich_plants': rich_plants, 
        'attrs_titles': attrs_titles_with_transl,
        'attrs_not_showing': attrs_not_showing,
        #'title': _('ListOfPlants'),
        'section_name': section_name,
        'user_name': user_name,
        'is_owner': is_owner,
        'brcr_data': brcr.data,
        'filter_attrs': filter_data,
    }
    template = loader.get_template('plants/index.html')
    return HttpResponse(template.render(context, request))


def plant_view(request, plant_id):
    """Plant Profile with History Timeline"""

    # try to get plant by id
    target_plant = get_object_or_404(Plant, id=plant_id)
    if target_plant:
        plant_access = target_plant.access_type
        target_rich_plant = RichPlant(target_plant)

        # authenticated
        current_user = request.user
        if current_user.is_authenticated: 
            user_is_owner = check_is_user_owner_of_plant(current_user, target_rich_plant)
            user_is_friend = check_is_user_friend_of_plant_owner(current_user, target_rich_plant)
            is_owner = user_is_owner

            # plant is public
            if plant_access == Plant.AccessTypeChoices.PUBLIC:
                rich_plant = target_rich_plant

            # plant is friends only
            elif plant_access == Plant.AccessTypeChoices.FRIENDS and (user_is_friend or user_is_owner):
                rich_plant = target_rich_plant

            # plant is privat
            elif plant_access == Plant.AccessTypeChoices.PRIVATE and user_is_owner:
                rich_plant = target_rich_plant
                
            else:
                raise PermissionDenied
        
        # anonymous
        else:
            is_owner = False
            
            # plant is public
            if plant_access == Plant.AccessTypeChoices.PUBLIC:
                rich_plant = target_rich_plant
            else:
                raise PermissionDenied

        # User name
        user_name = current_user.username
        owners_name = rich_plant.get_owners_name()

        # Breadcrubms
        brcr = BrCr()
        if is_owner:
            section_name = _('MyPlant')
            brcr.add_level(False, 'plants', section_name)
        else:
            section_name = _('PlantOfUser')
            brcr.add_level(False, 'plants', f'{section_name} {owners_name}')
        brcr.add_level(True, '', rich_plant.fancy_name)

        ## GET HISTORY
        # TODO add plant history
        # history = []
        # for log in rich_plant.logs():

        ## TODO:  add buttons: 
        #                       - add photo
        #                       - acton 

        # Template data
        context = {
            'plant': rich_plant,
            'section_name': section_name,
            'user_name': user_name,
            'is_owner': is_owner,
            'brcr_data': brcr.data,
        }
        template = loader.get_template('plants/view.html')
        return HttpResponse(template.render(context, request))


@login_required
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
        form = PlantForm()

    ## DATA FOR TEMPLATE
    template = loader.get_template('plants/create.html')
    context = {
        'form': form,
        'title': _('AddPlant'),
    }
    return HttpResponse(template.render(context, request))

@login_required
def edit_plant_attr(request, plant_id=None, attr_key=None):
    """Plant Attribute Editing"""

    # check authentication 
    current_user = request.user
    if not current_user.is_authenticated:
        return HttpResponseForbidden()

    # try to get plant by id
    target_plant = get_object_or_404(Plant, id=plant_id)
    target_rich_plant = RichPlant(target_plant)
    
    # check access (is owner?)
    user_is_owner = check_is_user_owner_of_plant(current_user, target_rich_plant)
    if not user_is_owner:
        return HttpResponseForbidden()
    
    # processing user data
    if request.method == 'POST':

        # check if attr key exist
        if attr_key in Attribute.keys.get_all_keys():
            new_value = request.POST[attr_key]

            # create log
            create_log(
                Log.ActionChoices.CHANGE,
                current_user,
                target_plant,
                {attr_key: new_value},
            )
        return redirect('plant_view', plant_id=plant_id)

    else:
        value = target_rich_plant.attrs_as_dic[attr_key]
        attr = Attribute.objects.get(key=attr_key)
        label = attr.name
        max_length = attr.max_text_length 
        type = attr.value_type
        form = AttributeForm(label, attr_key, value, max_length, type)

    # Template data
    template = loader.get_template('plants/edit_attr.html')
    context = {
        'attr_key': attr_key,
        'plant_id': plant_id,
        'form': form,
        'title': _('EditAttr'),
    }
    return HttpResponse(template.render(context, request))

@login_required
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




