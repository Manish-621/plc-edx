# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-10-28 10:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('code_editor', '0023_auto_20211018_0816'),
    ]

    operations = [
        migrations.AddField(
            model_name='codingquestion',
            name='test_cases_stdin',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='codingquestion',
            name='test_result_stdout',
            field=models.TextField(blank=True, null=True),
        ),
    ]
