from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Plant, Attribute, Action


def index(request):
    return HttpResponse("Plants here will be")


def plant_view(request, plant_id):
    return HttpResponse("Plants here will be")


def plant_create(request):
    attributes = Attribute.objects.all()
    template = loader.get_template('plants/create.html')
    context = {
        'attributes': attributes,
    }

    return HttpResponse(template.render(context, request))



def plant_update(request, plant_id):
    return HttpResponse("Plants here will be")

