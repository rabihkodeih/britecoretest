# Generated by Django 2.0.2 on 2018-03-02 17:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_auto_20180302_1743'),
    ]

    operations = [
        migrations.AlterField(
            model_name='riskinstance',
            name='title',
            field=models.CharField(max_length=256, unique=True),
        ),
    ]