# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import json
from django.contrib.auth.models import User
from edx_proctoring.models import ProctoredExam, ProctoredExamStudentAttempt

# Create your models here.
class ProctoringData(models.Model):
    class Meta(object):
        db_table = "proctoringsystem_proctoringdata"
        verbose_name = 'proctoring system data'
    
    user = models.ForeignKey(User,null=False,related_name="proctoringdata_user",on_delete=models.CASCADE)
    proctored_attempt = models.ForeignKey(ProctoredExamStudentAttempt,null=True,db_index=True,related_name="proctoringdata_exam",on_delete=models.CASCADE)
    event = models.CharField(max_length=100)
    timestamp = models.DateTimeField(null=False)
    status = models.TextField(null=True)

    @classmethod
    def create_blur_instance(cls, user, proctored_attempt, timestamp, blur_count, blur_duration):
        status = {}
        status['blur_count'] = blur_count
        status['blur_duration'] = blur_duration
        status_json = json.dumps(status)
        return cls.objects.create(
            user = user,
            proctored_attempt = proctored_attempt,
            event = 'BLUR',
            timestamp = timestamp,
            status = status_json
        )
    
    @classmethod
    def create_focus_instance(cls, user, proctored_attempt, timestamp, blur_count, blur_duration):
        status = {}
        status['blur_count'] = blur_count
        status['blur_duration'] = blur_duration
        status_json = json.dumps(status)
        return cls.objects.create(
            user = user,
            proctored_attempt = proctored_attempt,\
            event = 'FOCUS',
            timestamp = timestamp,
            status = status_json
        )
    
    @classmethod
    def create_blurCountViolation_instance(cls, user, proctored_attempt, timestamp, blur_count, blur_duration):
        status = {}
        status['violation_type'] = 'BLUR_COUNT'
        status['blur_count'] = blur_count
        status['blur_duration'] = blur_duration
        status_json = json.dumps(status)
        return cls.objects.create(
            user = user,
            proctored_attempt = proctored_attempt,
            event = 'FORCE_END',
            timestamp = timestamp,
            status = status_json
        )
    
    @classmethod
    def create_blurDurationViolation_instance(cls, user, proctored_attempt, timestamp, blur_count, blur_duration):
        status = {}
        status['violation_type'] = 'BLUR_DURATION'
        status['blur_count'] = blur_count
        status['blur_duration'] = blur_duration
        status_json = json.dumps(status)
        return cls.objects.create(
            user = user,
            proctored_attempt = proctored_attempt,
            event = 'FORCE_END',
            timestamp = timestamp,
            status = status_json
        )
    
    @classmethod
    def is_exam_forcedEnd(cls, proctored_attempt) :
        events = cls.objects.filter(proctored_attempt = proctored_attempt,event='FORCE_END')
        if events :
            return True
        return False
    
    @classmethod
    def get_blur_data_summary(cls, proctored_attempt) :
        events = cls.objects.filter(proctored_attempt = proctored_attempt).order_by('-id')
        if events.exists() :
            return json.loads(events.first().status)
        return json.loads('{}')
    
    @classmethod
    def get_full_blur_data(cls, proctored_attempt) :
        events = cls.objects.filter(proctored_attempt = proctored_attempt).order_by('id')
        return events

class ProctoringConfiguration(models.Model):
    proctored_exam = models.OneToOneField(ProctoredExam,null=True,db_index=True,related_name="proctoringconfiguration_exam",on_delete=models.CASCADE)
    blur_count = models.IntegerField(null=False,default=5)
    blur_duration = models.IntegerField(null=False,default=120)
    blur_restriction = models.BooleanField(null=False,default=True)
    force_fullscreen = models.BooleanField(null=False,default=True)
    disable_copy_paste = models.BooleanField(null=False,default=True)
    enable_camera = models.BooleanField(null=False, default=True)
    pop_up_window = models.BooleanField(null=False, default=True)

    @classmethod
    def get_proctoring_parameters(cls, proctored_exam):
        
        if proctored_exam['hide_after_due'] and proctored_exam['is_active']:
            exams = cls.objects.filter(proctored_exam_id=proctored_exam['id'])
            if exams.exists():
                return exams.first()
            else:
                exam = cls()
                exam.blue_count = 5
                exam.blur_duration = 120
                exam.disable_copy_paste = True
                exam.enable_camera = True
                return exam
        else :
            return None

class UserProctoringConfiguration(models.Model):
    user = models.ForeignKey(User,null=False,related_name="userproctoringconfiguration_user",on_delete=models.CASCADE)
    proctored_exam = models.ForeignKey(ProctoredExam,null=False,db_index=True,related_name="userproctoringconfiguration_exam",on_delete=models.CASCADE)
    blur_count = models.IntegerField(null=False,default=5)
    blur_duration = models.IntegerField(null=False,default=120)
    blur_restriction = models.BooleanField(null=False,default=True)
    force_fullscreen = models.BooleanField(null=False,default=True)
    disable_copy_paste = models.BooleanField(null=False,default=True)
    enable_camera = models.BooleanField(null=False, default=True)
    pop_up_window = models.BooleanField(null=False, default=True)
    reason = models.TextField(null=False)

    @classmethod
    def get_user_proctoring_parameters(cls, proctored_exam, user):
        #import ipdb; ipdb.set_trace()
        if proctored_exam['hide_after_due'] and proctored_exam['is_active']:
            exams = cls.objects.filter(proctored_exam_id=proctored_exam['id'], user_id = user.id)
            if exams.exists():
                return exams.first()
        return ProctoringConfiguration.get_proctoring_parameters(proctored_exam)