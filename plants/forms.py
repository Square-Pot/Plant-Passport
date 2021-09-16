import datetime
from django import forms
from django.forms import ModelForm
from django.utils.translation import gettext as _
from .models import Attribute, Plant, Action, Photo


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
                self.fields[attribute.key] = forms.FloatField(label=attribute.name, required=False)
            

class AttributeForm(forms.Form):
    """
    Form for editing plant attribute
    """
    def __init__(self, label=None, key=None, value=None, max_length=None, type=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # String
        if type == Attribute.AttributeTypeChoices.STRING:
            self.fields[key] = forms.CharField(label=label, initial=value, max_length=max_length, required=False)
        # Textarea
        if type == Attribute.AttributeTypeChoices.TEXTAREA:
            self.fields[key] = forms.CharField(label=label, initial=value, max_length=max_length, required=False, widget=forms.Textarea)
        # Date
        if type == Attribute.AttributeTypeChoices.DATE:
            self.fields[key] = forms.DateField(label=label, required=False, initial=value, widget=forms.widgets.DateInput(attrs={'type': 'date'}))
        # Number
        if type == Attribute.AttributeTypeChoices.NUMBER:
            self.fields[key] = forms.FloatField(label=label, initial=value, required=False)


class ActionForm(forms.Form):
    def __init__(self, action, rich_plant, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # comment field
        self.fields['comment'] = forms.CharField(label=_('Comment'), required=False, widget=forms.Textarea)

        # related attributes optional fields
        related_attrs = action.related_attributes.all()
        for attr in related_attrs:
            # String
            if attr.value_type == Attribute.AttributeTypeChoices.STRING:
                self.fields[attr.key] = forms.CharField(label=attr.name, initial=rich_plant.attrs_as_dic[attr.key], max_length=100, required=False)
            # Number
            if attr.value_type == Attribute.AttributeTypeChoices.NUMBER:
                self.fields[attr.key] = forms.FloatField(label=attr.name, initial=rich_plant.attrs_as_dic[attr.key], required=False)


class PhotoForm(forms.ModelForm):
    
    class Meta:
        model = Photo
        fields = ('description', 'original', 'user')


    
