from django.urls import reverse
from django.utils.translation import gettext as _
from .models import Log, Attribute
from users.models import User


class ExtraAttrs:
    """Class for storing extra attributes in RichPlant"""
    pass


class RichPlant:
    def __init__(self, plant_object):
        self.Plant = plant_object
        self.owner = None
        self.__include_plant_attrs()
        self.logs = self.__get_logs()
        self.attrs_as_dic = self.__get_atts_as_dic()
        self.attrs = ExtraAttrs()
        self.__include_extra_attrs() 
    
    def get_attrs_as_str(self, *args):
        """Return string of requested attrs"""
        result = ''
        for key in args:
            if key in self.attrs_as_dic:
                result += self.attrs_as_dic[key] + ' '
        return result

    def get_owners_name(self):
        """Returns username of Rich plant"""
        return User.objects.get(id=self.owner).username

    def __include_plant_attrs(self):
        """Copy Plant model fields"""
        plant_fields_names = self.__get_model_fields(self.Plant)
        for field_name in plant_fields_names:
            value = getattr(self.Plant, field_name)
            setattr(self, field_name, value)

    def __get_logs(self):
        """Get logs of this plant"""
        return Log.objects.filter(plant=self.Plant.id)

    def __get_atts_as_dic(self):
        """Get extra attributes and values from logs as dic"""
        # get ordered list of attibute keys
        all_attrs_keys = list(Attribute.keys.get_all_keys().order_by('weight'))
        
        # blank dic init
        extra_attrs = {}
        for key in all_attrs_keys:
            extra_attrs[key] = None

        # fill with values
        for log in self.logs: 
            for key in log.data:
                if key in extra_attrs:
                    extra_attrs[key] = log.data[key]

                # detect owner
                if key == 'owner':
                    self.owner = log.data[key]
        return extra_attrs

    def __include_extra_attrs(self):
        """Add extra attributes to ReachPlant from dict"""
        for key in self.attrs_as_dic:
            setattr(self.attrs, key, self.attrs_as_dic[key])

    @staticmethod
    def __get_model_fields(obj):
        """Get model attributs names from object"""
        fields_names = []
        for line in obj._meta.fields:
            attr_name = str(line).split('.')[-1]
            fields_names.append(attr_name)
        return fields_names
    


class BrCr:
    '''Breadcrumbs data generator class'''
    def __init__(self):
        self.data = []
        self.home_init()


    def add_level(self, active, url_name, title):
        if active:
            # reset active status in previous levels
            for set in self.data:
                set[0] = False

        if url_name:
            url = reverse(url_name)
        else: 
            url = None
        self.data.append([active, url, title])

    def home_init(self):
        self.add_level(True, 'user_home', _('Home'))
