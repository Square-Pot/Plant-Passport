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
                        create_log, create_new_plant, detect_data_matrix, \
                        get_date_from_exif
from users.services import is_friend
from .entities import RichPlant, BrCr, GenusForGroups, TagForGroups
from api.serializers import PlantSerializer, UserSerializer
from taggit.models import Tag


# https://docs.djangoproject.com/en/3.2/topics/auth/default/#the-login-required-decorator
from django.contrib.auth.decorators import login_required


def index(request, user_id=None, genus=None, tag_id=None, is_seed=None):
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
            rich_plants = get_user_richplants(user_id, genus=genus, tag_id=tag_id, seeds=is_seed)
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
            rich_plants = get_user_richplants(user_id, access=access, genus=genus, tag_id=tag_id, seeds=is_seed)
        # for anonymous
        else:
            access = [Plant.AccessTypeChoices.PUBLIC,]
            rich_plants = get_user_richplants(user_id, access=access, genus=genus, tag_id=tag_id, seeds=is_seed)
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


def groups(request, user_id=None):
    """ Groups of user plants: genuses, tags, etc. """

    # Breadcrumbs data
    brcr = BrCr()

    # Show personal plants
    if not user_id: 
        # authenticated
        current_user = request.user
        if current_user.is_authenticated:
            user_id = current_user.id
            rich_plants = get_user_richplants(user_id)

            # # Translators: Section name
            # section_name = _('MyPlants')
            user_name = current_user.username
            # is_owner = True
            # brcr.add_level(True, '', section_name)

        # anonymous
        else:
            return redirect('login')

    # Show someone's plants
    else:
        target_user = get_object_or_404(User, id=user_id)
        current_user = request.user
        tags = Tag.objects.filter(entry__user=current_user)
        # for friend
        if current_user.is_authenticated and is_friend(current_user, target_user):
            access = [Plant.AccessTypeChoices.PUBLIC, Plant.AccessTypeChoices.FRIENDS]
            rich_plants = get_user_richplants(user_id, access)
        # for anonymous
        else:
            access = [Plant.AccessTypeChoices.PUBLIC,]
            rich_plants = get_user_richplants(user_id, access)

        # section_name = _('PlantsOfUser') 
        user_name = target_user.username
        # is_owner = False
        # brcr.add_level(True, '', f'{section_name}: {user_name}')

    # make dic of available genuses and count plants
    genuses_plants = {}
    genuses_seeds =  {}
    tags_plants = {}
    tags_seeds =  {}

    for rp in rich_plants:
        # genuses 
        genus = rp.attrs.genus
        genus = genus.lower() if genus else 'None'
        
        #print(rp.is_seed)

        # for seed section 
        if rp.is_seed:
            # genuses
            if genus in genuses_seeds:  
                genuses_seeds[genus] += 1
            else: 
                genuses_seeds[genus] = 1

            # tags
            for tag in rp.Plant.tags.values():
                if tag['id'] in tags_seeds:
                    tags_seeds[tag['id']] += 1
                else:
                    tags_seeds[tag['id']] = 1
        
        # for plant section 
        else:
            # genuses
            if genus in genuses_plants:  
                genuses_plants[genus] += 1
            else: 
                genuses_plants[genus] = 1

            # tags
            for tag in rp.Plant.tags.values():
                if tag['id'] in tags_plants:
                    tags_plants[tag['id']] += 1
                else:
                    tags_plants[tag['id']] = 1

    # TODO why here empty genus? 
    try:
        genuses_plants.pop('None')
        genuses_seeds.pop('None')
    except:
        pass

    #print(genuses_seeds)

    # convert genuses dic to list of objects
    genuses_plant_objects = []
    for genus in genuses_plants: 
        genus_obj = GenusForGroups()
        genus_obj.name = genus
        genus_obj.number = genuses_plants[genus]
        genuses_plant_objects.append(genus_obj)

    genuses_seed_objects = []
    for genus in genuses_seeds: 
        genus_obj = GenusForGroups()
        genus_obj.name = genus
        genus_obj.number = genuses_seeds[genus]
        genuses_seed_objects.append(genus_obj)


    # convert tags dic to list of objects
    tag_plant_objects = []
    for tag_id in tags_plants:
        tag = Tag.objects.get(id=tag_id)
        tag_obj = TagForGroups()
        tag_obj.name = tag.name
        tag_obj.id = tag.id
        tag_obj.number = tags_plants[tag_id]
        tag_plant_objects.append(tag_obj)

    tag_seed_objects = []
    for tag_id in tags_seeds:
        tag = Tag.objects.get(id=tag_id)
        tag_obj = TagForGroups()
        tag_obj.name = tag.name
        tag_obj.id = tag.id
        tag_obj.number = tags_seeds[tag_id]
        tag_seed_objects.append(tag_obj)

    # sorted by name
    genuses_plant_objects_sorted = sorted(genuses_plant_objects, key=lambda x: x.name, reverse=False)
    genuses_seed_objects_sorted = sorted(genuses_seed_objects, key=lambda x: x.name, reverse=False)

    # Template data
    context = {
        'genuses': genuses_plant_objects_sorted, 
        'tags': tag_plant_objects,
        'seeds_genuses': genuses_seed_objects_sorted,
        'seeds_tags': tag_seed_objects,
        'user_name': user_name,
        #'title': _('Plants grouped:'),
        #'brcr_data': brcr.data,
    }
    template = loader.get_template('plants/groups.html')
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

        plant_serialized = PlantSerializer(target_plant).data
        user_serialized = UserSerializer(current_user).data

        # Template data
        context = {
            'plant': rich_plant,
            'section_name': section_name,
            'user_name': user_name,
            'is_owner': is_owner,
            'brcr_data': brcr.data,
            'plant_serialized': plant_serialized,
            'user_serialized': user_serialized,
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

        image_file = request.FILES.get('image_file', False)
        if not image_file:
            return redirect('upload_photo', plant_id=plant_id)

        photo_description = request.POST['photo_descr']
        
        if 'PhotoDateFromExif' in request.POST:
            # try to get date from exif    
            exif_date = get_date_from_exif(image_file)
            if exif_date:
                photo_datetime = exif_date
            else:
                # if failed, try to get from date field
                photo_datetime = request.POST['photo_datetime'] if request.POST['photo_datetime'] else None
        else:
            # try to get from date field
            photo_datetime = request.POST['photo_datetime'] if request.POST['photo_datetime'] else None

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
            {'action': 'add_photo', 'photo_url': image_url, 'photo_id':photo_id, 'photo_description': photo_description},
            action_time = photo_datetime
        )
        return redirect('plant_view', plant_id=plant_id)
    
    # Template data
    template = loader.get_template('plants/upload_photo.html')
    context = {
        'plant': target_rich_plant,
    }
    return HttpResponse(template.render(context, request))


