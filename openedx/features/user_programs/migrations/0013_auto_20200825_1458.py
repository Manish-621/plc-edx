# -*- coding: utf-8 -*-
# Generated by Django 1.11.27 on 2020-08-25 14:58
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_programs', '0012_auto_20200825_1455'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Program',
            new_name='EntityGroup',
        ),
        migrations.RenameModel(
            old_name='UserPrograms',
            new_name='UserEntityGroupMapping',
        ),
    ]
