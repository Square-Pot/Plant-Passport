from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('create/', views.plant_create, name='plant_create_edit'),
    path('view/<int:plant_id>', views.plant_view),
    #path('edit/<int:plant_id>', views.plant_create),
    path('edit/<int:plant_id>/attr/<str:attr_key>', views.edit_plant_attr, name='plant_edit_attr'),
]       
