# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid
from django.db import models
from django.contrib.auth.models import User
import datetime
from edx_proctoring.models import ProctoredExam
from django.conf import settings
from enums import CodingLanguagesType
from xmodule.exceptions import ProcessingError

# Create your models here.
class CodingQuestion(models.Model):
    class Meta(object):
        db_table = "coding_questions"
        verbose_name = 'Coding Question'
    proctored_exam = models.ForeignKey(ProctoredExam,null=True,db_index=True,related_name="codingexam_exam",on_delete=models.CASCADE)
    unit_id = models.CharField(max_length=200)
    question_id = models.CharField(max_length=200)
    coding_Languages_type = models.CharField(max_length=50, choices = [(tag.name, tag.value) for tag in CodingLanguagesType],null=False)
    coding_Languages = models.CharField(max_length=200 ,null=False,default="", blank=True)
    enable_code_run = models.BooleanField(null=False,default=True)
    enable_copy_paste = models.BooleanField(null=False,default=False)
    evaluvation_parameters = models.TextField(null=True, blank=True)
    additional_information = models.TextField(null=True, blank=True)
    # test_cases_stdin = models.TextField(null=True, blank=True)
    # test_result_stdout = models.TextField(null=True, blank=True)
    max_score = models.IntegerField(null=False)
    created = models.DateTimeField(null=False)
    modified = models.DateTimeField(null=False)
    auto_evaluation = models.BooleanField(null=False,default=True)
    default_snippet_id = models.CharField(max_length=500, null=True, blank=True)
    result_snippet_id = models.CharField(max_length=500, null=True, blank=True)
    allow_main_method = models.BooleanField(null=False,default=True)
    is_active = models.BooleanField(null=False,default=True)


    def __unicode__(self):
        """Represent ourselves with the course key."""
        return unicode(self.proctored_exam)

    @classmethod
    def enable_code_editor(cls, proctored_exam):
        exams = cls.objects.filter(proctored_exam_id=proctored_exam['id'],is_active=1)
        if exams.exists():
            exam = exams.first()
            return exam.id
        return None

    @classmethod
    def enable_code_editor_question(cls, proctored_exam, unitid):
        exams = cls.objects.filter(proctored_exam_id=proctored_exam['id'],is_active=1,unit_id=unitid)
        if exams.exists():
            exam = exams.first()
            return exam.id
        return None

    @classmethod
    def get_coding_question(cls, proctored_exam,unit_id):
        exams = cls.objects.filter(proctored_exam_id=proctored_exam['id'], unit_id=unit_id)
        if exams.exists():
            return exams.first()
        return None

    @classmethod
    def has_coding_questions(cls, proctored_exam):
        exams = cls.objects.filter(proctored_exam_id=proctored_exam['id'], is_active=1)
        if exams.exists():
            return True
        return False

    @classmethod
    def get_codingexambyid(cls,id):
        exams = cls.objects.filter(pk=id)
        if exams.exists():
            return exams.first()
        return None

    @classmethod
    def get_codingexambyUnitid(cls,subsection_id, unit_id):
        exams = cls.objects.filter(proctored_exam__content_id=subsection_id,unit_id=unit_id)
        if exams.exists():
            return exams.first()
        return None

    @classmethod
    def get_allcodingexambyexam(cls,exam_name):
        exams = cls.objects.filter(proctored_exam=exam_name)
        if exams.exists():
            return exams
        return None

    @classmethod
    def get_all_questions_course(cls, course_key):
            return cls.objects.filter(proctored_exam__course_id=course_key)


