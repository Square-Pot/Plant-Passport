from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:plant_uid>/edit', views.index, name='edit'),
]