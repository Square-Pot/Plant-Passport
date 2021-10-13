from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.template import loader
from django.utils.translation import gettext as _
from django.utils.translation import activate
from django.utils import translation
from django.contrib.auth import authenticate, login
from django.core.exceptions import PermissionDenied
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from users.forms import UserCreateForm
from users.models import User
from .models import Plant, Log, Attribute, Action, Photo, user_directory_path
from .forms import PlantForm, AttributeForm, ActionForm, PhotoForm
from .services import   get_user_richplants, \
                        get_attrs_titles_with_transl, \
                        check_is_user_friend_of_plant_owner, \
                        check_is_user_owner_of_plant, \
                        get_filteraible_attr_values, \
                        get_filtered_attr_values_from_post, \
                        filter_data_update,\
                        filter_plants, get_attr_keys_not_showing_in_list, \
                        create_log, create_new_plant
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
def plant_create(request):
    """Plant Creation"""

    # authenticated
    current_user = request.user
    # if not current_user.is_authenticated:
    #     raise PermissionDenied

    # processing user data
    if request.method == 'POST':
        form = PlantForm(request.POST)
        if form.is_valid():

            # create new plant
            new_plant = create_new_plant(current_user)

            # collect data
            data = {}
            data['owner'] = current_user.id
            for post_key in form.cleaned_data:
                data[post_key] = form.cleaned_data[post_key]

            # create log
            create_log(
                Log.ActionChoices.ADDITION,
                current_user,
                new_plant,
                data
            )
            return redirect('plant_view', plant_id=new_plant.id)
    else:
        form = PlantForm()

    # Template data
    template = loader.get_template('plants/create.html')
    context = {
        'form': form,
        'title': _('AddPlant'),
    }
    return HttpResponse(template.render(context, request))


@login_required
def edit_plant_attr(request, plant_id=None, attr_key=None):
    """Plant Attribute Editing"""

    #TODO add plant fancy name on the page where attr is editing

    # check authentication 
    current_user = request.user
    # if not current_user.is_authenticated:
    #     return HttpResponseForbidden()

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
def add_plant_action(request, plant_id, action_key):

    #TODO plant_id could be list (for group action)?

    # authenticated
    current_user = request.user
    # if not current_user.is_authenticated:
    #     raise PermissionDenied

    # try to get plant by id
    target_plant = get_object_or_404(Plant, id=plant_id)
    target_rich_plant = RichPlant(target_plant)

    # try to get action by key
    action = get_object_or_404(Action, key=action_key)

    # check access (is owner?)
    user_is_owner = check_is_user_owner_of_plant(current_user, target_rich_plant)
    if not user_is_owner:
        return HttpResponseForbidden()

     # processing user data
    if request.method == 'POST':

        # check if attr key exist
        if action_key in Action.keys.get_all_keys():
            # get comment
            comment = request.POST['comment']

            data = {
                'action': action_key,
                'comment': comment,
            }

            # create log
            create_log(
                Log.ActionChoices.ADDITION,
                current_user,
                target_plant,
                data
            )

            # process related attributes if they recieved
            related_attr_data = {}

            for attr_key in Attribute.keys.get_all_keys():
                if attr_key in request.POST:
                    related_attr_data[attr_key] = request.POST[attr_key]

            if related_attr_data:

                # create log
                create_log(
                    Log.ActionChoices.CHANGE,
                    current_user,
                    target_plant,
                    related_attr_data
                )
            
            return redirect('plant_view', plant_id=plant_id)

        else:
            raise PermissionDenied

    elif not action.comment_option:
        
            # create log
            create_log(
                Log.ActionChoices.ADDITION,
                current_user,
                target_plant,
                {'action': action_key}
            )
            
            return redirect('plant_view', plant_id=plant_id)

    else:
        form = ActionForm(action, target_rich_plant)

    # Template data
    template = loader.get_template('plants/add_action.html')
    context = {
        'action': action,
        'plant': target_rich_plant,
        'form': form,
        'watering_action_name': 'watering',
        'fertilizing_action_name': 'fertilizing',

    }
    return HttpResponse(template.render(context, request))


@login_required
def upload_photo(request, plant_id):
    """Photo Uploading"""

    # authentication
    current_user = request.user

    # try to get plant by id
    target_plant = get_object_or_404(Plant, id=plant_id)
    target_rich_plant = RichPlant(target_plant)

    # check access (is owner?)
    user_is_owner = check_is_user_owner_of_plant(current_user, target_rich_plant)
    if not user_is_owner:
        return HttpResponseForbidden()

    if request.method == 'POST':
        image_file = request.FILES['image_file']
        photo_description = request.POST['photo_descr']
        if settings.USE_S3:
            photo = Photo(original=image_file)
            photo.user = current_user
            photo.plant = target_plant
            photo.description = photo_description
            photo.save()
            image_url = photo.medium.url
            photo_id = photo.id
            
        else:
            fs = FileSystemStorage()
            filename = fs.save(f'photos/{current_user.username}/{image_file.name}', image_file)
            image_url = fs.url(filename)
            photo_id = None

        # create log
        create_log(
            Log.ActionChoices.ADDITION,
            current_user,
            target_plant,
            {'action': 'add_photo', 'photo_url': image_url, 'photo_id':photo_id, 'photo_description': photo_description} 
        )
        return redirect('plant_view', plant_id=plant_id)
    
    # Template data
    template = loader.get_template('plants/upload_photo.html')
    context = {
        'plant': target_rich_plant,
    }
    return HttpResponse(template.render(context, request))

@login_required
def set_profile_img(request, plant_id, photo_id=None):
    """Set main photo for plant profile"""

    # authentication
    current_user = request.user

    # try to get plant by id
    target_plant = get_object_or_404(Plant, id=plant_id)
    target_rich_plant = RichPlant(target_plant)

    # check access (is owner?)
    user_is_owner = check_is_user_owner_of_plant(current_user, target_rich_plant)
    if not user_is_owner:
        return HttpResponseForbidden()

    if photo_id:
        photo = get_object_or_404(Photo, id=photo_id)
        
        # check if photo is relaited to this plant
        if not photo in target_rich_plant.get_photos():
            return HttpResponseForbidden()

        # set new profile photo
        target_plant.profile_photo = photo
        target_plant.save()

        return redirect('plant_view', plant_id=plant_id)

    # get photos
    photos = target_rich_plant.get_photos()

    # Template data
    template = loader.get_template('plants/set_profile_img.html')
    context = {
        'plant': target_rich_plant,
        'photos': photos,
    }
    return HttpResponse(template.render(context, request))

  



