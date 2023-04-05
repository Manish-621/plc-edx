# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import IDEExams, IDEExamAttempt

# Register your models here.
class IDEExamsAdmin(admin.ModelAdmin):
    list_display= ['proctored_exam',
                    'image_name',
                    'container_command',
                    'max_score',
                    'created_date',
                    'modified_date',
                    'is_active']

class IDEExamAttemptAdmin(admin.ModelAdmin):
    list_display= ['ide_exam',
                    'user',
                    'container_url',
                    'container_created_date',
                    'created_date',
                    'modified_date',
                    'is_active']

    search_fields = ['ide_exam__proctored_exam__exam_name','ide_exam__proctored_exam__course_id','user__username','user__email']


admin.site.register(IDEExams, IDEExamsAdmin)
admin.site.register(IDEExamAttempt, IDEExamAttemptAdmin)