from django.db import models

class Plant(models.Model):
    #"{:06d}".format(242323232)
    uid = models.CharField(max_length=10)
    
    creation_date = models.DateTimeField('date created')
    
    #creator = models.ForeignKey()


class Attribute(models.Model):
    class AttributeTypeChoices(models.IntegerChoices):
        STRING = 1
        NUMBER = 2

    name = models.CharField(max_length=100, blank=False, unique=True)
    
    key = models.CharField(max_length=100, blank=False, unique=True)
    
    value_type = models.IntegerField(choices=AttributeTypeChoices.choices)

    #weight = models.IntegerField(blank=True, null=True)



class Action(models.Model):
    name = models.CharField(max_length=100, blank=False, unique=True)
    
    key = models.CharField(max_length=100, blank=False, unique=True)
    
    attributes = models.JSONField(blank=True)
    