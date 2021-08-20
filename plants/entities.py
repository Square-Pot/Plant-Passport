from .models import Log, Attribute


class ExtraAttrs:
    """Class for storing extra attributes in RichPlant"""
    pass


class RichPlant:
    def __init__(self, plant_object):
        self.Plant = plant_object
        self.__include_plant_attrs()
        self.logs = self.__get_logs()
        self.attrs_as_dic = self.__get_atts_as_dic()
        self.attrs = ExtraAttrs()
        self.__include_extra_attrs()  

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
        all_attrs_keys = Attribute.keys.get_all_keys().order_by('weight')
        
        # blank dic init
        extra_attrs = {}
        for key in all_attrs_keys:
            extra_attrs[key] = None

        # fill with values
        for log in self.logs: 
            for key in log.data:
                if key in extra_attrs:
                    extra_attrs[key] = log.data[key]
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
    
