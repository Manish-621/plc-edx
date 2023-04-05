# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import response

from django.shortcuts import render
from bisect import bisect
import urllib2
import ast
import requests
import base64
import json
import uuid
import random
import sys
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response
from util.json_request import JsonResponse, JsonResponseBadRequest, expect_json
from .models import CodingQuestion, CodingResult, DefaultSnippet
from .enums import CodingLanguagesType
from .languages_list import _languages
from .utils import get_code_by_snippet, save_or_update_code, run_backend_code, run_sql_query, run_backend_tests
from django.conf import settings
from xmodule.exceptions import ProcessingError
from django.views.decorators.csrf import csrf_exempt
from openedx.features.code_editor.enums import CodingLanguagesType
from edx_proctoring.models import ProctoredExam


# APIs for code editor
@login_required
def run_snippet(request):
    name = request.POST.get('name')
    content = request.POST.get('content')
    stdin = request.POST.get('stdin')
    language= request.POST.get('language')
    result_Snippet = request.POST.get('resultSnipptet')
    allow_main = request.POST.get('allow_main')

    if 'sql' in language :
        unit_id=request.POST.get('unit_id')
        subsection_id=request.POST.get('subsection_id')
        coding_exam = CodingQuestion.get_codingexambyUnitid(subsection_id, unit_id)
        resp1 = requests.get(coding_exam.additional_information, allow_redirects=True, verify=False)
        db_content = base64.b64encode(resp1.content)
        data = run_sql_query(content, db_content)

        if (data):
            data['stdout']= base64.b64decode(data['stdout']) if  data['stdout']  else None
            data['stderr']= base64.b64decode(data['stderr']) if  data['stderr']  else None
            data['ExamType']=CodingLanguagesType.DATABASE.value
            return JsonResponse(data)

    else :
        if result_Snippet:
            _,code = get_code_by_snippet(result_Snippet)
            content+= code
        elif str(allow_main) == 'false':
            for x in _languages.BACKEND :
                if x['language'] == language :
                    content+=x['main_method']
                    break
        response_data = run_backend_code(name, content, stdin, language)
        if(response_data):
            return JsonResponse(response_data)
    return JsonResponse("")

@login_required
def run_testcases(request):
    user = request.user
    name = request.POST.get('name')
    content = request.POST.get('content')
    stdin = request.POST.get('stdin')
    language= request.POST.get('language')
    # result_Snippet = request.POST.get('resultSnipptet')
    # allow_main = request.POST.get('allow_main')
    unit_id=request.POST.get('unit_id')
    subsection_id=request.POST.get('subsection_id')
    coding_exam = CodingQuestion.get_codingexambyUnitid(subsection_id, unit_id)
    if 'sql' in language :
        resp1 = requests.get(coding_exam.additional_information, allow_redirects=True, verify=False)
        db_content = base64.b64encode(resp1.content)
        data = run_sql_query(content, db_content)
        if (data):
            data['stdout']= base64.b64decode(data['stdout']) if  data['stdout']  else None
            data['stderr']= base64.b64decode(data['stderr']) if  data['stderr']  else None
            data['ExamType']=CodingLanguagesType.DATABASE.value
            return JsonResponse(data)

    else :
        coding_result_data = CodingResult.objects.filter(user=user, coding_exam=coding_exam).first()
        # Collect evaluation parameters as a list of dictionary
        complete_response = {}
        params = json.loads(coding_exam.evaluvation_parameters)

        eval_parameters = []
        for r in params:
            eval_parameters.append(ast.literal_eval(r))

        # get the score of the candidate's evaluation
        score = 0

        for param in eval_parameters:
            response_data = run_backend_tests(name, content, param['input'], language)
            # if response_data['stdout'] is not None:

            if response_data:
                if (response_data['stdout'] is None) and (param['output'] != 'None'):
                    complete_response['stdout'] = complete_response.get('stdout',"") + "Error Occured\n"
                else:
                    if (response_data['stdout'] is None):
                        complete_response['stdout'] = complete_response.get('stdout',"") + str(response_data['stdout']) + "\n"
                        score += param['weightage']
                    else:
                        complete_response['stdout'] = complete_response.get('stdout',"") + response_data['stdout'][:-1] + "\n"
                        if response_data['stdout'].strip('\n')==param['output']:
                            score += param['weightage']
                complete_response['time'] = complete_response.get('time',0.0) + float(response_data['time'])
                complete_response['memory'] = complete_response.get('memory',0) + response_data['memory']

        coding_result_data.score = score
        score = float(score) / coding_exam.max_score * 100
        coding_result_data.result = "PASSED" if int(score) >= 60 else "FAILED"
        coding_result_data.grade = get_grade(int(score))
        coding_result_data.save()
        test_response = {}
        # test_response['stdout'] = complete_response['stdout'] + "\n\nMemory consumed: " + str(complete_response['memory']) + " KB\nTime taken: " + str(response_data['time']) + " sec\n" + str(score) + "% Testcases Passed"
        test_response['stdout'] = "Memory consumed: " + str(complete_response['memory']) + " KB\nTime taken: " + str(response_data['time']) + " sec\n" + "Testcases Passed: " + str(score) + '%\nResult: '+ coding_result_data.result

        html_response = "<table border=1>"
        test_split = test_response['stdout'].split('\n')
        for test in test_split:
            html_response += '<tr>'
            tdt = test.split(': ')
            html_response += '<td>' + tdt[0] + '</td><td>' + tdt[1] + '</td>'
        html_response += '</table>'
        test_response['stdout'] = html_response
        return JsonResponse(test_response)
    return JsonResponse("")

