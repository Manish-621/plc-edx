# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2021-10-18 08:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('code_editor', '0022_defaultsnippet_coding_language'),
    ]

    operations = [
        migrations.AlterField(
            model_name='codingquestion',
            name='default_snippet_id',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='codingquestion',
            name='result_snippet_id',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]