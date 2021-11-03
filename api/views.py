from django.shortcuts import render, get_object_or_404

from rest_framework import viewsets
from rest_framework import permissions

from .serializers import PlantSerializer

# from rest_framework.views import APIView
# from rest_framework.response import Response
from rest_framework import permissions #, authentication
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

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


@api_view(['GET'])
@permission_classes((permissions.IsAuthenticatedOrReadOnly,))
def get_plant_tags(request, plant_id: int):
    target_plant = get_object_or_404(Plant, id=plant_id)
    return Response(target_plant.tags.all().values())
