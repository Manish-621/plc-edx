# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-06-25 10:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_proctoring_system', '0008_proctoringconfiguration_blur_restriction'),
    ]

    operations = [
        migrations.AddField(
            model_name='proctoringconfiguration',
            name='force_fullscreen',
            field=models.BooleanField(default=True),
        ),
    ]
