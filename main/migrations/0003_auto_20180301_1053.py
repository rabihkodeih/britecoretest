# Generated by Django 2.0.2 on 2018-03-01 10:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_risktype_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='enumvalue',
            options={'ordering': ['order']},
        ),
        migrations.AlterModelOptions(
            name='field',
            options={'ordering': ['order']},
        ),
        migrations.AlterModelOptions(
            name='risktype',
            options={'ordering': ['name']},
        ),
        migrations.AlterField(
            model_name='enumvalue',
            name='field',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='enum_values', to='main.Field'),
        ),
        migrations.AlterField(
            model_name='field',
            name='risk_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fields', to='main.RiskType'),
        ),
    ]
