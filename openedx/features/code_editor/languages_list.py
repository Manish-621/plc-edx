
def constant(f):
    def fset(self, value):
        raise TypeError
    def fget(self):
        return f()
    return property(fget, fset)

class Languages_List(object):

    @constant
    def BACKEND():
        return [
                {
                    'language':'c',
                    'filename':'main.c' ,
                    'displayname':'C',
                    'tagname' : 'c',
                    'syntaxhighlightName':'c_cpp',
                    'codeEditortheme':'monokai',
                    'default_code':'''#include <stdio.h>\nint main(void) {\n    printf("Hello World!");\n    return 0;\n}''',
                    'main_method':'''int main(void) {\n    start();\n    return 0;\n}''',
                    'default_without_main':'''#include <stdio.h>\nint start(void) {\n    printf("Hello World!");\n    return 0;\n}'''
                },
                {
                    "language":"cpp",
                    "filename":"main.cpp" ,
                    'displayname':'C++', 
                    'tagname' : 'cpp',
                    'syntaxhighlightName':'c_cpp',
                    'codeEditortheme':'monokai',
                    "default_code":'''#include <iostream>\nusing namespace std;\nint main() {\n    cout << "Hello World!";\n    return 0;\n}''',
                    "main_method":'''int main() {\n    start();\n    return 0;\n}''',
                    "default_without_main":'''#include <iostream>\nusing namespace std;\nint start() {\n    cout << "Hello World!";\n    return 0;\n}'''
                },
                {
                    "language":"csharp",
                    "filename":"main.cs" ,
                    'displayname':'C#', 
                    'tagname' : 'csharp',
                    'syntaxhighlightName':'csharp',
                    'codeEditortheme':'monokai',
                    "default_code":'''using System;\n\nclass MainClass {\n    static void Main() {\n        Console.WriteLine("Hello World!");\n    }\n}''',
                    "main_method":'''class MainClass {\n    static void Main() {\n        StartClass.Start();\n    }\n}''',
                    "default_without_main":'''using System;\n\nclass StartClass {\n    public static void Start() {\n        Console.WriteLine("Hello World!");\n    }\n}'''
                },
                {
                    "language":"java",
                    "filename":"Main.java" ,
                    'displayname':'Java',
                    'tagname' : 'java',
                    'syntaxhighlightName':'java',
                    'codeEditortheme':'monokai',
                    "default_code":'''class Main {\n    public static void main(String[] args) {\n        System.out.println("Hello World!");\n    }\n}''',
                    "main_method":'''class Main {\n    public static void main(String[] args) {\n        StartClass.start();\n    }\n}''',
                    "default_without_main":'''class StartClass {\n    public static void start() {\n        System.out.println("Hello World!");\n    }\n}'''
                },	
                {
                    "language":"javascript",
                    "filename":"main.js" ,
                    'displayname':'JavaScript',
                    'tagname' : 'javascript',
                    'syntaxhighlightName':'javascript',
                    'codeEditortheme':'monokai',
                    "default_code":'''console.log("Hello World!");''',
                    "main_method":''' ''',
                    "default_without_main":'''console.log("Hello World!");'''
                },
                {
                    "language":"php",
                    "filename":"main.php" ,
                    'displayname':'PHP',
                    'tagname' : 'php',
                    'syntaxhighlightName':'php',
                    'codeEditortheme':'monokai',
                    "default_code":'''<?php\necho "Hello World!";\n?>''',
                    "main_method":''' ''',
                    "default_without_main":'''<?php\necho "Hello World!";\n?>'''
                },		
                {
                    "language":"python",
                    "filename":"main.py" ,
                    'displayname':'Python',
                    'tagname' : 'python',
                    'syntaxhighlightName':'python',
                    'codeEditortheme':'monokai',
                    "default_code":'''print("Hello World!")''',
                    "main_method":''' ''',
                    "default_without_main":'''print("Hello World!")'''
                },
            ]

    @constant
    def DATABASE():
        return [
                {
                    'language':'mssql',
                    'filename':'mssql.sql' ,
                    'displayname':'MS SQL',
                    'tagname' : 'mssql',
                    'syntaxhighlightName':'sqlserver',
                    'codeEditortheme':'sqlserver',
                    'default_code':'''-- your code start from here'''
                },
                {
                    'language':'mysql',
                    'filename':'mssql.sql' ,
                    'displayname':'MySQL',
                    'tagname' : 'mysql',
                    'syntaxhighlightName':'mysql',
                    'codeEditortheme':'sqlserver',
                    'default_code':'''-- your code start from here'''
                },
                {
                    'language':'mysql',
                    'filename':'mssql.sql' ,
                    'displayname':'Oracle',
                    'tagname' : 'oracle',
                    'syntaxhighlightName':'mysql',
                    'codeEditortheme':'sqlserver',
                    'default_code':'''-- your code start from here'''
                }
            ]

    @constant
    def DEVOPS():
        return [
                {
                    'language':'groovy',
                    'filename':'main.groovy' ,
                    'displayname':'Groovy',
                    'tagname' : 'groovy',
                    'syntaxhighlightName':'groovy',
                    'codeEditortheme':'monokai',
                    'default_code':'''--write your Groovy code here'''
                },  
                {
                    'language':'yaml',
                    'filename':'main.yaml' ,
                    'displayname':'YAML',
                    'tagname' : 'yaml',
                    'syntaxhighlightName':'yaml',
                    'codeEditortheme':'monokai',
                    'default_code':'''--write your YAML code here'''
                },
                {
                    'language':'powershell',
                    'filename':'main.ps' ,
                    'displayname':'Powershell',
                    'tagname' : 'powershell',
                    'syntaxhighlightName':'powershell',
                    'codeEditortheme':'monokai',
                    'default_code':'''--write your Powershell script here'''
                },
                {
                    'language':'sh',
                    'filename':'main.sh' ,
                    'displayname':'Shell',
                    'tagname' : 'shell',
                    'syntaxhighlightName':'sh',
                    'codeEditortheme':'monokai',
                    'default_code':'''--write your shell script here'''
                }
            ]

    @constant
    def FRONTEND():
        return [
                {
                    "language":"html",
                    "filename":"main.html" ,
                    'displayname':'HTML',
                    'tagname' : 'html',
                    'syntaxhighlightName':'html',
                    'codeEditortheme':'monokai',
                    "default_code":'''<!DOCTYPE html>\n<html>\n</html>'''
                }
                # {
                #     "language":"javascript",
                #     "filename":"main.js" ,
                #     'displayname':'JavaScript',
                #     'tagname' : 'javascript',
                #     'syntaxhighlightName':'javascript',
                #     'codeEditortheme':'monokai',
                #     "default_code":'''console.log("Hello World!");'''
                # },
                # {
                #     "language":"css",
                #     "filename":"main.css" ,
                #     'displayname':'CSS',
                #     'tagname' : 'css',
                #     'syntaxhighlightName':'css',
                #     'codeEditortheme':'monokai',
                #     "default_code":'''/* start styling your page */'''
                # }
            ]

_languages = Languages_List()
