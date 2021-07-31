from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create', views.plant_create, name='create'),
    path('<int:plant_uid>', views.plant_view, name='view'),
    path('update/<int:plant_uid>', views.plant_update, name='update'),
]