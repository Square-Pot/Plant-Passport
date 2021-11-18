from django.shortcuts import render, get_object_or_404

from rest_framework import viewsets
from rest_framework import permissions

from .serializers import PlantSerializer

# from rest_framework.views import APIView
# from rest_framework.response import Response
from rest_framework import permissions #, authentication
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from taggit.models import Tag

from plants.services import check_is_user_owner_of_plant
from plants.entities import RichPlant
from plants.models import Plant



class PlantViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Plants to be viewed or edited.
    """
    queryset = Plant.objects.all().order_by('-creation_date')
    serializer_class = PlantSerializer
    #permission_classes = [permissions.IsAuthenticated]



# authentication_classes = [authentication.TokenAuthentication]
# permission_classes = [permissions.IsAdminUser]

@api_view(['GET', 'POST'])
@permission_classes((permissions.AllowAny,))
def ListPlants(request):
    username = request.user.username

    if request.method == 'POST':
        return Response({"message": "Got some data!", "data": request.data})
    return Response({"message": "Hello, world! %s" % username })


@api_view(['GET', 'POST'])
@permission_classes((permissions.IsAuthenticated,))
def add_tag_to_plant(request, plant_id: int, tag: str):
    current_user = request.user
    target_plant = get_object_or_404(Plant, id=plant_id)
    rich_plant = RichPlant(target_plant)
    # TODO maybe new tag should send via POST
    if check_is_user_owner_of_plant(current_user, rich_plant):
        tag = tag.strip()
        target_plant.tags.add(tag)
        return Response({"message": "Tag %s was added successfully" % tag})


@api_view(['GET', 'POST'])
@permission_classes((permissions.IsAuthenticated,))
def remove_tag_from_plant(request, plant_id: int, tag: str):
    current_user = request.user
    target_plant = get_object_or_404(Plant, id=plant_id)
    rich_plant = RichPlant(target_plant)
    # TODO maybe new tag should send via POST
    if check_is_user_owner_of_plant(current_user, rich_plant):
        target_plant.tags.remove(tag)
        return Response({"message": "Tag %s was removed successfully" % tag})


@api_view(['GET'])
#@permission_classes((permissions.IsAuthenticatedOrReadOnly,))
@permission_classes((permissions.AllowAny,))
def get_plant_tags(request, plant_id: int):
    target_plant = get_object_or_404(Plant, id=plant_id)
    return Response(target_plant.tags.all().values())


@api_view(['GET'])
@permission_classes((permissions.IsAuthenticatedOrReadOnly,))
def get_plant_tags_and_rest(request, plant_id: int):
    # get plant tags
    target_plant = get_object_or_404(Plant, id=plant_id)
    plant_tags = target_plant.tags.all().values()
    print('*', plant_tags)

    # get user tags
    current_user = request.user
    all_user_tags = Tag.objects.filter(plant__creator=current_user).values()
    #print('*', all_user_tags)

    # list of dics with all user tags and belonging to current plant
    tags_with_belonging = []
    for tag in all_user_tags:
        if tag in plant_tags:
            tags_with_belonging.append({'tag': tag, 'belongs_to_plant': True})
        else:
            tags_with_belonging.append({'tag': tag, 'belongs_to_plant': False})

    return Response(tags_with_belonging)

@api_view((['GET']))
#@permission_classes((permissions.IsAuthenticated,))
@permission_classes((permissions.AllowAny,))
def get_user_tags(request):
    current_user = request.user
    all_tags = Tag.objects.filter(plant__creator=current_user)
    return Response(all_tags.values_list())
