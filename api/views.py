from django.shortcuts import render

from plants.models import Plant
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import PlantSerializer


class PlantViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Plants to be viewed or edited.
    """
    queryset = Plant.objects.all().order_by('-creation_date')
    serializer_class = PlantSerializer
    #permission_classes = [permissions.IsAuthenticated]

