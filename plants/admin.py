from django.contrib import admin

# Register your models here.
from .models import Plant, Attribute, Action, Log

admin.site.register(Plant)
admin.site.register(Attribute)
admin.site.register(Action)
admin.site.register(Log)
