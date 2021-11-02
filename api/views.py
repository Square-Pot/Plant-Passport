from django.shortcuts import render

from rest_framework import viewsets
from rest_framework import permissions
from plants.models import Plant
from .serializers import PlantSerializer

# from rest_framework.views import APIView
# from rest_framework.response import Response
from rest_framework import permissions #, authentication
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response


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