def get_grade(score, breakpoints=[60, 70, 80, 90], grades='FDCBA'):
    i = bisect(breakpoints, score)
    return grades[i]

@login_required
def save_snippet(request):
    user = request.user
    coding_exam_id = request.POST.get('coding_exam_id')
    language = request.POST.get('language')
    name = request.POST.get('name')
    content = request.POST.get('content')
    question_id = request.POST.get('question_id')
    snippet_id = request.POST.get('snippet_id')
    unit_id=request.POST.get('unit_id')
    subsection_id=request.POST.get('subsection_id')
    is_submit =request.POST.get('is_Submit')

    coding_exam = CodingQuestion.get_codingexambyUnitid(subsection_id, unit_id)

    # will throw exception if the response already submitted
    CodingResult.request_save(user, coding_exam, unit_id)
    # snippet_id = save_or_update_code(language, user.username, name, content, snippet_id)

    if CodingResult.save_result(user, coding_exam, question_id, snippet_id, unit_id, is_submit=='true', content, language):
        # Log for auto evaluation
        #import ipdb; ipdb.set_trace()
        try :
            if coding_exam.auto_evaluation and coding_exam.coding_Languages_type == CodingLanguagesType.BACKEND.value:
                coding_result_data = CodingResult.objects.filter(user=user, coding_exam=coding_exam, is_graded=0).first()
                request_data = {}
                request_data['attempt_id'] = coding_result_data.id
                request_data['snippet_id'] = coding_result_data.snippet_id
                request_data['langType'] = 'be'
                request_data['evaluation_parameters'] = coding_result_data.coding_exam.evaluvation_parameters
                payload = json.dumps(request_data)
                headers = {
                            'Content-Type': 'application/json'
                        }
                response = requests.post(url = settings.AZURE_CLI_API_URL+'/api/v1/evaluation/add-job', data = payload, headers = headers)
        except :
            print(str(sys.exc_info()[1]))
        return JsonResponse({'success': True, 'snippet_id':snippet_id})
    return JsonResponse({'success': False})