class CodingResult(models.Model):
    class Meta(object):
        db_table = "coding_studentattempt"
        verbose_name = 'Coding Attempt'
    user = models.ForeignKey(User,null=False,related_name="coding_attempt_user",on_delete=models.CASCADE)
    coding_exam = models.ForeignKey(CodingQuestion,null=False,related_name="coding_attempt_exam",on_delete=models.CASCADE)
    question_id = models.CharField(max_length=200)
    unit_id = models.CharField(max_length=200)
    snippet_id = models.CharField(max_length=50)
    snippet_url = models.CharField(max_length=100)
    snippet_text = models.TextField(null=True)
    snippet_language = models.CharField(max_length=100)
    score = models.CharField(max_length=100,null=True, blank=True)
    result = models.CharField(max_length=100,null=True, blank=True)
    grade = models.CharField(max_length=100,null=True, blank=True)
    is_graded = models.BooleanField(null=False,default=False)
    created = models.DateTimeField(null=False)
    modified = models.DateTimeField(null=False)
    evaluation_details = models.TextField(null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)
    is_submit = models.BooleanField(null=False,default=False)


    @classmethod
    def request_save(cls, user, coding_exam, unit_id):
        results = cls.objects.filter(user=user,coding_exam=coding_exam,is_submit=True)
        if results.exists():
            raise ProcessingError('Response already submitted. Cannot Alter.')
        return False

    @classmethod
    def save_result(cls, user, coding_exam, question_id, snippet_id, unit_id, is_submit, content, language):
        results = cls.objects.filter(user=user,coding_exam=coding_exam)
        if results.exists():
            result = results.first()
            if result.is_submit:
                raise ProcessingError('Response already submitted. Cannot Alter.')
            result.snippet_id = snippet_id
            result.snippet_text = content
            result.snippet_language = language
            result.snippet_url = settings.GLOT_SNIPPET_URL+'/snippets/'+str(snippet_id)
            result.modified = datetime.datetime.utcnow()
            result.is_submit = is_submit
            result.question_id = question_id
            result.save()
            return True

        result = cls()
        result.user=user
        result.unit_id=unit_id
        result.coding_exam = coding_exam
        result.question_id = question_id
        result.snippet_id = snippet_id
        result.snippet_url = settings.GLOT_SNIPPET_URL+'/snippets/'+str(snippet_id)
        result.created = datetime.datetime.utcnow()
        result.modified = datetime.datetime.utcnow()
        result.is_graded = False
        result.is_submit = is_submit
        result.save()
        return True


    @classmethod
    def getStudentsByCourseID(cls,coding_exam):
        results = cls.objects.filter(coding_exam=coding_exam)
        return results

    @classmethod
    def save_exam_score(cls, id, score , evaluvation_par, remarks):
        results = cls.objects.filter(id=id)
        if results.exists():
            result = results.first()
            result.score =  score;
            #result.evaluation_details=  evaluvation_par;
            result.remarks= remarks;
            result.is_graded =  True;
            result.save()
            return True

        return False

    @classmethod
    def get_submitted_questions(cls, proctored_exam, user):
        exam_id = proctored_exam['id']
        results = cls.objects.filter(coding_exam__proctored_exam__id=exam_id,user=user)
        saved = []
        submitted = []
        if results.exists():
            saved = [result.unit_id for result in results]
            submitted = [result.unit_id for result in results if result.is_submit]
        return saved,submitted

    @classmethod
    def get_attempts_count(cls,coding_exam):
        return len(cls.objects.filter(coding_exam=coding_exam))


# Model for default coding snippet
class DefaultSnippet(models.Model):
    class Meta(object):
        db_table = "default_snippets"
        verbose_name = 'Default Snippet'
    snippet_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    snippet_name = models.CharField(max_length=200)
    snippet_text = models.TextField(null=True)
    coding_language = models.CharField(max_length=200)
    coding_Languages_type = models.CharField(max_length=50, choices = [(tag.name, tag.value) for tag in CodingLanguagesType],null=False)

    # Get default snippet by id
    @classmethod
    def get_snippet(cls, snippet_id):
        snippets = cls.objects.filter(snippet_id=snippet_id)
        if snippets.exists():
            return snippets.first()
