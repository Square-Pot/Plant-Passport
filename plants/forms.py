from django import forms
from django.forms import ModelForm
from .models import Attribute



class PlantForm(forms.Form):
    #original_field = forms.CharField()
    extra_field_count = forms.CharField(label='Владелец')
    #print(dir(extra_field_count))
    extra_field_count.initial = 'Owner'
    extra_field_count.widget.attrs['readonly'] = True
    

    def __init__(self, *args, **kwargs):
        #extra_fields = kwargs.pop('extra', 0)

        super(PlantForm, self).__init__(*args, **kwargs)
        #self.fields['extra_field_count'].initial = extra_fields

        #for index in range(int(extra_fields)):
        for attribute in Attribute.objects.all():
            # generate extra fields in the number specified via extra_fields
            self.fields[attribute.key] = \
                forms.CharField(label=attribute.name)

# class PlantForm(forms.Form):
#     d = {}
#     for attribute in Attribute.objects.all():
#         if attribute.value_type == 1:ate
#             d["string_{0}".format(attribute.key)] = forms.CharField(label=attribute.key, max_length=100)
