# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-10-19 14:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course_overviews', '0028_auto_20201001_1353'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursecustomdetails',
            name='Tags',
            field=models.TextField(blank=True, null=True),
        ),
    ]