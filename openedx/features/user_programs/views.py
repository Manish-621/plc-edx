# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
from django.shortcuts import render
from django.shortcuts import render, render_to_response
import datetime
import json
from django.contrib.auth.decorators import login_required
from util.json_request import JsonResponse, JsonResponseBadRequest, expect_json
from .models import EntityGroup, UserEntityGroupMapping
from openedx.core.djangoapps.content.course_overviews.models import CourseOverview
from opaque_keys.edx.keys import CourseKey
from openedx.core.djangoapps.content.course_overviews.enums import CourseTypeChoice
from lms.djangoapps.instructor.views.api import _split_input_list, _get_boolean_param
from lms.djangoapps.instructor.views.tools import get_student_from_identifier
from openedx.features.user_programs import models as user_programs

from student.models import CourseEnrollment
# Create your views here.
@login_required
def get_faqs(request):    
    faqs= r'''[
        {   
            "title":"Support",
            "questions":[
                            {
                                "question":"Whom I should reach out to, if I face any technical glitch in the system ?",
                                "answer":"Please contact the technical support team through chat option available in bottom right corner of the screen. You can also email to the support team (mail id given in program landing page)."
                            }
                    ]
        },
        {   
            "title":"Course",
            "questions":[
                            {   
                                "question":"What if I could not complete my course within the end date mentioned, Can I access the course content after that ?",
                                "answer":"Yes, you can access till your training program is active. Please report to support team, in case any technical glitch."
                            }
                    ]
        },
        {   
            "title":"Assessments",
            "questions":[
                            {   
                                "question":"When is my Assessments are scheduled, and how will I know that there is an upcoming assessment?",
                                "answer":"You can see the list of assessments scheduled in your landing page under \"My Assessments\" section, and date will be mentioned beneath the \"Assessment Title\". You will also receive an email notification from SkillAssure support team 1 day prior to the assessment with the details."
                            },
                            {   
                                "question":"When I can access my Assessment ?",
                                "answer":"Assessments can be accessed only during the scheduled Date and Time. (Ex, If your \"Assessment 1\" is scheduled on 26-June-2020 from 5 PM to 6.30 PM, the same will be accessible during this schedule)."
                            }
                    ]
        },
        {   
            "title":"Programs",
            "questions":[
                            {   
                                "question":"How do online programs work?",
                                "answer":"Some programs are a combination of on-campus and online study, while other programs are offered totally online. Often students are allowed to create their own study schedules using class materials, such as taped lectures and slide show presentations, which are accessible 24-7 through an Internet-based portal. Through this platform, students can also find their assignments, upload homework and take up assessments."
                            }
                    ]
        },
        {   
            "title":"Tools & Technology",
            "questions":[
                            {   
                                "question":"What kind of tools and technology will I need?",
                                "answer":"Technology requirements vary according to the program, there may also be program- and course-specific requirements, such as specialized software for programing or design the information technology work. The course specific technology needs are detailed in course content (i.e., every course starts with the pre-requites of the course and user guide to set-up the same)"
                            }
                    ]
        }
    ]'''    
    context ={
        'user': request.user,  
        'faqs':faqs    
    }
    return render_to_response('faq.html',context)

@login_required
def get_programs_by_id(request, id):
    program = EntityGroup.objects.filter(id=id).first()
    courses = []
    assessments = []
    applications = []
    projects = []
    user = request.user
    #identifier = program.identifier.CourseKey
    for course_id in program.identifier.CourseKey.split(",") :
        #Enroll for laterly Added courses
        if not CourseEnrollment.is_enrolled(user, CourseKey.from_string(course_id)) :
            try:
                CourseEnrollment.enroll(user, CourseKey.from_string(course_id), mode='audit', check_access=True)
            except Exception :
                pass

        course = CourseOverview.objects.filter(id=CourseKey.from_string(course_id)).first()
        course_type = course.get_course_type()
        if course_type == CourseTypeChoice.Course.value:
            courses.append(course)
        elif course_type == CourseTypeChoice.Assessment.value :
            assessments.append(course)
        elif course_type == CourseTypeChoice.Application.value:
            applications.append(course)
        elif course_type == CourseTypeChoice.Project.value :
            projects.append(course)

    course_list = []
    course_section = {'entity':'Courses', 'list' : courses}
    course_list.append(course_section)
    course_section = {'entity':'Assessments', 'list' : assessments}
    course_list.append(course_section)
    course_section = {'entity':'Applications', 'list' : applications}
    course_list.append(course_section)
    course_section = {'entity':'Projects', 'list' : projects}
    course_list.append(course_section)

    program_sessions = None

    if program.program_sessions :
        #Get the sessions with dates ascending order
        program_sessions= sorted(json.loads(program.program_sessions), key=lambda d: datetime.datetime.strptime(d['startDate'], '%Y/%m/%d %H:%M')) 
        #Removing expired sission
        program_sessions= filter(lambda x: datetime.datetime.strptime(x['endDate'], '%Y/%m/%d %H:%M') > datetime.datetime.now(), program_sessions)

    


    context ={
        'user': request.user,
        #'program_key' : request.GET["program_key"],
        'program':program,
        'course_list':course_list,
        'courses_count' : len(courses),
        'program_sessions' : program_sessions

    }  
    return render_to_response('programs-view-details.html',context)


@login_required
def program_update_enrollment(request):
    program_identifer = int(request.POST["program_id"])
    program = EntityGroup.objects.filter(id=program_identifer).first()

    action = request.POST.get('action')
    identifiers_raw = request.POST.get('identifiers')
    identifiers = _split_input_list(identifiers_raw)
    auto_enroll = _get_boolean_param(request, 'auto_enroll')
    email_students = _get_boolean_param(request, 'email_students')
    reason = request.POST.get('reason')
    role = request.POST.get('role')
    
    results_courses = []
    results_program = []

    for course_id in program.identifier.CourseKey.split(",") :
        for identifier in identifiers:
            if not CourseEnrollment.is_enrolled(get_student_from_identifier(identifier), CourseKey.from_string(course_id)) :
                if(action == 'enroll'):
                    CourseEnrollment.enroll(get_student_from_identifier(identifier), CourseKey.from_string(course_id), mode='audit', check_access=True)
                    course_status = 'enrolled'               

            else :
                course_status = 'already enrolled'
                if(action == 'unenroll'):
                    CourseEnrollment.unenroll(get_student_from_identifier(identifier), CourseKey.from_string(course_id))
                    course_status = 'unenrolled'
            results_courses.append({
                'course_id': course_id,
                'identifier' : identifier,
                'course_status' : course_status
            })
    
    for identifier in identifiers:
        if(action == 'enroll'):
            program_status = user_programs.UserEntityGroupMapping.enroll_ifProgram(program.identifier,get_student_from_identifier(identifier))
        if(action == 'unenroll'):
            program_status = user_programs.UserEntityGroupMapping.unenroll_ifProgram(program.identifier,get_student_from_identifier(identifier))

        results_program.append({
            'identifier' : identifier,
            'program_status' : program_status
        })
    # api_enrollment
    return JsonResponse({'result':'true','course': results_courses, 'program': results_program})