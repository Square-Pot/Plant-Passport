from django.db import models
from django.conf import settings

class Plant(models.Model):
    uid = models.CharField(
        max_length=10
    )
    
    creation_date = models.DateTimeField(
        auto_now_add=True, 
        blank=True
    )
    
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        null=True
    )
    
    is_deleted = models.BooleanField(
        default=False
    )



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

    def __str__(self):
        return f"{self.name} ({self.key})"



class Action(models.Model):
    name = models.CharField(max_length=100, blank=False, unique=True)
    key = models.CharField(max_length=100, blank=False, unique=True)
    attributes = models.JSONField(blank=True)
    #weight = models.IntegerField(blank=True, null=True)
    