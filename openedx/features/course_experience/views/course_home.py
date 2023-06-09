"""
Views for the course home page.
"""
from django.db.models import Q
from django.urls import reverse
from django.template.context_processors import csrf
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control
from django.views.decorators.csrf import ensure_csrf_cookie
from opaque_keys.edx.keys import CourseKey
from web_fragments.fragment import Fragment

from courseware.courses import get_course_overview_with_access
from edx_proctoring.api import (
    get_all_exams_for_course,
    get_exam_by_content_id
)
from edx_proctoring.models import ProctoredExamStudentAttempt
#from contentstore.proctoring import get_time_limit_byCourseKey
from course_modes.models import get_cosmetic_verified_display_price
from courseware.access import has_access
from courseware.courses import can_self_enroll_in_course, get_course_info_section, get_course_with_access
from lms.djangoapps.commerce.utils import EcommerceService
from lms.djangoapps.course_goals.api import (
    get_course_goal,
    get_course_goal_options,
    get_goal_api_url,
    has_course_goal_permission
)
from lms.djangoapps.grades.course_grade_factory import CourseGradeFactory
from lms.djangoapps.courseware.exceptions import CourseAccessRedirect
from lms.djangoapps.courseware.views.views import CourseTabView
from openedx.core.djangoapps.plugin_api.views import EdxFragmentView
from openedx.core.djangoapps.util.maintenance_banner import add_maintenance_banner
from openedx.features.course_experience.course_tools import CourseToolsPluginManager
from openedx.features.course_duration_limits.access import generate_course_expired_fragment
from student.models import CourseEnrollment
from util.views import ensure_valid_course_key
from xmodule.course_module import COURSE_VISIBILITY_PUBLIC_OUTLINE, COURSE_VISIBILITY_PUBLIC

from .. import (
    LATEST_UPDATE_FLAG, SHOW_UPGRADE_MSG_ON_COURSE_HOME, USE_BOOTSTRAP_FLAG, COURSE_ENABLE_UNENROLLED_ACCESS_FLAG
)
from ..utils import get_course_outline_block_tree, get_resume_block
from .course_dates import CourseDatesFragmentView
from .course_home_messages import CourseHomeMessageFragmentView
from .course_outline import CourseOutlineFragmentView
from .course_sock import CourseSockFragmentView
from .latest_update import LatestUpdateFragmentView
from .welcome_message import WelcomeMessageFragmentView
from openedx.core.djangoapps.content.course_overviews.enums import CourseTypeChoice
from openedx.features.IDE_Exam.models import IDEExams, IDEExamAttempt
from util.json_request import JsonResponse, JsonResponseBadRequest, expect_json
import requests
import json
from django.conf import settings
from django.shortcuts import render, render_to_response
from django.http import HttpResponse

EMPTY_HANDOUTS_HTML = u'<ol></ol>'


class CourseHomeView(CourseTabView):
    """
    The home page for a course.
    """
    @method_decorator(ensure_csrf_cookie)
    @method_decorator(cache_control(no_cache=True, no_store=True, must_revalidate=True))
    @method_decorator(ensure_valid_course_key)
    @method_decorator(add_maintenance_banner)
    def get(self, request, course_id, **kwargs):
        """
        Displays the home page for the specified course.
        """
        return super(CourseHomeView, self).get(request, course_id, 'courseware', **kwargs)

    def uses_bootstrap(self, request, course, tab):
        """
        Returns true if the USE_BOOTSTRAP Waffle flag is enabled.
        """
        return USE_BOOTSTRAP_FLAG.is_enabled(course.id)

    def render_to_fragment(self, request, course=None, tab=None, **kwargs):
        course_id = unicode(course.id)
        home_fragment_view = CourseHomeFragmentView()
        return home_fragment_view.render_to_fragment(request, course_id=course_id, **kwargs)


