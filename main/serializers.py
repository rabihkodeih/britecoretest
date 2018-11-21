import json
from main.models import RiskType
from main.models import RiskInstance
from main.models import FieldType
from main.models import Field
from main.models import EnumValue
from main.models import FieldValue
from rest_framework import serializers
from json.decoder import JSONDecodeError


class EnumValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnumValue
        fields = ('value',)


class FieldTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldType
        fields = ('id', 'name', 'regex_validator', 'nullable')


class FieldSerializer(serializers.ModelSerializer):
    type = FieldTypeSerializer(read_only=False)
    enum_values = EnumValueSerializer(many=True, read_only=False)

    class Meta:
        model = Field
        fields = ('id', 'name', 'type', 'required', 'order', 'enum_values')


class RiskTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiskType
        fields = ('id', 'name')


class FieldValueSerializer(serializers.ModelSerializer):
    field = FieldSerializer(read_only=False)
    value = serializers.SerializerMethodField()

    def get_value(self, obj):
        try:
            return json.loads(obj.value.replace("'", '"'))
        except JSONDecodeError:
            return obj.value

    class Meta:
        model = FieldValue
        fields = ('value', 'field')


class RiskInstanceSerializer(serializers.ModelSerializer):
    columns = FieldValueSerializer(many=True, read_only=False)
    type = RiskTypeSerializer(read_only=False)

    class Meta:
        model = RiskInstance
        fields = ('id', 'title', 'type', 'columns')


class RiskInstanceShallowSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiskInstance
        fields = ('id', 'title')


# end of file
