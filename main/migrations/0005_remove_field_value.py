# Generated by Django 2.0.2 on 2018-03-02 08:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_field_value'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='field',
            name='value',
        ),
    ]
