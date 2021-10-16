# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-10-15 11:22


import django.core.validators
from django.db import migrations, models
import django.db.models.manager
import re


class Migration(migrations.Migration):

    dependencies = [
        ('naturebank', '0002_remove_useless_manytomanyfield_options'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='tempdelete',
            managers=[
                ('gis_objects', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterField(
            model_name='geocodeoption',
            name='code',
            field=models.CharField(max_length=10, primary_key=True, serialize=False, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:\\,\\d+)*\\Z'), code='invalid', message='Enter only digits separated by commas.')]),
        ),
    ]
