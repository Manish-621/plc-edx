# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-06-26 04:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('code_editor', '0004_auto_20200625_0659'),
    ]

    operations = [
        migrations.AddField(
            model_name='codingresult',
            name='remarks',
            field=models.TextField(blank=True, null=True),
        ),
    ]
