# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-05-11 12:31
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_proctoring_system', '0002_auto_20200511_0958'),
    ]

    operations = [
        migrations.AlterField(
            model_name='proctoringdata',
            name='proctored_attempt',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='proctoringdata_exam', to='edx_proctoring.ProctoredExamStudentAttempt'),
        ),
        migrations.AlterField(
            model_name='proctoringdata',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='proctoringdata_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
