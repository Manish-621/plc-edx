# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import UserBatch, UserBatchMapping
# Register your models here.
class UserBatchSetAdmin(admin.ModelAdmin):
    list_display= ['organization',
                    'batch_name',
                    'batch_description',
                    'is_active',
                    'created_date',
                    'last_modified_date']

    search_fields = ['organization__name','batch_name']

class UserBatchMappingSetAdmin(admin.ModelAdmin):
    list_display= ['user','user_batch']
    search_fields = ['user','user_batch']


admin.site.register(UserBatch, UserBatchSetAdmin)
admin.site.register(UserBatchMapping, UserBatchMappingSetAdmin)