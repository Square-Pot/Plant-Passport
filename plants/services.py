from django.utils.translation import gettext as _
from plants.models import Log, Plant, Attribute
from plants.entities import RichPlant


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

def get_attrs_titles_with_transl() -> dict:
    """Returns attribut titles and translation"""
    attr_titles = Attribute.keys.get_all_names()
    result = {}
    for title in attr_titles:
        result[title] = _(title)
    return result

    