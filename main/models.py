from django.db import models
from django.contrib.auth.models import User


class RiskType(models.Model):
    name = models.CharField(max_length=256)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class RiskInstance(models.Model):
    title = models.CharField(max_length=256, unique=True)
    type = models.ForeignKey(RiskType, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


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
    required = models.BooleanField(default=False)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return '(%s) %s: %s' % (self.type.name, self.risk_type.name, self.name)


class FieldValue(models.Model):
    value = models.TextField()
    field = models.ForeignKey(Field, on_delete=models.CASCADE)
    riskinstance = models.ForeignKey(RiskInstance, related_name="columns", on_delete=models.CASCADE)

    class Meta:
        ordering = ['field__order']

    def __str__(self):
        return '(%s, %s) : %s' % (str(self.riskinstance), str(self.field), self.value)


class EnumValue(models.Model):
    field = models.ForeignKey(Field, related_name='enum_values', on_delete=models.CASCADE)
    value = models.CharField(max_length=128)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return '%s: %s' % (self.order, self.value)


# end of file
