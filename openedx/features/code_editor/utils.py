from django.conf import settings
import requests
import random
import json
import base64
import uuid

###
# Object with language to language code for judge0 compiler api
###
judge0_language_codes = {
        "c" :50,
        "cpp" : 54,
        "csharp" : 51,
        "java" : 62,
        "javascript" : 63,
        "python" : 71,
        "php" : 68,
        "mssql" : 82,
        "mysql" : 82
}

###
# Method to run get code from glot compiler
###
def get_code_by_snippet(snippet_id):
    response = requests.get(settings.GLOT_SNIPPET_URL+"/snippets/"+snippet_id)
    # response = requests.get("https://glot.io/api"+"/snippets/"+snippet_id)
    json_data = response.json()
    return json_data['language'], str(json_data['files'][0]['content'])

###
# Method to save or update the given code in glot compiler
###
def save_or_update_code(language, username, filename, content, snippet_id) :
    data = {"language": language,
         "title": username+""+str(random.randrange(1,1000)) ,
         "public": False,
         "files": [{"name": filename, "content": content}]
         }
    url = settings.GLOT_SNIPPET_URL+"/snippets"
    # url = "https://glot.io/api"+"/snippets"
    headers = {
                    'Authorization': settings.GLOT_AUTH_TOKEN,
                    'Content-Type':'application/json'
                }

    if snippet_id and len(snippet_id)>1:
        response = requests.put(url+"/"+snippet_id, json.dumps(data), headers=headers)
    else:
        response = requests.post(url, json.dumps(data), headers=headers)
    # print('************************************************')
    # print(response.__dict__)
    # print(type(response.json()))

    if response.json().get('id'):
        return response.json()['id']

    return str(uuid.uuid4())

###
# Method to run backend code
###
def run_backend_code(filename, content, stdin, language):
    if settings.CODE_COMPILER_OPTION == 1:
        return run_backend_judge0(filename, content, stdin, language)
    elif settings.CODE_COMPILER_OPTION == 2:
        return run_backend_glot(filename, content, stdin, language)


def run_backend_tests(filename, content, stdin, language):
    return run_backend_tests_judge0(filename, content, stdin, language)

###
# Method to run database code with judge0 Compiler
###
def run_sql_query(query, database_base64):
    query = '.headers on \n.mode html \n' + query
    if 'insert' in query or 'update' in query:
        query += "\n.headers OFF \nselect changes()||' row(s) affected';"
    query_base64 = base64.b64encode(query.encode()).decode("utf-8")

    payload = {
            'source_code' : query_base64,
            'language_id'  : 82,
            'additional_files':database_base64.decode("utf-8")
        }

    headers = {
        'content-type': "application/json",
        'accept': "application/json"
        }
    response = requests.post(settings.JUDGE0_RUN_URL+'/?wait=true&base64_encoded=true', data=json.dumps(payload), headers=headers)
    if (response.status_code==200 or response.status_code==201):
        return response.json()
    return None


###
# Method to run backend code using glot compiler
###
def run_backend_glot(filename, content, stdin, language):
    data = {
                "files": [
                            {
                                "name": filename,
                                "content": content
                            }
                ],
                "stdin":stdin
        }
    url = settings.GLOT_RUN_URL+'/languages/'+str(language)+'/latest'
    headers = {
                'Authorization': settings.GLOT_AUTH_TOKEN,
                'Content-Type':'application/json'
            }
    response = requests.post(url, json.dumps(data), headers=headers)
    if(response.status_code==200):
        return response.json()
    return None

###
# Method to run backend code using judge0 compiler
###
def run_backend_judge0(filename, content, stdin, language):
    data = {
        "language_id":judge0_language_codes[language],
        "source_code":content,
        "stdin":stdin
    }
    r = requests.post(url = settings.JUDGE0_RUN_URL+'/?wait=true', data = data)

    # extracting response text
    data_response = json.loads(r.text)
    status_id = data_response['status']['id']
    if status_id == 6 :
        data_response['stderr'] = data_response['compile_output']
    elif status_id in [1,2]:
        data_response['stderr'] = 'Got unexpected response'
    elif status_id in [5]:
        data_response['stderr'] = 'Runtime Error : Time Limit Exceeded \nPlease check for code optimizations'
    return data_response


def run_backend_tests_judge0(filename, content, stdin, language):
    data = {
        "language_id":judge0_language_codes[language],
        "source_code":content,
        "stdin":stdin
    }
    r = requests.post(url = settings.JUDGE0_RUN_URL+'/?wait=true', data = data)

    # extracting response text
    data_response = json.loads(r.text)

    status_id = data_response['status']['id']
    if status_id == 6 :
        data_response['stderr'] = data_response['compile_output']
    elif status_id in [1,2]:
        data_response['stderr'] = 'Got unexpected response'
    elif status_id in [5]:
        data_response['stderr'] = 'Runtime Error : Time Limit Exceeded \nPlease check for code optimizations'
    return data_response