class CourseHomeFragmentView(EdxFragmentView):
    """
    A fragment to render the home page for a course.
    """

    def _get_resume_course_info(self, request, course_id):
        """
        Returns information relevant to resume course functionality.

        Returns a tuple: (has_visited_course, resume_course_url)
            has_visited_course: True if the user has ever visted the course, False otherwise.
            resume_course_url: The URL of the 'resume course' block if the user has visited the course,
                otherwise the URL of the course root.

        """
        course_outline_root_block = get_course_outline_block_tree(request, course_id, request.user)
        resume_block = get_resume_block(course_outline_root_block) if course_outline_root_block else None
        has_visited_course = bool(resume_block)
        if resume_block:
            resume_course_url = resume_block['lms_web_url']
        else:
            resume_course_url = course_outline_root_block['lms_web_url'] if course_outline_root_block else None

        return has_visited_course, resume_course_url

    def _get_course_handouts(self, request, course):
        """
        Returns the handouts for the specified course.
        """
        handouts = get_course_info_section(request, request.user, course, 'handouts')
        if not handouts or handouts == EMPTY_HANDOUTS_HTML:
            return None
        return handouts

    def render_to_fragment(self, request, course_id=None, **kwargs):
        """
        Renders the course's home page as a fragment.
        """
        course_key = CourseKey.from_string(course_id)
        course = get_course_with_access(request.user, 'load', course_key)

        course_block_tree = get_course_outline_block_tree(
            request, course_id, request.user
        )
        course_overview = get_course_overview_with_access(
            request.user, 'load', course_key, check_if_enrolled=True
        )

        # Render the course dates as a fragment
        dates_fragment = CourseDatesFragmentView().render_to_fragment(request, course_id=course_id, **kwargs)

        # Render the full content to enrolled users, as well as to course and global staff.
        # Unenrolled users who are not course or global staff are given only a subset.
        enrollment = CourseEnrollment.get_enrollment(request.user, course_key)
        user_access = {
            'is_anonymous': request.user.is_anonymous,
            'is_enrolled': enrollment and enrollment.is_active,
            'is_staff': has_access(request.user, 'staff', course_key),
        }

        allow_anonymous = COURSE_ENABLE_UNENROLLED_ACCESS_FLAG.is_enabled(course_key)
        allow_public = allow_anonymous and course.course_visibility == COURSE_VISIBILITY_PUBLIC
        allow_public_outline = allow_anonymous and course.course_visibility == COURSE_VISIBILITY_PUBLIC_OUTLINE

        # Set all the fragments
        outline_fragment = None
        update_message_fragment = None
        course_sock_fragment = None
        course_expiration_fragment = None
        has_visited_course = None
        resume_course_url = None
        handouts_html = None

        if user_access['is_enrolled'] or user_access['is_staff']:
            outline_fragment = CourseOutlineFragmentView().render_to_fragment(
                request, course_id=course_id, **kwargs
            )
            if LATEST_UPDATE_FLAG.is_enabled(course_key):
                update_message_fragment = LatestUpdateFragmentView().render_to_fragment(
                    request, course_id=course_id, **kwargs
                )
            else:
                update_message_fragment = WelcomeMessageFragmentView().render_to_fragment(
                    request, course_id=course_id, **kwargs
                )
            course_sock_fragment = CourseSockFragmentView().render_to_fragment(request, course=course, **kwargs)
            has_visited_course, resume_course_url = self._get_resume_course_info(request, course_id)
            handouts_html = self._get_course_handouts(request, course)
            course_expiration_fragment = generate_course_expired_fragment(request.user, course)
        elif allow_public_outline or allow_public:
            outline_fragment = CourseOutlineFragmentView().render_to_fragment(
                request, course_id=course_id, user_is_enrolled=False, **kwargs
            )
            course_sock_fragment = CourseSockFragmentView().render_to_fragment(request, course=course, **kwargs)
            if allow_public:
                handouts_html = self._get_course_handouts(request, course)
        else:
            # Redirect the user to the dashboard if they are not enrolled and
            # this is a course that does not support direct enrollment.
            if not can_self_enroll_in_course(course_key):
                raise CourseAccessRedirect(reverse('dashboard'))

        # Get the course tools enabled for this user and course
        course_tools = CourseToolsPluginManager.get_enabled_course_tools(request, course_key)

        # Check if the user can access the course goal functionality
        has_goal_permission = has_course_goal_permission(request, course_id, user_access)

        # Grab the current course goal and the acceptable course goal keys mapped to translated values
        current_goal = get_course_goal(request.user, course_key)
        goal_options = get_course_goal_options()

        # Get the course goals api endpoint
        goal_api_url = get_goal_api_url(request)

        # Grab the course home messages fragment to render any relevant django messages
        course_home_message_fragment = CourseHomeMessageFragmentView().render_to_fragment(
            request, course_id=course_id, user_access=user_access, **kwargs
        )

        # Get info for upgrade messaging
        upgrade_price = None
        upgrade_url = None

        # TODO Add switch to control deployment
        if SHOW_UPGRADE_MSG_ON_COURSE_HOME.is_enabled(course_key) and enrollment and enrollment.upgrade_deadline:
            upgrade_url = EcommerceService().upgrade_url(request.user, course_key)
            upgrade_price = get_cosmetic_verified_display_price(course)

        # Render the course home fragment
        context = {
            'request': request,
            'csrf': csrf(request)['csrf_token'],
            'course': course,
            'course_key': course_key,
            'outline_fragment': outline_fragment,
            'handouts_html': handouts_html,
            'course_home_message_fragment': course_home_message_fragment,
            'course_expiration_fragment': course_expiration_fragment,
            'has_visited_course': has_visited_course,
            'resume_course_url': resume_course_url,
            'course_tools': course_tools,
            'dates_fragment': dates_fragment,
            'username': request.user.username,
            'goal_api_url': goal_api_url,
            'has_goal_permission': has_goal_permission,
            'goal_options': goal_options,
            'current_goal': current_goal,
            'update_message_fragment': update_message_fragment,
            'course_sock_fragment': course_sock_fragment,
            'disable_courseware_js': True,
            'uses_pattern_library': True,
            'upgrade_price': upgrade_price,
            'upgrade_url': upgrade_url,
            'course_overview' : course_overview,
            'blocks' : course_block_tree
        }

        if course_overview.get_course_type() == CourseTypeChoice.Assessment.value :
            
            from openedx.features.user_proctoring_system.models import ProctoringData, UserProctoringConfiguration
            from openedx.features.code_editor.models import CodingQuestion
            from openedx.features.IDE_Exam.models import IDEExams, IDEExamAttempt
            
            viewPath = 'course_experience/Assessment/course-home-fragment-new.html'
            
            grades_details = CourseGradeFactory().read(request.user, course)
            proctored_exams = get_all_exams_for_course(course_key)
            exam_durations = dict()
            exam_attempts = dict()
            exam_configs = dict()
            coding_exams = dict()
            ide_exams =dict()
            IDEExamattempts = dict()
            for proctored_exam in proctored_exams :
                if proctored_exam['is_active'] :
                    exam_durations[proctored_exam['content_id']] = proctored_exam['time_limit_mins']
                    exam_attempts[proctored_exam['content_id']] = ProctoredExamStudentAttempt.objects.filter(user=request.user,proctored_exam_id=proctored_exam['id']).first()
                    exam_configs[proctored_exam['content_id']] = UserProctoringConfiguration.get_user_proctoring_parameters(proctored_exam, request.user)
                    if CodingQuestion.enable_code_editor(proctored_exam):
                        coding_exams[proctored_exam['content_id']] = True
                    ideExam= IDEExams.get_ide_exam(proctored_exam)
                    if ideExam :
                        ide_exams[proctored_exam['content_id']] = ideExam
                        IDEExamattempt= IDEExamAttempt.objects.filter(user=request.user,ide_exam=ideExam).first()
                        if IDEExamattempt:
                            IDEExamattempts[proctored_exam['content_id']]=IDEExamattempt

            context['grades_details'] = grades_details
            context['proctored_exams'] = proctored_exams
            context['exam_durations'] = exam_durations
            context['exam_attempts'] = exam_attempts
            context['exam_configs'] = exam_configs
            context['coding_exams'] = coding_exams
            context['ide_exams'] = ide_exams
            context['ide_exam_attempts']=IDEExamattempts
            context['client_id'] = settings.GITHUB_CLIENT_ID
            context['oauth_login_url'] = settings.GITHUB_LOGIN_URL
            context['oauth_redirect_url'] = settings.GITHUB_REDIRECT_URL

        elif course_overview.get_course_type() == CourseTypeChoice.Project.value or course_overview.get_course_type() == CourseTypeChoice.Application.value:
            viewPath = 'course_experience/course-home-fragment-project.html'
            from openedx.features.IDE_Exam.models import IDEExams, IDEExamAttempt
            proctored_exams = get_all_exams_for_course(course_key)
            # ide_exams = dict()
            # IDEExamattempts=dict()
            # for proctored_exam in proctored_exams :
            #     ideExam= IDEExams.get_ide_exam(proctored_exam)
                # if ideExam :
                #     ide_exams[proctored_exam['content_id']] = ideExam
                #     IDEExamattempt= IDEExamAttempt.objects.filter(user=request.user,ide_exam=ideExam).first()
                #     if IDEExamattempt:
                #         IDEExamattempts[proctored_exam['content_id']]=IDEExamattempt
                #     break

            # context['ide_exams'] = ide_exams
            # context['ide_exam_attempts']=IDEExamattempts
            # context['client_id'] = settings.GITHUB_CLIENT_ID
            # context['oauth_login_url'] = settings.GITHUB_LOGIN_URL
            # context['oauth_redirect_url'] = settings.GITHUB_REDIRECT_URL

        elif course_overview.get_course_type() == CourseTypeChoice.Course.value :
            viewPath = 'course_experience/course-home-fragment.html'
        elif course_overview.get_course_type() == CourseTypeChoice.Application.value :
            viewPath = 'course_experience/course-home-fragment-application.html'

        html = render_to_string(viewPath, context)
        return Fragment(html)

