from django import forms
from .models import Attribute, Plant, RichPlant, Photo
#from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import ModelForm



class PlantForm(forms.Form):
    """
    Generate form fields for all plant attributes
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for attribute in Attribute.objects.all().order_by('weight'):
            # String
            if attribute.value_type == Attribute.AttributeTypeChoices.STRING:
                self.fields[attribute.key] = forms.CharField(label=attribute.name, max_length=attribute.max_text_length, required=False)
            # Textarea
            if attribute.value_type == Attribute.AttributeTypeChoices.TEXTAREA:
                self.fields[attribute.key] = forms.CharField(label=attribute.name, max_length=attribute.max_text_length, required=False, widget=forms.Textarea)
            # Date
            if attribute.value_type == Attribute.AttributeTypeChoices.DATE:
                self.fields[attribute.key] = forms.DateField(label=attribute.name, required=False, widget=forms.widgets.DateInput(attrs={'type': 'date'}))
            # Number
            if attribute.value_type == Attribute.AttributeTypeChoices.NUMBER:
                self.fields[attribute.key] = forms.DecimalField(label=attribute.name, max_digits=5, required=False)
            

class AttributeForm(forms.Form):
    """
    Form for editing plant attribute
    """
    
    def __init__(self, label=None, key=None, value=None, max_length=None, type=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        widget = None
        if type == Attribute.AttributeTypeChoices.TEXTAREA:
            widget = forms.Textarea
        self.fields[key] = forms.CharField(label=label, initial=value, max_length=max_length, required=False, widget=widget)
        
        


class PhotoForm(forms.ModelForm):
    
    class Meta:
        model = Photo
        fields = ('description', 'photo', 'user')


    
