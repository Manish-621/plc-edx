# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-06-23 06:15
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('organizations', '0006_auto_20171207_0259'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserBatch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('batch_name', models.CharField(max_length=100)),
                ('batch_description', models.TextField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=1)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('last_modified_date', models.DateTimeField(default=django.utils.timezone.now, null=True)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userbatch_organization', to='organizations.Organization')),
            ],
            options={
                'db_table': 'usermanagement_userbatches',
                'verbose_name': 'User Batches',
            },
        ),
        migrations.CreateModel(
            name='UserBatchMapping',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userbatchmapping_user', to=settings.AUTH_USER_MODEL)),
                ('user_batch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userbatchmapping_userbatch', to='user_management.UserBatch')),
            ],
            options={
                'db_table': 'usermanagement_userbatchmapping',
                'verbose_name': 'User Batch Mapping',
            },
        ),
    ]
