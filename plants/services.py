from django.utils.translation import gettext as _
from plants.models import Log, Plant, Attribute
from plants.entities import RichPlant
from users.models import User


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



def get_filteraible_attr_values(rich_plants: list) -> dict:
    """Temproray method: get availiable filterable attrs """
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


def check_is_attr_filterable(attr_key):
    attr = Attribute.objects.get(key=attr_key)
    return attr.filterable

def check_is_attr_show_in_list(attr):
    attr = Attribute.objects.get(key=attr_key)
    return attr.show_in_list

def get_attrs_titles_with_transl() -> dict:
    """Returns attribut titles and translation"""
    attr_titles = Attribute.keys.get_all_names()
    result = {}
    for title in attr_titles:
        result[title] = _(title)
    return result

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