def gitHubRedirect(request,ExamId):
    context={}
    git_details={}
    try:
        code=request.GET['code']
        url = "https://github.com/login/oauth/access_token"
        payload = { 'client_id': settings.GITHUB_CLIENT_ID,
                    'client_secret': settings.GITHUB_CLIENT_SECRET,
                    'code': code 
                  }
        response = requests.request("POST", url, headers={'Accept':'application/json'}, data = payload, files = [])
        data = response.json()
        if data['access_token'] : 
            accesstoken = data['access_token']
            git_details['username'] = getUserDetailsFromGitHub(accesstoken)
            git_details['access_token'] = accesstoken
            git_details['is_token_generated']=True
            git_details['is_forked']=False
            IDEExamAttempt.saveGitInfo(request.user, ExamId, json.dumps(git_details) )
            
        context['is_logged_in']=True 
        context['access_token']=accesstoken
        return render_to_response('course_experience/GitHubRedirection/github-success-login.html',context)

    except :
        context['is_logged_in']= False 
        context['access_token']= None
        return render_to_response('course_experience/GitHubRedirection/github-success-login.html',context)

def getUserDetailsFromGitHub(accesstoken) :
    try:
        url='https://api.github.com/user'
        response = requests.request("GET", url, headers={'Accept':'application/json','Authorization':'token '+accesstoken}, files = [])
        data=response.json()
        if data['login'] :    
            return data['login']
    except :
        pass
    
