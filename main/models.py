'''
Created on Feb 4, 2018

@author: rabihkodeih
'''

from django.db import models
from django.contrib.auth.models import User


class RiskType(models.Model):
    name = models.CharField(max_length=256)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class FieldType(models.Model):
    name = models.CharField(max_length=16)
    regex_validator = models.CharField(max_length=256)
    nullable = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name


class Field(models.Model):
    name = models.CharField(max_length=128)
    type = models.ForeignKey(FieldType, on_delete=models.CASCADE)
    risk_type = models.ForeignKey(RiskType, related_name='fields', on_delete=models.CASCADE)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return '%s: %s' % (self.risk_type.name, self.name)
    

class EnumValue(models.Model):
    field = models.ForeignKey(Field, related_name='enum_values', on_delete=models.CASCADE)
    value = models.CharField(max_length=128)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return '%s: %s' % (self.order, self.value)

    








