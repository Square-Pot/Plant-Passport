from django import forms
from .models import Attribute


class PlantForm(forms.Form):
    
    def __init__(self, *args, **kwargs):
        """
        Generate form fields for all plant attributes
        """
        # test
        # test 2 
        super(PlantForm, self).__init__(*args, **kwargs)
        for attribute in Attribute.objects.all():
            self.fields[attribute.key] = forms.CharField(label=attribute.name, max_length=100, required=False)    
