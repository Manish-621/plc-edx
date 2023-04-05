# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-07-01 14:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('code_editor', '0006_merge_20200626_1907'),
    ]

    operations = [
        migrations.AddField(
            model_name='codingresult',
            name='unit_id',
            field=models.CharField(default='NA', max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='codingexams',
            name='coding_Languages_type',
            field=models.CharField(choices=[(b'BACKEND', b'BACKEND'), (b'DATABASE', b'DATABASE')], max_length=50),
        ),
    ]