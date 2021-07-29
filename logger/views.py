#from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Log response op")


def add(request):
    return HttpResponse("Log response op")