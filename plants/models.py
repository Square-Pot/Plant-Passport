from django.db import models
from django.conf import settings
from django.utils.translation import gettext, gettext_lazy as _
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.model import AbstractUser


class User(AbstractUser):
    friends = models.ManyToManyField("User", blank=True)

class FriendRequest(models.Model):
    from_user = models.ForeignKey(User, related_name='from_user', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='to_user', on_delete=models.CASCADE)





class Plant(models.Model):
    uid = models.CharField(
        max_length=10,
    )
    
    creation_date = models.DateTimeField(
        auto_now_add=True, 
        blank=True,
    )
    
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        null=True,
    )
    
    is_deleted = models.BooleanField(
        default=False,
    )

    
class AttributeManager(models.Manager):
    def get_all_keys(self):
        return self.order_by('weight').values_list('key', flat=True)

    def get_all_names(self):
        return self.order_by('weight').values_list('name', flat=True)


class Attribute(models.Model):
    class AttributeTypeChoices(models.IntegerChoices):
        STRING = 1
        NUMBER = 2

    name = models.CharField(
        max_length=100, 
        blank=False, 
        unique=True
    ) 

    short_name = models.CharField(
        max_length=10,
        blank=False, 
        unique=True,
        default='replace it',
    ) 
    
    key = models.CharField(
        max_length=100, 
        blank=False, 
        unique=True
    )
    
    value_type = models.IntegerField(
        choices=AttributeTypeChoices.choices
    )
    
    weight = models.IntegerField(
        blank=True, 
        null=True
    )

    objects = models.Manager()

    keys = AttributeManager()

    def __str__(self):
        return f"{self.weight} - {self.name} ({self.key})"


class Log(models.Model):

    CHOICES = {
        1: 'added',
        2: 'changed',
        3: 'deleted',
    }

    class ActionChoices(models.IntegerChoices):
        ADDITION = 1
        CHANGE = 2
        DELETION = 3

    action_time = models.DateTimeField(
        _('action time'),
        default=timezone.now,
        editable=False,
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        models.CASCADE,
        verbose_name=_('user'),
    )

    plant = models.ForeignKey(
        Plant,
        on_delete=models.CASCADE,
        null=True,
    )

    action_type = models.IntegerField(
        choices=ActionChoices.choices,
    )

    data = models.JSONField(
        null=False,
    )

    def __str__(self):
        return f"{self.user} {self.CHOICES[self.action_type]} for plant {self.plant.uid}: {str(self.data)}"


class RichPlantAttrs():
    
    def __init__(self, plant_id):
        self.plant_id = plant_id

    def logs(self):
        return Log.objects.filter(plant=self.plant_id)

    def owner_id(self) -> int:
        log = Log.objects.filter(plant=self.plant_id, data__has_key='owner').order_by('-id')[0]
        return log.data['owner']

    def actual_attrs(self) -> dict:
        # generate blank dic with all keys and placeholders
        attrs_all_keys = Attribute.keys.get_all_keys().order_by('weight')
        actual_attrs = {}
        for key in attrs_all_keys:
            actual_attrs[key] = '-'

        # fill values with logs (playback)
        logs = Log.objects.filter(plant=self.plant_id)
        for log in logs: 
            for key in log.data:
                if key in actual_attrs:
                    actual_attrs[key] = log.data[key]
        return actual_attrs

    def actual_attrs_values(self) -> list:
        return list(self.actual_attrs().values())
     

class RichPlant(Plant):

    # classmethod for creation RichPlant from Plant
    @classmethod
    def new_from(cls, obj):
        if issubclass(obj.__class__, Plant):
            _new = cls(obj.id, obj.uid, obj.creation_date, obj.creator, obj.is_deleted)
            return _new
        else:
            raise TypeError('Expected subclass of <class Plant>, got {}.'.format(type(obj)))
            
    def get_attrs_values(self):
        self.attrs_values = RichPlantAttrs(self.id).actual_attrs_values()

    def get_attrs_dics(self):
        self.attrs_dics = RichPlantAttrs(self.id).actual_attrs()


class Action(models.Model):
    name = models.CharField(max_length=100, blank=False, unique=True)
    key = models.CharField(max_length=100, blank=False, unique=True)
    attributes = models.JSONField(blank=True)
    #weight = models.IntegerField(blank=True, null=True)
    