# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-06-26 07:06
from __future__ import unicode_literals

from django.db import migrations, models
import openedx.features.code_editor.enums


class Migration(migrations.Migration):

    dependencies = [
        ('code_editor', '0003_auto_20200617_1301'),
    ]

    operations = [
        migrations.AddField(
            model_name='codingexams',
            name='coding_Languages_type',
            field=models.CharField(choices=[(b'BACKEND', b'BACKEND'), (b'DATABASE', b'DATABASE'), (b'UI', b'UI')], default=openedx.features.code_editor.enums.CodingLanguagesType(b'BACKEND'), max_length=50),
        ),
    ]