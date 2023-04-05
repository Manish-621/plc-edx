# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import EntityGroup, UserEntityGroupMapping

# Register your models here.
class EntityGroupSetAdmin(admin.ModelAdmin):
    list_display= ['program_name',
                    'learning_points',
                    'program_overview',
                    'instructors',
                    'duration',
                    'image_url',
                    'identifier',
                    'focus_area',
                    'tags',
                    'start_date',
                    'end_date',
                    'is_active']
    search_fields = ['program_name']

class UserEntityGroupMappingSetAdmin(admin.ModelAdmin):
    list_display= ['user','entity_group']
    search_fields = ['user__username','entity_group__program_name']


admin.site.register(EntityGroup, EntityGroupSetAdmin)
admin.site.register(UserEntityGroupMapping, UserEntityGroupMappingSetAdmin)
