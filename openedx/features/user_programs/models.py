# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import json
import datetime
from django.contrib.auth.models import User
from django.utils import timezone
from student.models import (
    CourseIdentifier
)
from enums import ProgramPaceChoice, EntityGroupChoice

# Create your models here.
class EntityGroup(models.Model):
    class Meta(object):
        db_table = "entitygroup_entitygroup"
        verbose_name = 'Entity Group'
    
    program_name = models.CharField(max_length=100)
    learning_points = models.TextField(null=True)
    program_overview = models.TextField(null=True)
    program_instructions = models.TextField(null=True)
    instructors = models.TextField(null=True)
    program_schedule = models.TextField(null=True)
    program_sessions = models.TextField(null=True, blank=True)
    program_pace = models.CharField(max_length=50, choices = [(tag.name, tag.value) for tag in ProgramPaceChoice], default="Instructor")
    duration = models.CharField(max_length=100)
    weekly_duration = models.CharField(max_length=100,null=True)
    image_url = models.CharField(max_length=256)
    identifier = models.ForeignKey(CourseIdentifier,null=False,related_name="programlist_identifier",on_delete=models.CASCADE)
    start_date = models.DateTimeField(null=False)
    end_date = models.DateTimeField(null=False)
    is_active = models.BooleanField(default=0)
    focus_area = models.CharField(max_length=100)
    tags = models.CharField(max_length = 100, null=True)
    entity_group_type = models.CharField(max_length=50, choices = [(tag.name, tag.value) for tag in EntityGroupChoice], default="Program")
    support=models.TextField(null=True)
    created_date = models.DateTimeField(null=False)
    last_modified_date = models.DateTimeField(null=False, default=timezone.now)
    organization_logo_url = models.TextField(null=True , blank=True)

    def __unicode__(self):
        """Represent ourselves with the course key."""
        return unicode(self.program_name)


class UserEntityGroupMapping(models.Model):
    class Meta(object):
        db_table = "entitygroup_userentitygroupmapping"
        verbose_name = 'User EntityGroup Mapping'
    
    user = models.ForeignKey(User,null=False,related_name="userprogram_user",on_delete=models.CASCADE)
    entity_group = models.ForeignKey(EntityGroup,null=False,related_name="userprogram_user",on_delete=models.CASCADE)
    is_active = models.BooleanField(default=1)
    created_date = models.DateTimeField(null=True, default=timezone.now)
    last_modified_date = models.DateTimeField(null=True, default=timezone.now)

    @classmethod
    def get_programs_by_user(cls, user):
        return cls.objects.filter(user=user,is_active=True)

    @classmethod
    def unenroll_ifProgram(cls, identifier, user):
        return_object = {}
        return_object['program_name'] = None
        #get program for the user
        programs = EntityGroup.objects.filter(identifier=identifier)
        #chech if programs exist
        if programs.exists():
            program = programs.first()
            return_object['program_name'] = program.program_name
            if cls.objects.filter(user=user,entity_group=programs.first()).exists():
                return_object['already_enrolled'] = True
                user_program = cls.objects.filter(user=user,entity_group=programs.first()).update(is_active=0, last_modified_date=datetime.datetime.utcnow())
                return_object['unenrollstatus'] = True
            else : 
                return_object['already_enrolled'] = False
                return_object['unenrollstatus'] = False
        return return_object

    @classmethod
    def enroll_ifProgram(cls, identifier, user):
        return_object = {}
        return_object['program_name'] = None
        programs = EntityGroup.objects.filter(identifier=identifier)
        if programs.exists():
            program = programs.first()
            return_object['program_name'] = program.program_name
            existing_enrollments = cls.objects.filter(user=user,entity_group=program)
            if existing_enrollments.exists():
                if not existing_enrollments.first().is_active:
                    enrollment = existing_enrollments.first()
                    enrollment.is_active = True
                    enrollment.last_modified_date = datetime.datetime.utcnow()
                    enrollment.save()
                return_object['already_enrolled'] = True
            else : 
                return_object['already_enrolled'] = False
                user_program = cls()
                user_program.user = user
                user_program.entity_group = program
                user_program.created_date = datetime.datetime.utcnow()
                user_program.last_modified_date = datetime.datetime.utcnow()
                user_program.save()
                
        return return_object