# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-15 18:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travels', '0003_trip_plan'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='users_joined',
            field=models.ManyToManyField(null=True, related_name='users_trips', to='travels.User'),
        ),
    ]
