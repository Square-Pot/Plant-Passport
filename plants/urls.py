from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name="plants"),
    path('<int:user_id>', views.index, name="plants"),
    path('create/', views.plant_create, name='plant_create_edit'),
    path('view/<int:plant_id>', views.plant_view, name='plant_view'),
    path('edit/<int:plant_id>/attr/<str:attr_key>', views.edit_plant_attr, name='plant_edit_attr'),
    path('upload_photo/<int:plant_id>', views.upload_photo, name='upload_photo'),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
