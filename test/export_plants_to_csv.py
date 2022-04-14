# A command to run the script via shell: 
# ./manage.py shell < export_plants_to_csv.py 
#

from plants.models import Plant, Attribute
from plants.entities import RichPlant
from plants.services import get_attrs_titles_with_transl


SEPARATOR = '|'
RESULT_FILENAME = 'plants_export.txt'

# Collect all data: plants and attributes
attributes = Attribute.objects.all().order_by('weight')
plants = Plant.objects.all()
rich_plants = []
for p in plants: 
    rich_plants.append(RichPlant(p))

# Create first line: titles
title_line = 'UID' + SEPARATOR
for a in attributes: 
    title_line += a.key + SEPARATOR
title_line += '\n'

# Export data to file
with open(RESULT_FILENAME, 'w') as f: 
    f.write(title_line)

    for rplant in rich_plants: 
        line = '%s%s' % (rplant.Plant.uid, SEPARATOR)
        for a in attributes:
            if a.key in rplant.attrs_as_dic:
                line += str(rplant.attrs_as_dic[a.key]) + SEPARATOR
            else:
                line += SEPARATOR
        line += '\n'
        f.write(line)