@login_required
def upload_photo_decode_matrix(request):
    """Photo Uploading, try to detect PUID by Data Matrix and save if successful"""

    # authentication
    current_user = request.user

    messages = []
    context = {}

    if request.method == 'POST':

        image_file = request.FILES.get('image_file', False)
        if not image_file:
            return redirect('detect_photo')

        if 'PhotoDateFromExif' in request.POST:
            # try to get date from exif    
            photo_datetime = get_date_from_exif(image_file)
            messages.append(f'Date from EXIF: {photo_datetime}')
        else:
            photo_datetime =  None

        # try to detect PUID by Data Matrix
        puids = detect_data_matrix(image_file)
        if len(puids) > 0:
            rich_plants = []
            for puid in puids:

                # try to get plant by puid
                try:
                    plant = Plant.objects.get(uid=puid['puid'])
                except Plant.DoesNotExist:
                    messages.append('No plant was found with PUID: %s' % puid['puid'])
                    break
                
                rich_plant = RichPlant(plant)

                # check access (is owner?)
                user_is_owner = check_is_user_owner_of_plant(current_user, rich_plant)
                if not user_is_owner:
                    messages.append(f'{current_user.username} is not the owner of plant with PUID: {puid}')
                    break

                rich_plants.append(rich_plant)
                
                # save image
                if settings.USE_S3:
                    photo = Photo(original=image_file)
                    photo.user = current_user
                    photo.plant = plant
                    #photo.description = photo_description
                    photo.save()
                    image_url = photo.medium.url
                    photo_id = photo.id
                    
                else:
                    fs = FileSystemStorage()
                    filename = fs.save(f'photos/{current_user.username}/{image_file.name}', image_file)
                    image_url = fs.url(filename)
                    photo_id = None

                # create log
                photo_description = 'Autodetected photo.'
                if 'position_clarifications' in puid:
                    photo_description += '\n Data matrix position calrification:\n'
                    for line in puid['position_clarifications']:
                        photo_description += ' ' + line + '<br />'
                create_log(
                    Log.ActionChoices.ADDITION,
                    current_user,
                    plant,
                    {'action': 'add_photo', 'photo_url': image_url, 'photo_id':photo_id, 'photo_description': photo_description},
                    action_time = photo_datetime
                )
            context['rich_plants'] = rich_plants
        else: 
            messages.append('Plant identification was failed')
    else:
        messages.append('Please upload a photo')

    # Template data
    template = loader.get_template('plants/detect_photo.html')
    context['messages'] = messages

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

  



