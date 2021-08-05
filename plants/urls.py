from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('create', views.plant_create),
    path('view/<int:plant_id>', views.plant_view),
    path('edit/<int:plant_id>', views.plant_edit),
]