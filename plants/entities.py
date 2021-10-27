from django.urls import reverse
from django.utils.translation import gettext as _
from .models import Log, Attribute, Photo
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
        self.logs_for_cards = self.__prepare_logs_for_cards()
        self.attrs_as_dic = self.__get_atts_as_dic()
        self.attrs_as_list_w_types = self.__get_attrs_as_list_w_types()
        self.attrs = ExtraAttrs()
        self.__include_extra_attrs()
        self.fancy_name = self.__get_fancy_name()
        self.photos = None
    
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

    def __get_fancy_name(self):
        fancy_name = ''
        attrs = self.attrs_as_list_w_types
        for attr in attrs:
            if attr['value']:
                # Field Number always uppercase
                if attr['key'] == "number":
                    fancy_name += f"{attr['value'].upper()}: "
                # Genus always capitlized and italic
                elif attr['key'] == "genus":
                    fancy_name += f"<i>{attr['value'].capitalize()}</i> "
                # species  
                elif attr['key'] == 'species':
                    fancy_name += f"<i>{attr['value'].lower()}</i> " 
                # subspecies, variety always italic and lowercase with short name
                elif attr['key'] in ['subspecies', 'variety']:
                    fancy_name += f"{attr['short_name']} <i>{attr['value'].lower()}</i> " 
                # Cultivated variety alway regular Uppercase
                elif attr['key'] == 'cultivar':
                    fancy_name += f"{attr['short_name']}  ‘{attr['value'].title()}’ " 
                # etc.
                elif attr['key'] in ['affinity', 'ex']:
                    fancy_name += f"{attr['short_name']} {attr['value'].title()} " 
        return fancy_name

    def __include_plant_attrs(self):
        """Copy Plant model fields"""
        plant_fields_names = self.__get_model_fields(self.Plant)
        for field_name in plant_fields_names:
            value = getattr(self.Plant, field_name)
            setattr(self, field_name, value)

    def __get_logs(self, order_by ='-action_time'):
        """Get logs of this plant"""
        return Log.objects.filter(plant=self.Plant.id).order_by(order_by)

    def __prepare_logs_for_cards(self):
        prepared_logs = []

        for log in self.logs: 
            l = LogForCard()

            if log.action_type == 1:
                l.title = _('Addition')
            elif log.action_type == 2:
                l.title = _('Editing')
            elif log.action_type == 3: 
                l.title = _('Deleting')

            for key in log.data:
                if key == 'action':
                    l.subtitle = log.data[key]
                elif key == 'photo_url':
                    l.img_url = log.data[key]
                elif key == 'comment' or key == 'photo_description':
                    l.text = log.data[key]
                else:
                    l.attrs[key] = log.data[key]

            prepared_logs.append(l)

        return prepared_logs


    def __get_atts_as_dic(self):
        """Get extra attributes and values from logs as dic"""
        # get ordered list of attibute keys
        all_attrs_keys = list(Attribute.keys.get_all_keys().order_by('weight'))
        
        # blank dic init
        extra_attrs = {}
        for key in all_attrs_keys:
            extra_attrs[key] = None

        # fill with values
        for log in self.__get_logs(order_by='action_time'): 
            for key in log.data:
                if key in extra_attrs:
                    extra_attrs[key] = log.data[key]

                # detect owner
                if key == 'owner':
                    self.owner = log.data[key]

        return extra_attrs

    def __get_attrs_as_list_w_types(self) -> list:
        """Get extra attributes as list of dics with: key, value, type"""
        attrs_as_dic = self.attrs_as_dic
        attrs_as_list_w_types = []
        for attr_key in attrs_as_dic:
            attr =  Attribute.objects.get(key=attr_key)
            d = {
                    'key': attr_key, 
                    'value': self.attrs_as_dic[attr_key],
                    'type': attr.value_type,
                    'name': attr.name,
                    'short_name': attr.short_name
                }
            attrs_as_list_w_types.append(d)
        return attrs_as_list_w_types

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

    def get_photos(self):
        return Photo.objects.filter(plant=self.Plant)


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


class LogForCard:
    def __init__(self):
        self.title = None
        self.subtitle = None
        self.img_url = None
        self.img_alt = None
        self.text = None
        self.attrs = {}
