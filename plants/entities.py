from .services import get_model_fields


class RichPlant:
    def __init__(self, plant_object):
        self.Plant = plant_object
        self.include_plant_attrs()
        self.include_extra_attrs()

    def include_plant_attrs(self):
        """Copy Plant model fields"""
        plant_fields_names = get_model_fields(self.Plant)
        for field_name in plant_fields_names:
            value = getattr(self.Plant, field_name)
            setattr(self, field_name, value)

    def include_extra_attrs(self):
        """Extend list of attributes from logs"""
        pass