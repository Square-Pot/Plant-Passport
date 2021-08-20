from plants.models import Log, Plant
from plants.entities import RichPlant


def get_user_plants(user_id):
    """Returns Plant-objects of user by user id"""
    plant_ids = Log.objects.filter(data__owner=user_id).values_list('plant', flat=True)
    plants = Plant.objects.filter(id__in=plant_ids)
    return plants

def get_user_richplants(user_id):
    """Returns RichPlant-objects of user by user id"""
    plants = get_user_plants(user_id)
    rich_plants = []
    for plant in plants:
        rich_plants.append(RichPlant(plant))
    return rich_plants