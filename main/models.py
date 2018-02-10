'''
Created on Feb 4, 2018

@author: rabihkodeih
'''

import re
from django.db import models


class RiskType(models.Model):
    name = models.CharField(max_length=256)

    @staticmethod
    def serialize_all(deep=False):
        risktypes = RiskType.objects.select_related().order_by('name')
        if deep:
            data = [rt.serialize() for rt in risktypes]
        else:
            data = [{'id': rt.id, 'name': rt.name} for rt in risktypes]
        return data
        
    def serialize(self):
        data = {'id': self.id,
        'name': self.name,
        'fields': [f.serialize() for f in self.field_set.order_by('order')]}
        return data
    
    def __str__(self):
        return self.name


class FieldType(models.Model):
    name = models.CharField(max_length=16)
    regex_validator = models.CharField(max_length=256)
    nullable = models.BooleanField(default=False)
    
    def serialize(self):
        data = {'id': self.id,
                'name': self.name,
                'regex_validator': self.regex_validator,
                'nullable': self.nullable}
        return data
    
    def __str__(self):
        return self.name


class Field(models.Model):
    name = models.CharField(max_length=128)
    type = models.ForeignKey(FieldType, on_delete=models.CASCADE)
    risk_type = models.ForeignKey(RiskType, on_delete=models.CASCADE)
    order = models.IntegerField(default=0)
    
    def serialize(self):
        data = {'id': self.id,
                'name': self.name,
                'html_input_name': re.sub('[^A-Za-z0-9]+', '', self.name).lower(),
                'type': self.type.serialize(),
                'order': self.order}
        enum_values = [v.value for v in self.enumvalue_set.order_by('order')]
        if enum_values:
            data['enum_values'] = enum_values
        return data
    
    def __str__(self):
        return '%s: %s' % (self.risk_type.name, self.name)
    

class EnumValue(models.Model):
    field = models.ForeignKey(Field, on_delete=models.CASCADE)
    value = models.CharField(max_length=128)
    order = models.IntegerField(default=0)
    def __str__(self):
        return '%s: %s' % (self.order, self.value)

    








