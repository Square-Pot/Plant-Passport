

def get_model_fields(obj):
    """Get model attributs names from object"""
    fields_names = []
    for line in obj._meta.fields:
        attr_name = str(line).split('.')[-1]
        fields_names.append(attr_name)
    return fields_names