@login_required
def get_code_by_questionID(request) :
    user = request.user
    unit_id = request.POST.get('unit_id')
    subsection_id = request.POST.get('subsection_id')
    coding_exam_id = request.POST.get('coding_exam_id')
    coding_question = CodingQuestion.get_codingexambyUnitid(subsection_id, unit_id)
    Coding_Result = CodingResult.objects.filter(coding_exam=coding_question,user=user).first()
    saved_language=None
    saved_snippetid=None
    data = {}
    is_submit=None
    editorLanguages=None
    filteredLanguage=None
    attempted_language='na'
    if Coding_Result:
        saved_snippet = Coding_Result.snippet_text
    else:
        saved_snippet = None

    if coding_question and coding_question.is_active :
        data['is_coding'] = True
        language_list=""
        #Loading Language
        if coding_question.coding_Languages :
            # language_list=coding_question.coding_Languages.lower().split(',')
            language_list= [language.strip() for language in coding_question.coding_Languages.lower().split(',')]

        coding_languages_type =  coding_question.coding_Languages_type
        if not coding_languages_type:
            coding_languages_type=CodingLanguagesType.BACKEND.value

        if coding_languages_type== CodingLanguagesType.BACKEND.value :
            editorLanguages=json.loads(json.dumps(_languages.BACKEND))
        elif coding_languages_type== CodingLanguagesType.DATABASE.value :
            editorLanguages=json.loads(json.dumps(_languages.DATABASE))
        elif coding_languages_type== CodingLanguagesType.DEVOPS.value :
            editorLanguages=json.loads(json.dumps(_languages.DEVOPS))
        elif coding_languages_type== CodingLanguagesType.FRONTEND.value :
            editorLanguages=json.loads(json.dumps(_languages.FRONTEND))

        if len(language_list)>0:
            filteredLanguages= [x for x in editorLanguages if x['tagname'].lower() in language_list]
        else :
            filteredLanguages= editorLanguages

        #Loading default snippet code
        default_snippetsID=None
        if coding_question.default_snippet_id:
            # default_snippetsID=coding_question.default_snippet_id.split(',')
            default_snippetsID = [snippet.strip() for snippet in coding_question.default_snippet_id.split(',')]

        result_SnippetsIds = None
        if coding_question.result_snippet_id:
            # result_SnippetsIds = coding_question.result_snippet_id.split(',')
            result_SnippetsIds = [snippet.strip() for snippet in coding_question.result_snippet_id.split(',')]

        resultSnippets = dict()
        if default_snippetsID:
            for index, default_snippet_id in enumerate(default_snippetsID) :
                try:
                    default_snippet = DefaultSnippet.get_snippet(default_snippet_id)
                    code = default_snippet.snippet_text
                    language = default_snippet.coding_language
                    if result_SnippetsIds:
                        resultSnippets[language] = result_SnippetsIds[index]
                    for x in filteredLanguages :
                        if x['language'] == language :
                            x['default_code'] = code
                            x['default_without_main'] = code
                except:
                    raise

        #Loading saved snippet code
        if Coding_Result and Coding_Result.snippet_text:
            is_submit = Coding_Result.is_submit
            saved_snippetid= Coding_Result.snippet_id
            saved_snippet = Coding_Result.snippet_text
            if saved_snippetid :
                try:
                    # language, code = get_code_by_snippet(saved_snippetid)
                    language = Coding_Result.snippet_language
                    code = saved_snippet
                    attempted_language=language
                    for x in filteredLanguages :
                        if x['language'] == language and code != "Not Attempted" :
                            x['default_code'] = code
                            x['default_without_main'] = code
                except Exception:
                    code = filteredLanguages[0]['default_code']
                    if not coding_question.allow_main_method:
                        code = filteredLanguages[0]['default_without_main']
                    try:
                        snippet_id = save_or_update_code(filteredLanguages[0]['language'], user.username, filteredLanguages[0]['filename'], code, None)
                    except:
                        snippet_id = str(uuid.uuid4())
                    saved_snippetid=snippet_id
                    CodingResult.save_result(user, coding_question,'NA', snippet_id, unit_id, is_submit=='false', code, filteredLanguages[0]['language'])
        else :
            code = filteredLanguages[0]['default_code']
            if not coding_question.allow_main_method:
                code = filteredLanguages[0]['default_without_main']
            try:
                snippet_id = save_or_update_code(filteredLanguages[0]['language'], user.username, filteredLanguages[0]['filename'], code, None)
            except:
                snippet_id = str(uuid.uuid4())
            saved_snippetid=snippet_id
            CodingResult.save_result(user, coding_question,'NA', snippet_id, unit_id, is_submit=='false', code, filteredLanguages[0]['language'])

        data['coding_Languages']=filteredLanguages
        data['snippetid'] = saved_snippetid
        data['is_submit']= is_submit
        data['attempted_language'] = attempted_language
        data['enable_run'] = coding_question.enable_code_run
        data['enable_copy_paste'] = coding_question.enable_copy_paste
        data['language_type'] = coding_question.coding_Languages_type
        data['resultSnippets'] = resultSnippets
        data['allow_main'] = coding_question.allow_main_method
    else :
        data['is_coding'] = False
    return JsonResponse(data)


