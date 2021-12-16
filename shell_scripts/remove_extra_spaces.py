# django shell:
# exec(open('shell_scripts/remove_extra_spaces.py').read())

from plants.models import Log

logs = Log.objects.all()

for l in logs:
    for key in l.data:
        value = l.data[key]
        if type(value) == str and len(value) > 1:
            if value[0] == ' ' or value[-1] == ' ':
                print(value)
                l.data[key] = value.strip()
                l.save()