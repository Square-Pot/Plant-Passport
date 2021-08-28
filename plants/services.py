import random
import string
from django.utils.translation import gettext as _
from plants.models import Log, Plant, Attribute
from plants.entities import RichPlant
from users.models import User


# Plants

def get_user_plants(user_id, access=[]):
    """Returns Plant-objects of user by user id"""
    if not access: 
        access = [0,1,2]  # wbithot specifying acces type - returns all plants 
    plant_ids = Log.objects.filter(data__owner=user_id).values_list('plant', flat=True)
    plants = Plant.objects.filter(id__in=plant_ids, access_type__in=access)
    return plants

def get_user_richplants(user_id, access=[]) -> list:
    """Returns RichPlant-objects of user by user id"""
    plants = get_user_plants(user_id, access)
    rich_plants = []
    for plant in plants:
        rich_plants.append(RichPlant(plant))
    return rich_plants

def create_new_plant(user: User) -> Plant:
    """New Plant creation"""
    new_upid = get_new_upid()
    new_plant = Plant(uid=new_upid, creator=user)
    new_plant.save()
    return new_plant

def get_new_upid():
    """Unique Plant ID Generator"""
    while True: 
        # Example: '798670'
        random_string = ''.join(random.choices(string.digits, k=6))
        
        # Check uniqueness
        if Plant.objects.filter(uid=random_string).count() == 0:
            upid = random_string
            break
    return upid

def filter_plants(rich_plants: list, filter_data: dict) -> list:
    """Filter plants according to filtered data"""
    plant_pass_grade = {}
    
    # pass grade calculation
    for plant in rich_plants:
        plant_pass_grade[plant] = 0
        for attr_name in filter_data:
            for val in filter_data[attr_name]:
                if getattr(plant.attrs, attr_name) == val:
                    plant_pass_grade[plant] += 1
    
    # check grade 
    filter_plants = []
    for plant in plant_pass_grade:
        if plant_pass_grade[plant] == len(filter_data):
            filter_plants.append(plant)

    return filter_plants


# Attributes

def get_filtered_attr_values_from_post(post_data) -> dict:
    """
    Convert post-data to filterable attrs dict:

    {
        'genus': ['Lithops', 'Conophytum'], 
        'species': ['karasmontana', 'Leslie'],
    }
    """
    filter_data = {}

    for key in post_data:
        if 'checkbox' in key:
            key = key.split('-')
            attr_name = key[1]
            attr_value = key[2]

            if attr_name in filter_data:
                filter_data[attr_name].append(attr_value)
            else:
                filter_data[attr_name] = [attr_value, ]
    return filter_data

def get_filteraible_attr_values(rich_plants: list) -> dict:
    """
    Returns all availiable filterable attrs dict:

    {
        'genus': [
                {'val':'lithops', 'checked':1},
                {'val':'conophytum', 'checked':1}, 
                {'val':'ophtalmophyllum', 'checked':1},
            ],
        'species':[
                {'val':'karasmontana', 'checked':1},
                {'val':'lesley', 'checked':1},
                {'val':'dorothea', 'checked':1},
            ],
    }    
    """
    filter_data = {}

    # generate blank structure with attr names
    for attr_name in Attribute.keys.get_all_keys():
        filter_data[attr_name] = []

    used_values = {}

    # fill
    for rp in rich_plants: 
        for attr_name in rp.attrs_as_dic:
            if attr_name not in used_values:
                used_values[attr_name] = []
            if check_is_attr_filterable(attr_name):
                value = rp.attrs_as_dic[attr_name]
                if value not in used_values[attr_name]:
                    filter_data[attr_name].append({'val':rp.attrs_as_dic[attr_name], 'checked':1})
                    used_values[attr_name].append(value)
    return filter_data

def filter_data_update(full_filled_filter_data, post_filter_data):
    # reset all checked status to 0 
    for attr_name in full_filled_filter_data:
        for d in full_filled_filter_data[attr_name]:
            d['checked'] = 0

    # set checked status to 1 as in posted data
    for post_attr_name in post_filter_data:
        for post_val in post_filter_data[post_attr_name]:
            for d in full_filled_filter_data[post_attr_name]:
                if d['val'] == post_val:
                    d['checked'] = 1

    return full_filled_filter_data

def check_is_attr_filterable(attr_key):
    attr = Attribute.objects.get(key=attr_key)
    return attr.filterable

def check_is_attr_show_in_list(attr):
    attr = Attribute.objects.get(key=attr_key)
    return attr.show_in_list

def get_attrs_titles_with_transl() -> dict:
    """Returns attribut titles and translation"""
    attr_titles = []
    attrs = Attribute.objects.filter(show_in_list=True).order_by('weight')
    for attr in attrs:
        attr_titles.append(attr.name)

    result = {}
    for title in attr_titles:
        result[title] = _(title)
    return result

def get_attr_keys_not_showing_in_list() -> list:
    attrs = Attribute.objects.filter(show_in_list=False)
    attr_keys = []
    for attr in attrs:
        attr_keys.append(attr.key)
    return(attr_keys)


# Users

def check_are_users_friends(user_1, user_2):
    """Check if one user is friend of another"""
    if user_1 in user_2.friends.all():
        return True
    else:
        return False

def check_is_user_friend_of_plant_owner(user, target_rich_plant):
    """Check if user is friend of Rich plant owner """
    target_user = User.objects.get(id=target_rich_plant.owner)
    if user in target_user.friends.all():
        return True
    else:
        return False

def check_is_user_owner_of_plant(user, target_rich_plant):
    """Check if user is owner of Rich plant"""
    if user.id == target_rich_plant.owner:
        return True
    else:
        return False


# Logs

def create_log(action_type: Log.ActionChoices, user: User, plant: Plant, data: dict):
    """Create new log"""
    new_log = Log(
        action_type = action_type,
        user = user, 
        plant = plant, 
        data = data
    )
    new_log.save()