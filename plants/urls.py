from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('', views.index, name="plants"),
    path('by_user/<int:user_id>', views.index, name="plants_by_user"),
    path('create/', views.plant_create, name='plant_create_edit'),
    path('<int:plant_id>/view', views.plant_view, name='plant_view'),
    path('<int:plant_id>/edit/attr/<str:attr_key>', views.edit_plant_attr, name='plant_edit_attr'),
    path('<int:plant_id>/add/action/<str:action_key>', views.add_plant_action, name='plant_add_action'),
    path('<int:plant_id>/upload_photo', views.upload_photo, name='upload_photo'),
    path('<int:plant_id>/set_profile_img', views.set_profile_img, name='set_profile_img_dialog'),
    path('<int:plant_id>/set_profile_img/<int:photo_id>', views.set_profile_img, name='set_profile_img'),
    path('detect', views.upload_photo_decode_matrix, name='detect_photo'),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


