from django import forms
from .models import Attribute, Plant, RichPlant


class PlantForm(forms.Form):
    
    def __init__(self, attributes_dic, *args, **kwargs):
        """
        Generate form fields for all plant attributes
        """
        if attributes_dic:
            super().__init__(*args, **kwargs)
            for attribute in Attribute.objects.all():
                self.fields[attribute.key] = forms.CharField(label=attribute.name, initial=attributes_dic[attribute.key],  max_length=100, required=False)    
        else: 
            super().__init__(*args, **kwargs)
            for attribute in Attribute.objects.all():
                self.fields[attribute.key] = forms.CharField(label=attribute.name, max_length=100, required=False)    
