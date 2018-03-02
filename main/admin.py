from django.contrib import admin
from main.models import RiskType
from main.models import FieldType
from main.models import Field
from main.models import EnumValue
from main.models import RiskInstance
from main.models import FieldValue


class RiskTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user')


class FieldTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'regex_validator', 'nullable')


class FieldAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'type', 'risk_type', 'order')


class EnumValueAdmin(admin.ModelAdmin):
    list_display = ('id', 'field', 'value', 'order')


class RiskInstanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')


class FieldValueAdmin(admin.ModelAdmin):
    list_display = ('id', 'riskinstance', 'field', 'holder')


admin.site.register(RiskType, RiskTypeAdmin)
admin.site.register(FieldType, FieldTypeAdmin)
admin.site.register(Field, FieldAdmin)
admin.site.register(EnumValue, EnumValueAdmin)
admin.site.register(RiskInstance, RiskInstanceAdmin)
admin.site.register(FieldValue, FieldValueAdmin)