# APIs for auto evaluation
@csrf_exempt
def get_pending_responses(request):
    course_id = request.GET['course_id']
    if course_id:
        course_id = course_id.replace('*','+')
        responses = CodingResult.objects.filter(coding_exam__proctored_exam__course_id=course_id,is_graded=0,is_submit=1)
    else :
        responses = CodingResult.objects.filter(is_graded=0,is_submit=1)
    ids = []
    if responses.exists():
        ids = [response.id for response in responses]
    return JsonResponse(json.dumps(ids))

@csrf_exempt
def get_student_response(request, id):
    responses = CodingResult.objects.filter(is_graded=0,is_submit=1,pk=id)
    response_data = {}
    if responses.exists():
        response = responses.first()
        response_data['attempt_id'] = response.id
        response_data['snippet_id'] = response.snippet_id
        response_data['langType'] = 'be'
        if response.coding_exam.coding_Languages_type == CodingLanguagesType.DATABASE.value :
            response_data['langType'] = 'db'
        response_data['evaluation_parameters'] = response.coding_exam.evaluvation_parameters
    return JsonResponse(json.dumps(response_data))

@csrf_exempt
def update_coding_result(request):
    attempt_id = request.POST.get('attempt_id')
    evaluation_details = request.POST.get('evaluation_details')
    #import ipdb; ipdb.set_trace()
    responses = CodingResult.objects.filter(is_graded=0,is_submit=1,pk=attempt_id)
    if responses.exists():
        response = responses.first()
        response.evaluation_details = evaluation_details
        response.score = json.loads(evaluation_details)['final_score']
        response.is_graded = 1
        response.save()

    return JsonResponse({'success':True})


# APIs for snippet manager
@login_required
def get_snippet_manager(request):
    if not (request.user.is_superuser or request.user.is_staff):
        raise NotFoundError('Unauthorized Request')

    #import ipdb;ipdb.set_trace()
    backend = json.dumps(_languages.BACKEND)
    database = json.dumps(_languages.DATABASE)
    devops = json.dumps(_languages.DEVOPS)
    frontend = json.dumps(_languages.FRONTEND)
    context = {
        'BACKEND':backend,
        'DATABASE':database,
        'DEVOPS':devops,
        'FRONTEND':frontend
    }
    return render_to_response('snippet-manager.html',context)

@login_required
def get_snippet_code(request, snippet_id):
    data = {}
    #import ipdb; ipdb.set_trace()
    # data['language'], data['code'] = get_code_by_snippet(snippet_id)
    coding_results = CodingResult.objects.filter(snippet_id=snippet_id)
    if coding_results.exists:
        result = coding_results.first()
        data["language"] = result.snippet_language
        data["code"] = result.snippet_text
    return JsonResponse(data)

@login_required
def save_or_update_snippet_code(request):
    if not (request.user.is_superuser or request.user.is_staff):
        raise NotFoundError('Unauthorized Request')

    language = request.POST.get('language')
    filename = request.POST.get('filename')
    content = request.POST.get('content')
    snippet_id = request.POST.get('snippet_id')
    is_update =request.POST.get('is_Update')

    data = {}
    data['snippet_id'] = save_or_update_code(language, request.user.username, filename, content, snippet_id if is_update == 'true' else None)

    return JsonResponse(data)
