from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('plant_list/', views.ListPlants, name="api plant list"),
    path('add_tag_to_plant/<int:plant_id>/<str:tag>', views.add_tag_to_plant, name="add tag to plant"),
    path('remove_tag_from_plant/<int:plant_id>/<str:tag>', views.remove_tag_from_plant, name="remove tag from plant"),
    path('get_plant_tags/<int:plant_id>', views.get_plant_tags, name="get plant tags"),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
