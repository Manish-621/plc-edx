# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-06-03 05:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_programs', '0008_program_program_pace'),
    ]

    operations = [
        migrations.AlterField(
            model_name='program',
            name='program_pace',
            field=models.CharField(choices=[(b'Instructor', b'INSTRUCTOR'), (b'Self', b'SELF')], default='Instructor', max_length=50),
        ),
    ]
