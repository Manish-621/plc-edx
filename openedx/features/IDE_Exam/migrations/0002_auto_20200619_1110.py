# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-06-19 11:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IDE_Exam', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='ideexamattempt',
            name='container_port',
            field=models.CharField(default=0, max_length=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ideexams',
            name='server_ip',
            field=models.CharField(default=0, max_length=20),
            preserve_default=False,
        ),
    ]