# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-05-21 18:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course_overviews', '0023_merge_20200520_1118'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursecustomdetails',
            name='course_type_choice',
            field=models.CharField(choices=[(b'Application', b'APPLICATION'), (b'Assessment', b'ASSESSMENT'), (b'Course', b'COURSE'), (b'Project', b'PROJECT')], default='Course', max_length=50),
            preserve_default=False,
        ),
    ]
