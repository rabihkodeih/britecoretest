from django.contrib import admin
from main.models import RiskType
from main.models import FieldType
from main.models import Field
from main.models import EnumValue
from main.models import RiskInstance
from main.models import FieldValue


@admin.register(RiskType)
class RiskTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user')


@admin.register(FieldType)
class FieldTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'regex_validator', 'nullable')


@admin.register(Field)
class FieldAdmin(admin.ModelAdmin):
    list_editable = ('required',)
    list_display = ('id', 'name', 'type', 'risk_type', 'required', 'order')


@admin.register(EnumValue)
class EnumValueAdmin(admin.ModelAdmin):
    list_display = ('id', 'field', 'value', 'order')


@admin.register(RiskInstance)
class RiskInstanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')


@admin.register(FieldValue)
class FieldValueAdmin(admin.ModelAdmin):
    list_display = ('id', 'riskinstance', 'field', 'value')


# end of file
