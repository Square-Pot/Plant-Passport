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
        for attribute in Attribute.objects.all():
            widget = None
            if attribute.value_type == Attribute.AttributeTypeChoices.TEXTAREA:
                widget = forms.Textarea
            if attribute.value_type == Attribute.AttributeTypeChoices.DATE:
                widget = forms.TextInput(attrs={'type': 'date'})
            self.fields[attribute.key] = forms.CharField(label=attribute.name, max_length=100, required=False, widget=widget)    


class AttributeForm(forms.Form):
    """
    Form for editing plant attribute
    """
    def __init__(self, label=None, key=None, value=None, max_length=None, type=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        widget = None
        if type == Attribute.AttributeTypeChoices.TEXTAREA:
            widget = forms.Textarea
        if type == Attribute.AttributeTypeChoices.DATE:
            widget = forms.TextInput(attrs={'type': 'date'})
        self.fields[key] = forms.CharField(label=label, initial=value, max_length=max_length, required=False, widget=widget)



class PhotoForm(forms.ModelForm):
    
    class Meta:
        model = Photo
        fields = ('description', 'photo', 'user')


    
