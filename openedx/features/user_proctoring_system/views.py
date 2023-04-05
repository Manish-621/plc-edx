# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, render_to_response
import datetime
from django.contrib.auth.decorators import login_required
from util.json_request import JsonResponse, JsonResponseBadRequest, expect_json
from edx_proctoring.api import (
    get_all_exams_for_course,
    get_exam_by_content_id,
    get_exam_by_id
)
from edx_proctoring.models import ProctoredExam, ProctoredExamStudentAttempt, ProctoredExamStudentAttemptManager
from edx_proctoring.statuses import ProctoredExamStudentAttemptStatus
from models import ( ProctoringData )
from openedx.core.djangoapps.content.course_overviews.models import CourseOverview
from lms.djangoapps.grades.course_grade_factory import CourseGradeFactory
from courseware.courses import can_self_enroll_in_course, get_course_info_section, get_course_with_access
from xmodule.exceptions import NotFoundError
from opaque_keys.edx.keys import CourseKey

proctoring_manager = ProctoredExamStudentAttempt.objects

@login_required
def logBlur(request) :
    exam_id = request.POST.get('examId')
    blur_count = request.POST.get('bC01')
    blur_duration = request.POST.get('bD01')
    user = request.user
    incomplete_exam = proctoring_manager.get_exam_attempt(exam_id,user.pk)
    if incomplete_exam.status != ProctoredExamStudentAttemptStatus.submitted :
        timestamp = datetime.datetime.utcnow()
        ProctoringData.create_blur_instance(user, incomplete_exam, timestamp, blur_count, blur_duration)
    return JsonResponse({'success': True})

@login_required
def logFocus(request) :
    exam_id = request.POST.get('examId')
    blur_count = request.POST.get('bC01')
    blur_duration = request.POST.get('bD01')
    user = request.user
    incomplete_exam = proctoring_manager.get_exam_attempt(exam_id,user.pk)
    if incomplete_exam.status != ProctoredExamStudentAttemptStatus.submitted :
        timestamp = datetime.datetime.utcnow()
        ProctoringData.create_focus_instance(user, incomplete_exam, timestamp, blur_count, blur_duration)
    return JsonResponse({'success': True})

@login_required
def endExam(request) :
    exam_id = request.POST.get('examId')
    blur_count = request.POST.get('bC01')
    blur_duration = request.POST.get('bD01')
    is_count = request.POST.get('is_cnt')
    user = request.user
    incomplete_exam = proctoring_manager.get_exam_attempt(exam_id,user.pk)
    if incomplete_exam.status != ProctoredExamStudentAttemptStatus.submitted :
        timestamp = datetime.datetime.utcnow()
        setattr(incomplete_exam,'status',ProctoredExamStudentAttemptStatus.submitted)
        setattr(incomplete_exam,'completed_at', timestamp)
        incomplete_exam.save()
        if is_count == 'true' :
            ProctoringData.create_blurCountViolation_instance(user, incomplete_exam, timestamp, blur_count, blur_duration)
        else :
            ProctoringData.create_blurDurationViolation_instance(user, incomplete_exam, timestamp, blur_count, blur_duration)
    return JsonResponse({'success': True})

@login_required
def endExamView(request) :
    return render_to_response('end-exam-page.html')

@login_required
def timedExams(request):
    if not (request.user.is_superuser or request.user.is_staff) :
        raise NotFoundError('Unauthorized Request')

    courses_data = CourseOverview.objects.filter()
    courses = []
    for course_data in courses_data :
        
        course_key = getattr(course_data,'id')

        course = {}
        course['course_name'] = getattr(course_data,'display_name')
        course['course_id'] = course_key
        exams = []
        timed_exams = get_all_exams_for_course(course_key)
        course_data = get_course_with_access(request.user, 'load', course_key)
        for timed_exam in timed_exams :
            exam = {}
            exam['id'] = timed_exam['id']
            exam['course_id'] = timed_exam['course_id']
            exam['content_id'] = timed_exam['content_id']
            exam['exam_name'] = timed_exam['exam_name']
            exam['time_limit'] = timed_exam['time_limit_mins']
            exam['is_proctored'] = timed_exam['hide_after_due']
            exam['is_active'] = timed_exam['is_active']
            
            exam_attempts = ProctoredExamStudentAttempt.objects.filter(proctored_exam__id = timed_exam['id'])
            exam['attempts_count'] = len(exam_attempts)
            exams.append(exam)
        
        course['exams'] = exams
        courses.append(course)

    context ={
        'courses':courses
    }
    return render_to_response('timed-exams.html', context)

@login_required
def examResult(request,id):

    if not (request.user.is_superuser or request.user.is_staff) :
        raise NotFoundError('Unauthorized Request')

    exam = get_exam_by_id(id)

    course_key = CourseKey.from_string(exam['course_id'])
    course_data = get_course_with_access(request.user, 'load', course_key)
    attempts = []
    exam_attempts = ProctoredExamStudentAttempt.objects.filter(proctored_exam__id = exam['id'])
    for exam_attempt in exam_attempts :
        course_grades = CourseGradeFactory().read(exam_attempt.user, course_data)
        grade = course_grades.get_subsection_location(exam['content_id'])
        attempt = {}
        attempt['id'] = exam_attempt.id
        attempt['user'] = exam_attempt.user
        attempt['status'] = exam_attempt.status
        attempt['time_limit'] = exam_attempt.allowed_time_limit_mins
        attempt['start'] = exam_attempt.started_at
        attempt['end'] = exam_attempt.completed_at
        attempt['is_forcedEnd'] = ProctoringData.is_exam_forcedEnd(exam_attempt)
        attempt['score'] = grade
        attempt['blur_data'] = ProctoringData.get_blur_data_summary(exam_attempt)
        attempts.append(attempt)

    context ={
        'exam':exam,
        'attempts':attempts,
        'course_name':course_data.display_name
    }
    return render_to_response('timed-exam-attempts.html', context)

@login_required
def get_exam_details(request, id):

    if not (request.user.is_superuser or request.user.is_staff) :
        raise NotFoundError('Unauthorized Request')
        
    attempt = proctoring_manager.get_exam_attempt_by_id(id)
    if not attempt :
        raise NotFoundError('Attempt not found')
    blur_data = ProctoringData.get_full_blur_data(attempt)
    blur_summary = ProctoringData.get_blur_data_summary(attempt)

    course_key = CourseKey.from_string(attempt.proctored_exam.course_id)
    course_data = get_course_with_access(request.user, 'load', course_key)
    course_grades = CourseGradeFactory().read(attempt.user, course_data)
    grades = course_grades.get_subsection_location(attempt.proctored_exam.content_id)
    #attempt[]
    context ={
        'attempt':attempt,
        'blur_data' : blur_data,
        'blur_summary' : blur_summary,
        'grades':grades,
        'course_name':course_data.display_name
    }
    return render_to_response('student-exam-details.html', context)