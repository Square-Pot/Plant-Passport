from django import forms
from .models import Attribute


class PlantForm(forms.Form):
    def __init__(self):
        super().__init__()
        for attribute in Attribute.objects.all():
            # generate extra fields in the number specified via extra_fields
            self.fields[attribute.key] = \
                forms.CharField(label=attribute.name)    
