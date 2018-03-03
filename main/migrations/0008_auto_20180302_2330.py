# Generated by Django 2.0.2 on 2018-03-02 23:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_auto_20180302_1744'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='fieldvalue',
            options={'ordering': ['field__order']},
        ),
        migrations.RenameField(
            model_name='fieldvalue',
            old_name='holder',
            new_name='value',
        ),
        migrations.AlterField(
            model_name='fieldvalue',
            name='riskinstance',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='columns', to='main.RiskInstance'),
        ),
    ]
