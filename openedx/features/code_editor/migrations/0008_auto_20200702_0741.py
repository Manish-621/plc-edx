# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-07-02 07:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('code_editor', '0007_auto_20200701_1412'),
    ]

    operations = [
        migrations.AlterField(
            model_name='codingexams',
            name='coding_Languages',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
    ]
