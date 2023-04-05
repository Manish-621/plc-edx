# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-06-03 04:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_programs', '0007_merge_20200601_1207'),
    ]

    operations = [
        migrations.AddField(
            model_name='program',
            name='program_pace',
            field=models.CharField(choices=[(b'Instructor', b'INSTRUCTOR'), (b'Self', b'SELF')], default='INSTRUCTOR', max_length=50),
        ),
    ]
