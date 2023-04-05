# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-06-26 07:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('code_editor', '0004_codingexams_coding_languages_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='codingexams',
            name='coding_Languages_type',
            field=models.CharField(choices=[(b'BACKEND', b'BACKEND'), (b'DATABASE', b'DATABASE'), (b'UI', b'UI')], max_length=50),
        ),
    ]
