# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-05-29 15:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_proctoring_system', '0005_auto_20200527_1032'),
    ]

    operations = [
        migrations.AddField(
            model_name='proctoringconfiguration',
            name='enable_camera',
            field=models.BooleanField(default=True),
        ),
    ]
