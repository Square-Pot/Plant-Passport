from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('create', views.plant_create),
    path('view/<int:plant_id>', views.plant_view),
    path('update/<int:plant_id>', views.plant_update),
]