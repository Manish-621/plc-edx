# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-10-01 13:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course_overviews', '0027_coursecustomdetails_organization_logo_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursecustomdetails',
            name='organization_logo_url',
            field=models.TextField(blank=True, null=True),
        ),
    ]
