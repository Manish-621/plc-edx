# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import IDEExams, IDEExamAttempt
from util.json_request import JsonResponse, JsonResponseBadRequest, expect_json
import json

# Create your views here.
def get_ide_url(request) :
    repository_url=None
    user = request.user
    ide_exam_id = request.POST.get('ide_exam_id')
    Ide_exam = IDEExams.objects.filter( id=ide_exam_id).first()
    url = IDEExamAttempt.get_ide_url(Ide_exam,user)
    if url is None:
        return HttpResponse(status=500)
    else:
        try:
            if Ide_exam.enable_git_oauth:
                repository_url = get_repository_url(Ide_exam,user)
        finally:
            return JsonResponse({'success': True,'container_url':url,'repository_url': repository_url})

def delete_container(request):
    user = request.user
    container_group= request.POST.get('container_group')
    ide_exam_id = request.POST.get('ide_exam_id')
    if container_group :
        result = IDEExamAttempt.deletecontainer(container_group,user)
        if result:
            IDEExamAttempt.clearContainerUrl(ide_exam_id,user)
            return JsonResponse({'success': True})
        else:
            return  HttpResponse(status=500)

def get_repository_url(Ide_exam,user):
    IDEExamattempt= IDEExamAttempt.objects.filter(user=user,ide_exam=Ide_exam).first()
    if IDEExamattempt:
        gitdetails=json.loads(IDEExamattempt.git_detais)
        return gitdetails['repository_url'] if gitdetails['repository_url'] else None
    