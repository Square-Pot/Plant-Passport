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
from users.models import User



class PlantViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Plants to be viewed or edited.
    """
    queryset = Plant.objects.all().order_by('-creation_date')
    serializer_class = PlantSerializer
    #permission_classes = [permissions.IsAuthenticated]



# authentication_classes = [authentication.TokenAuthentication]
# permission_classes = [permissions.IsAdminUser]
# @api_view(['GET', 'POST'])
# @permission_classes((permissions.AllowAny,))
# def ListPlants(request):
#     username = request.user.username

#     if request.method == 'POST':
#         return Response({"message": "Got some data!", "data": request.data})
#     return Response({"message": "Hello, world! %s" % username })


@api_view(['GET', 'POST'])
@permission_classes((permissions.IsAuthenticated,))
def add_existing_tag_to_plant(request, plant_id: int, tag_id: int):
    current_user = request.user
    tag = Tag.objects.get(id = tag_id)
    target_plant = get_object_or_404(Plant, id=plant_id)
    rich_plant = RichPlant(target_plant)
    if check_is_user_owner_of_plant(current_user, rich_plant):
        target_plant.tags.add(tag.name)
        return Response({"message": "Tag %s was added successfully" % tag})


@api_view(['POST'])
@permission_classes((permissions.IsAuthenticated,))
def create_new_tag(request):
    current_user = request.user

    if 'plant_id' in request.data:
        plant_id = request.data['plant_id']
        target_plant = get_object_or_404(Plant, id=plant_id)
    else:
        return Response({"message": "No plant id!"})

    if 'tag_name' in request.data:
        new_tag = request.data['tag_name']
    else:
        return Response({"message": "No tag was received!"})

    rich_plant = RichPlant(target_plant)

    if check_is_user_owner_of_plant(current_user, rich_plant):
        new_tag = new_tag.strip()
        target_plant.tags.add(new_tag)
        #print(new_tag, 'created')
        return Response({"message": "Tag %s was created successfully" % new_tag})
    else:
        return Response({"message": "Current user is not the owner" })


@api_view(['GET'])
@permission_classes((permissions.IsAuthenticated,))
def remove_tag_from_plant(request, plant_id: int, tag_id: int):
    current_user = request.user
    target_plant = get_object_or_404(Plant, id=plant_id)
    rich_plant = RichPlant(target_plant)
    if check_is_user_owner_of_plant(current_user, rich_plant):
        tag = Tag.objects.get(id = tag_id)
        target_plant.tags.remove(tag.name)
        return Response({"message": "Tag %s was removed successfully" % tag.name})
    else: 
        return Response({"message": "You are not the owner of the plant" })


# not using method afair
@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def get_plant_tags(request, plant_id: int):
    target_plant = get_object_or_404(Plant, id=plant_id)
    return Response(target_plant.tags.all().values())


@api_view(['GET'])
#@permission_classes((permissions.IsAuthenticated,))
@permission_classes((permissions.AllowAny,))
def get_plant_tags_and_rest(request, plant_id: int):
    target_plant = get_object_or_404(Plant, id=plant_id)
    plant_tags = target_plant.tags.all().values()
    current_user = request.user
    if current_user.is_authenticated: 
        rich_plant = RichPlant(target_plant)
        # for owner show plant tags and other available tags
        if check_is_user_owner_of_plant(current_user, rich_plant):
            all_user_tags = Tag.objects.filter(plant__creator=current_user).values()
            # list of dics with all user tags and belonging to current plant
            tags_with_belonging = []
            # for check uniqueness in result list of dics
            used_tags = []
            for tag in all_user_tags:
                if tag not in used_tags:
                    used_tags.append(tag)
                    if tag in plant_tags:
                        tag_dic = {}
                        tag_dic['id'] = tag['id']
                        tag_dic['name'] = tag['name']
                        tag_dic['belongs'] = True
                        tags_with_belonging.append(tag_dic)
                    else:
                        tag_dic = {}
                        tag_dic['id'] = tag['id']
                        tag_dic['name'] = tag['name']
                        tag_dic['belongs'] = False
                        tags_with_belonging.append(tag_dic)
            return Response(tags_with_belonging)

        # for not owners show only plant tags
        else:
            tags_with_belonging = []
            for tag in plant_tags:
                tag_dic = {}
                tag_dic['id'] = tag['id']
                tag_dic['name'] = tag['name']
                tag_dic['belongs'] = True
                tags_with_belonging.append(tag_dic)
            return Response(tags_with_belonging)
    else:
        # for anons
        tags_with_belonging = []
        for tag in plant_tags:
            tag_dic = {}
            tag_dic['id'] = tag['id']
            tag_dic['name'] = tag['name']
            tag_dic['belongs'] = True
            tags_with_belonging.append(tag_dic)
        return Response(tags_with_belonging)



@api_view((['GET']))
@permission_classes((permissions.IsAuthenticated,))
#@permission_classes((permissions.AllowAny,))
def get_user_tags(request):
    current_user = request.user
    all_tags = Tag.objects.filter(plant__creator=current_user)
    return Response(all_tags.values_list())
