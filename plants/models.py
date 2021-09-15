from django.db import models
from django.conf import settings
from django.utils.translation import gettext, gettext_lazy as _
from django.utils import timezone
from django.conf import settings


class Plant(models.Model):

    class AccessTypeChoices(models.IntegerChoices):
        PUBLIC = 0
        FRIENDS = 1
        PRIVATE = 2

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

    access_type = models.IntegerField(
        choices=AccessTypeChoices.choices,
        default=0,
    )

    def __str__(self):
        return f"{self.uid}  by  {self.creator} "

    
class AttributeManager(models.Manager):
    def get_all_keys(self):
        return self.order_by('weight').values_list('key', flat=True)

    def get_all_names(self):
        return self.order_by('weight').values_list('name', flat=True)


class Attribute(models.Model):

    # TODO before deploy: exclude the gap between 2 and 4
    class AttributeTypeChoices(models.IntegerChoices):
        STRING = 1
        NUMBER = 2
        #TEXT = 3
        DATE = 4
        TEXTAREA = 5

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

    show_in_list = models.BooleanField(
        default=True,
    )

    filterable = models.BooleanField(
        default=False,
    )

    max_text_length = models.IntegerField(
        default=100,
    )
    
    objects = models.Manager()

    keys = AttributeManager()

    def __str__(self):
        return f"{self.weight} - {self.name} ({self.key})"


class ActionManager(models.Manager):
    def get_all_keys(self):
        return self.values_list('key', flat=True)

    def get_all_names(self):
        return self.values_list('name', flat=True)


class Action(models.Model):
    name = models.CharField(
        max_length=100, 
        blank=False, 
        unique=True,
    ) 

    key = models.CharField(
        max_length=100, 
        blank=False, 
        unique=True,
    )

    related_attributes = models.ManyToManyField(
        "Attribute", 
        blank=True
    )

    icon = models.CharField(
        max_length=100, 
        blank=True, 
    )

    color = models.CharField(
        max_length=100, 
        blank=True,
    )

    comment_option = models.BooleanField(
        default=True,
    )

    objects = models.Manager()

    keys = ActionManager()

    def __str__(self):
        return f"{self.name} - {self.key} ({self.color})"


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

    hidden = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return f"{self.user} {self.CHOICES[self.action_type]} for plant {self.plant.uid}: {str(self.data)}"


def user_directory_path(instance, filename):
    # TODO: file name scheme: uid_date
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f'photos/{instance.user.username}/{filename}'


class Photo(models.Model):
    description = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        models.CASCADE,
        verbose_name=_('user'),
    )
    photo = models.FileField(upload_to=user_directory_path)