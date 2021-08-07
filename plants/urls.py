from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('create/', views.plant_create, name='plant_create_edit'),
    path('view/<int:plant_id>', views.plant_view),
    path('edit/<int:plant_id>', views.plant_create),
]


# urlpatterns = [
#     path('', views.index, name='index'),
#     path('create', views.plant_create, name='create'),
#     path('view/<int:plant_id>', views.plant_view, name='view'),
#     path('edit/<int:plant_id>', views.plant_create, name='edit'),
# ]