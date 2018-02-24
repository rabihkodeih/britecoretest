'''
Created on Feb 24, 2018

@author: rabihkodeih
'''

from main.models import RiskType, FieldType, Field, EnumValue
from rest_framework import serializers  # @UnresolvedImport


class EnumValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnumValue
        fields = ('value',)
        

class FieldTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldType
        fields = ('id', 'name', 'regex_validator', 'nullable')


class FieldSerializer(serializers.ModelSerializer):
    type = FieldTypeSerializer(read_only=True)
    enum_values = EnumValueSerializer(many=True, read_only=True) 
    class Meta:
        model = Field
        fields = ('id', 'name', 'type', 'order', 'enum_values')
        

class RiskTypeSerializer(serializers.ModelSerializer):
    fields = FieldSerializer(many=True, read_only=True)
    class Meta:
        model = RiskType
        fields = ('id', 'name', 'fields')


class RiskTypeShallowSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiskType
        fields = ('id', 'name')



