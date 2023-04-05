# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-10-21 20:30
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('edx_proctoring', '0009_proctoredexamreviewpolicy_remove_rules'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user_proctoring_system', '0009_proctoringconfiguration_force_fullscreen'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProctoringConfiguration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('blur_count', models.IntegerField(default=5)),
                ('blur_duration', models.IntegerField(default=120)),
                ('blur_restriction', models.BooleanField(default=True)),
                ('force_fullscreen', models.BooleanField(default=True)),
                ('disable_copy_paste', models.BooleanField(default=True)),
                ('enable_camera', models.BooleanField(default=True)),
                ('pop_up_window', models.BooleanField(default=True)),
                ('reason', models.TextField()),
                ('proctored_exam', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userproctoringconfiguration_exam', to='edx_proctoring.ProctoredExam')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userproctoringconfiguration_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]