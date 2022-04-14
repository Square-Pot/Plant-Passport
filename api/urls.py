from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    #path('plant_list/', views.ListPlants, name="api plant list"),
    path('add_tag_to_plant/<int:plant_id>/<int:tag_id>', views.add_existing_tag_to_plant, name="add tag to plant"),
    path('create_new_tag', views.create_new_tag, name="create new tag"),
    path('remove_tag_from_plant/<int:plant_id>/<int:tag_id>', views.remove_tag_from_plant, name="remove tag from plant"),
    path('get_plant_tags/<int:plant_id>', views.get_plant_tags, name="get plant tags"),
    path('get_plant_tags_and_rest/<int:plant_id>', views.get_plant_tags_and_rest, name="get plant tags and rest"),
    path('get_user_tags/', views.get_user_tags, name="get user tags"), 
    path('set_as_seed/<int:plant_id>', views.set_as_seed, name="set as seed"), 
    path('unset_as_seed/<int:plant_id>', views.unset_as_seed, name="unset as seed"), 
    
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
