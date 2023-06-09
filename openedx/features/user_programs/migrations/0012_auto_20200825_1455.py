# -*- coding: utf-8 -*-
# Generated by Django 1.11.27 on 2020-08-25 14:55
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_programs', '0011_program_program_sessions'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='program',
            options={'verbose_name': 'Entity Group'},
        ),
        migrations.AlterModelOptions(
            name='userprograms',
            options={'verbose_name': 'User EntityGroup Mapping'},
        ),
        migrations.AlterModelTable(
            name='program',
            table='entitygroup_entitygroup',
        ),
        migrations.AlterModelTable(
            name='userprograms',
            table='entitygroup_userentitygroupmapping',
        ),
    ]
