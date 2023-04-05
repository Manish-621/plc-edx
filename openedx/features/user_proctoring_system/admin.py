# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import ProctoringData, ProctoringConfiguration, UserProctoringConfiguration

# Register your models here.
class ProctoringDataAdmin(admin.ModelAdmin):
    list_display= ['user',
                    'proctored_attempt',
                    'event',
                    'timestamp',
                    'status']

class ProctoringConfigurationAdmin(admin.ModelAdmin):
    list_display= ['proctored_exam',
                    'blur_count',
                    'blur_duration',
                    'disable_copy_paste']

class UserProctoringConfigurationAdmin(admin.ModelAdmin):
    list_display= ['user',
                    'proctored_exam',
                    'blur_count',
                    'blur_duration',
                    'disable_copy_paste']
    search_fields = ['user__username','proctored_exam__exam_name','proctored_exam__course_id']

                    

admin.site.register(ProctoringData, ProctoringDataAdmin)
admin.site.register(ProctoringConfiguration, ProctoringConfigurationAdmin)
admin.site.register(UserProctoringConfiguration, UserProctoringConfigurationAdmin)