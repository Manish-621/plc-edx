# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import json
from django.shortcuts import render, render_to_response
from django.contrib.auth.decorators import login_required
from util.json_request import JsonResponse, JsonResponseBadRequest, expect_json
from xmodule.exceptions import NotFoundError
from student.helpers import (
    do_create_account_custom
)
import sys
# Create your views here.

@login_required
def get_bulk_create_screen(request):

    if not (request.user.is_superuser or request.user.is_staff) :
        raise NotFoundError('Unauthorized Request')

    return render_to_response('user-bulk-create.html')

@login_required
def bulk_create(request):

    if not (request.user.is_superuser or request.user.is_staff) :
        raise NotFoundError('Unauthorized Request')

    users = request.POST.get('data')
    
    skip_email = True
    try:
        is_email = request.POST.get('is_email')
        if is_email == 'true':
            skip_email = False
    except:
        pass
    statuses = []
    for form in json.loads(users):
        status = dict()
        status['record'] = json.dumps(form)
        try:
            do_create_account_custom(form, skip_email)
            status['result'] = 'successful'
        except:
            status['result']='Oops! Error Occured. '+ str(sys.exc_info()[1])
        statuses.append(status)

    return JsonResponse({'success': True,'result_status':statuses})