# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
import datetime
from django.utils import timezone
import requests
from edx_proctoring.models import ProctoredExam
from django.conf import settings
from xmodule.exceptions import NotFoundError

# Create your models here.
class IDEExams(models.Model):
    class Meta(object):
        db_table = 'ide_ideexam'
        verbose_name = 'IDE Exam'

    proctored_exam = models.OneToOneField(ProctoredExam,null=True,db_index=True,related_name="ideexam_exam",on_delete=models.CASCADE)
    image_name = models.CharField(max_length=100)
    container_command = models.CharField(max_length=200, null=True, blank=True)
    server_ip = models.CharField(max_length=20, null=True, blank=True)
    is_embedded = models.BooleanField(null=False,default=True)
    max_score = models.IntegerField(null=False)
    created_date = models.DateTimeField(null=False, default=timezone.now)
    modified_date = models.DateTimeField(null=False, default=timezone.now)
    is_active = models.BooleanField(null=False,default=True)
    enable_git_oauth = models.BooleanField(null=False,default=False)

    git_fork_repository = models.CharField(max_length=100, null=True, blank=True)

    def __unicode__(self):
        """Represent ourselves with the course key."""
        return unicode(self.proctored_exam)

    @classmethod
    def get_ide_exam(cls, proctored_exam):
        exams = cls.objects.filter(proctored_exam_id=proctored_exam['id'])
        if exams.exists():
            exam = exams.first()
            if exam.is_active :
                return exam
        return None
    
    @classmethod
    def get_ide_handsOn(cls, course_id):
        exams = cls.objects.filter(proctored_exam__course_id=course_id)
        if exams.exists():
            exam = exams.first()
            if exam.is_active :
                return exam
        return None


class IDEExamAttempt(models.Model):
    class Meta(object):
        db_table = 'ide_ideexam_attempt'
        verbose_name = 'IDE Exam Attempt'

    ide_exam = models.ForeignKey(IDEExams,null=False,related_name="ide_attempt_exam",on_delete=models.CASCADE)
    user = models.ForeignKey(User,null=False,related_name="ide_attempt_user",on_delete=models.CASCADE)
    container_url = models.CharField(max_length=200,null=True, blank=True)
    container_created_date = models.DateTimeField(null=True, blank=True)
    container_port = models.CharField(max_length=10, null=True, blank=True)
    created_date = models.DateTimeField(null=False, default=timezone.now)
    modified_date = models.DateTimeField(null=False, default=timezone.now)
    is_active = models.BooleanField(null=False,default=True)
    git_detais = models.TextField(null=True, blank=True)

    @classmethod
    def get_ide_url(cls, ide_exam, user):
        user_exams = cls.objects.filter(user=user,ide_exam=ide_exam)
        if user_exams.exists():
            user_exam = user_exams.first()
        else :
            user_exam = cls()
            user_exam.ide_exam = ide_exam
            user_exam.user = user
        if user_exam.container_url is None or not user_exam.is_active:
            url = settings.AZURE_CLI_API_URL+'/api/v1/containers/create?containerGroup='+str(ide_exam.proctored_exam.exam_name+'_'+user.username+'_'+str(ide_exam.id)).replace(' ','')+'&&imageName='+ide_exam.image_name
            headers = {
                    'Content-Type':'application/json'
                }
            try :
                response = requests.get(url, headers=headers)
            except :
                raise NotFoundError('Container creation error. URL:'+url)
            if response.status_code not in [200,201,202]:
                raise NotFoundError('Container creation error. URL:'+url)
            user_exam.container_url  = 'http://'+response.content
            user_exam.container_created_date = datetime.datetime.utcnow()
            user_exam.modified_date = datetime.datetime.utcnow()
            user_exam.is_active = True
            user_exam.save()    
        return user_exam.container_url

    @classmethod
    def get_IDE_Attempt(cls, ide_exam, user):
        user_exams = cls.objects.filter(user=user,ide_exam=ide_exam)
        if user_exams.exists():
            user_exam = user_exams.first()
            if user_exam.is_active:
                return user_exam
        return None

    @classmethod
    def deletecontainer(cls, container_group, user):
        url = settings.AZURE_CLI_API_URL+'/api/v1/containers/delete?containerGroup='+container_group
        headers = {
                'Content-Type':'application/json'
            }
        try :
            response = requests.get(url, headers=headers)
        except :
            raise NotFoundError('Container deletion error')
        if response.status_code not in [200,201,202]:
            raise NotFoundError('Container deletion error')
        return response

    @classmethod
    def clearContainerUrl(cls, ide_exam_id, user):
        IDEExam= IDEExams.objects.filter(id = ide_exam_id).first()
        user_exams = cls.objects.filter(user=user,ide_exam=IDEExam)
        if user_exams.exists():
            user_exam = user_exams.first()
            user_exam.container_url=None
            user_exam.save()

    @classmethod
    def saveGitInfo(cls, user ,examId, git_details):
        IDEExam= IDEExams.objects.filter(id = examId).first()
        user_exams = cls.objects.filter(user=user,ide_exam=IDEExam)
        if user_exams.exists():
            user_exam = user_exams.first()
            user_exam.git_detais = git_details
            user_exam.save()
            return None
        else :
            user_exam = cls()
            user_exam.ide_exam = IDEExam
            user_exam.user = user
            user_exam.git_detais = git_details
            user_exam.created_date = datetime.datetime.utcnow()
            user_exam.modified_date = datetime.datetime.utcnow()
            user_exam.is_active = True
            user_exam.save()
            return None



    