def gitForkRepository(request) :
    ExamId =  request.POST.get('ide_exam_id')
    accesstoken = request.POST.get('accesstoken')
    if not accesstoken:
        accesstoken = get_access_token(ExamId, request, accesstoken)
    try:
        IDEExam= IDEExams.objects.filter(id = ExamId).first()
        if IDEExam.git_fork_repository :
            url = 'https://api.github.com/repos/'+ IDEExam.git_fork_repository+'/forks'
            response = requests.request("POST", url, headers={'accept':'application/vnd.github.v3+json','Authorization':'Token '+accesstoken})
            data=response.json()
            if data['html_url']:
                IDEExamattempt= IDEExamAttempt.objects.filter(user=request.user,ide_exam=IDEExam).first()
                if IDEExamattempt:
                    gitdetails=json.loads(IDEExamattempt.git_detais)
                    gitdetails['repository_url']=data['html_url']
                    gitdetails['is_forked']= True
                    IDEExamAttempt.saveGitInfo(request.user, ExamId, json.dumps(gitdetails) )
                    return JsonResponse({'success': True})
            else:
                return HttpResponse(status=500)
        else :
            return HttpResponse(status=500)
    except:
        pass

def get_access_token(ExamId, request, accesstoken):
    IDEExam= IDEExams.objects.filter(id = ExamId).first()
    IDEExamattempt= IDEExamAttempt.objects.filter(user=request.user,ide_exam=IDEExam).first()
    if IDEExamattempt:
        gitdetails=json.loads(IDEExamattempt.git_detais)
        accesstoken=gitdetails['access_token']
    return accesstoken

def deleteRepository(request):
    from student.models import get_user
    ExamId =  request.GET.get('exam_id')
    accesstoken = request.GET.get('accesstoken')
    userEmail = request.GET.get('email')
    user= get_user(userEmail)
    if not accesstoken:
        accesstoken = get_access_token(ExamId, request, accesstoken)
    try:
        IDEExam = IDEExams.objects.filter(id = ExamId).first()
        repository = IDEExam.git_fork_repository.split("/", 1)[1]
        IDEExamattempt = IDEExamAttempt.objects.filter(user=user[0],ide_exam=IDEExam).first()
        if IDEExamattempt:
            gitdetails = json.loads(IDEExamattempt.git_detais)
            url = "https://api.github.com/repos/"+gitdetails['username']+"/"+repository
            response = requests.request("DELETE", url, headers={'accept':'application/vnd.github.v3+json','Authorization':'Token '+accesstoken})
            if response.status_code != 204:
                return HttpResponse(status=500)
            else:
                return JsonResponse({'success': True})
    except:
        pass
