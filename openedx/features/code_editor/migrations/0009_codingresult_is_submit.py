# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-07-02 14:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('code_editor', '0008_auto_20200702_0741'),
    ]

    operations = [
        migrations.AddField(
            model_name='codingresult',
            name='is_submit',
            field=models.BooleanField(default=False),
        ),
    ]
