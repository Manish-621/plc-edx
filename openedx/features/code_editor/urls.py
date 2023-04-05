from django.conf.urls import url
from .views import get_snippet_manager, get_snippet_code, save_or_update_snippet_code

urlpatterns = [
    url(r'^snippet/manage', get_snippet_manager, name='snippet_manager'),
    url(r'^snippet/get/(?P<snippet_id>.*)?$', get_snippet_code, name='snippet_manager'),
    url(r'^snippet/save_or_update', save_or_update_snippet_code, name='snippet_manager')
]
