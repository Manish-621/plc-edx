from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
import sys
from openedx.core.djangoapps.content.course_overviews.models import CourseCustomDetails

@login_required
def saveCourseCustomDetails(request):
    c = CourseCustomDetails()
    course_key = request.POST['course_key']
    c.CourseType = request.POST.get('CourseType')
    c.Duration = request.POST.get('Duration')
    c.FocusArea = request.POST.get('FocusArea')
    c.Tags = request.POST.get('Tags')
    c.course_instructions = request.POST.get('Instructions')
    try:
        instructions = json.loads(c.course_instructions)
    except :
        return JsonResponse({'success': False, 'error':'Oops! Error Occured. '+ str(sys.exc_info()[1])})
    CourseCustomDetails.objects.filter(course_key=course_key).update(FocusArea=c.FocusArea,Duration=int(c.Duration),course_type_choice=c.CourseType, course_instructions=c.course_instructions, Tags = c.Tags)
    return JsonResponse({'success': True,'FocusArea': c.FocusArea,'Duration': c.Duration,'course_type': c.CourseType, 'Tags': c.Tags})

@login_required
def getCourseCustomDetails(request):
    c = CourseCustomDetails()
    course_key = request.POST['course_key']
    c = CourseCustomDetails.objects.filter(course_key=course_key).values()
    return JsonResponse({'success': True, 'details': list(c),'course_key': course_key})