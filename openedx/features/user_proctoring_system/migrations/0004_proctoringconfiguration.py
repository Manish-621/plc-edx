# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-05-27 10:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('edx_proctoring', '0009_proctoredexamreviewpolicy_remove_rules'),
        ('user_proctoring_system', '0003_auto_20200511_1231'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProctoringConfiguration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blur_count', models.IntegerField(default=5)),
                ('blur_duration', models.IntegerField(default=120)),
                ('disable_copy_paste', models.BooleanField(default=True)),
                ('proctored_exam', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='proctoringconfiguration_exam', to='edx_proctoring.ProctoredExam')),
            ],
        ),
    ]
