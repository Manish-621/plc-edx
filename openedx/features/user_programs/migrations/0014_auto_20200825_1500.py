# -*- coding: utf-8 -*-
# Generated by Django 1.11.27 on 2020-08-25 15:00
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_programs', '0013_auto_20200825_1458'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userentitygroupmapping',
            old_name='program',
            new_name='entity_group',
        ),
    ]
