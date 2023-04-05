# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-04-01 07:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course_overviews', '0015_courseoverview_is_assessment'),
    ]

    operations = [
        migrations.AddField(
            model_name='courseoverview',
            name='Duration',
            field=models.IntegerField(default=60),
        ),
        migrations.AddField(
            model_name='courseoverview',
            name='FocusArea',
            field=models.TextField(default=b'Buddy'),
        ),
    ]