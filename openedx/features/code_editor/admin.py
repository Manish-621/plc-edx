# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import CodingQuestion, CodingResult, DefaultSnippet

# Register your models here.
class CodingQuestionAdmin(admin.ModelAdmin):
    list_display= ['proctored_exam',
                    'max_score',
                    'coding_Languages_type',
                    'coding_Languages',
                    'evaluvation_parameters',
                    'modified',
                    'is_active']
    search_fields = ['proctored_exam__exam_name','proctored_exam__course_id','coding_Languages','coding_Languages_type']

class CodingResultAdmin(admin.ModelAdmin):
    list_display= ['user',
                    'coding_exam',
                    'question_id',
                    'snippet_id',
                    'snippet_url',
                    'score',
                    'is_graded',
                    'created',
                    'modified',]
    readonly_fields = ['user','coding_exam', 'question_id','snippet_id','snippet_url']
    search_fields = ['coding_exam__proctored_exam__exam_name','coding_exam__proctored_exam__course_id','user__username','user__email']


class DefaultSnippetAdmin(admin.ModelAdmin):
    list_display= ['snippet_name',
                    'snippet_id',
                    'coding_language',
                    'coding_Languages_type']
    search_fields = ['snippet_name','snippet_id','coding_language','coding_Languages_type']

admin.site.register(CodingQuestion, CodingQuestionAdmin)
admin.site.register(CodingResult, CodingResultAdmin)
admin.site.register(DefaultSnippet, DefaultSnippetAdmin)
