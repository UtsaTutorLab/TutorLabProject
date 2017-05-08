from django.conf import settings 
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, Group
from django.core import serializers, signing
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import get_object_or_404, render

from .models import Course, CustomIssueSet, Instructor, Student as classStudent
from ta_tutor.models import Session, Tutor
from tutor_admin.models import Term
from student.models import Student
from survey.models import Choice, Question
from home.models import CommonStudentIssue

import pyexcel as pe
from xlrd import XLRDError
import time, json, sys

# Attempt with Selenium
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def instructor(request):
    if request.user.is_active:
        if not request.user.groups.filter(name='Instructor').exists() and not request.user.groups.filter(name='Tutor_Admin').exists():
            return HttpResponseRedirect('/')
        
        # Check to see if need to populate instructor course models (should be done at start of each semester, 
        #but currently no way auto re-pop after new semester)
        first_name = request.user.first_name
        last_name = request.user.last_name
        courses = []

        # if not Course.objects.filter(Instructor = request.user):
        #     courses = populate_courses(request)
        # else:
        instructor = Instructor.objects.get(user=request.user)
        for course in Course.objects.filter(Instructor = instructor).order_by('course_num'):
            courses.append(course)

        student_list_raw = Session.objects.order_by('student')
        student_dict = {}
        for student in student_list_raw:
            if not student.student in student_dict:
                try:
                    student_dict[student.student] = student.whole_name
                except ObjectDoesNotExist:
                    pass
        tutor_list = Tutor.objects.order_by('tutor')
        term_list = []
        # GET TERMS FROM DB
        for term in Term.objects.all():
            term_list.append(term)

        # MAKE SURE THERE ARE AT LEAST 5 QUESTIONS
        question_list = Question.objects.all()
        if question_list.count() < 5:
            for new in range(0, (5 - question_list.count())):
                new_question = Question.objects.create(question_test = "New Question")
                new_question.save()
            question_list = Question.objects.all()
        
        choice_list = Choice.objects.all()

        issue_list = CommonStudentIssue.objects.all()

        custom_issue_list = []
        for course in courses:
            custom_issue_list.append(CustomIssueSet.objects.filter(course=course))

        # Tutor Admin
        if request.user.groups.filter(name='Tutor_Admin').exists():
            return render(request, 'tutor_admin/home.html', {"student_list":student_dict, "tutor_list":tutor_list,
                "courses":courses, "question_list":question_list, 'term_list':term_list, "issue_list":issue_list,
                "custom_issue_list":custom_issue_list, "choice_list":choice_list})

        return render(request, 'instructor/home.html', {"student_list":student_dict, "courses":courses})
    else:
        return HttpResponseRedirect('/')

def activate_account(request, token):
    '''
    '''
    try:
        abc123 = signing.loads(token, salt=settings.SECRET_KEY)
        user = get_object_or_404(User, username=abc123)
        if not user.instructor.token == token:
            raise Http404("Your token is not valid")
        if request.method == 'POST':
            pass1 = request.POST.get('password')
            pass2 = request.POST.get('confirm-password')
            if len(pass1) < 8:
                return HttpResponse(
                    json.dumps("fail1"),
                    content_type="application/json"
                )
            elif pass1 != pass2:
                return HttpResponse(
                    json.dumps("fail2"),
                    content_type="application/json"
                )
            else:
                user = User.objects.get(username=abc123)
                user.set_password(pass1)
                user.is_active=True
                user.save()
                user = authenticate(username=abc123, password=pass1)
                if user is not None:
                    if user.is_active:
                        login(request, user)
                        user.instructor.token = None
                        user.instructor.save()
                        return HttpResponse(
                            json.dumps("/instructor"),
                            content_type="application/json"
                        )
        else:
            return render(request, 'instructor/activate_account.html', {"user":user})
    except signing.BadSignature:
        raise Http404("Invalid token")

def student_sessions(request, abc123, classID):
    session_list = Session.objects.filter(student=abc123).filter(classID=classID).order_by('sessionID')

    return render(request, 'instructor/studentdetail.html', {"student":abc123, "session_list":session_list})

def session_detail(request, id):
    session = get_object_or_404(Session, id=id)
    return render(request, 'instructor/studentdata.html', {"session":session})

def populate_courses(request):
    first_name = request.user.first_name
    last_name = request.user.last_name

    driver = webdriver.PhantomJS()
    driver.get("https://bluebook.utsa.edu")
    
    searchType_radioBUTTON = driver.find_element_by_id("ctl00_MainContentSearchQuery_searchCriteriaEntry_SearchTypeRBL_1")
    searchType_radioBUTTON.click()
    searchBox = driver.find_element_by_name("ctl00$MainContentSearchQuery$searchCriteriaEntry$FacultyTitleTxtBox")
    searchBox.clear()
    searchBox.send_keys(last_name + ", " + first_name)
    submitSearch_button = driver.find_element_by_id("ctl00_MainContentSearchQuery_searchCriteriaEntry_SearchBtn")
    submitSearch_button.click()

    term_radioBUTTON = driver.find_element_by_id("ctl00_MainContent_mainContent1_CourseTermSelectRBL_1")
    term_radioBUTTON.click()
    time.sleep(15)

    courses_div = driver.find_element_by_id("ctl00_MainContent_mainContent1_MainContentAccordion")
    courses = courses_div.find_elements_by_class_name("accordionMasterPane")
    course_num_list = []
    courses_name_final = []
    courses_num_final = []
    course_index = 0
    for course in courses:
        course_num = course.find_element_by_id("ctl00_MainContent_mainContent1_MainContentAccordion_Pane_"+str(course_index)+"_header_CourseLbl")
        course_name = course.find_element_by_id("ctl00_MainContent_mainContent1_MainContentAccordion_Pane_"+str(course_index)+"_header_TitleLnkBtn")
        course_num_list.append(course_num.find_element_by_xpath("..").text)
        courses_name_final.append(course_name.text)
        course_index += 1

    for course in course_num_list:
        courses_num_final.append(course[3:])

    driver.quit()

    index = 0
    while index < course_index:
        new_course = Course(course_num = courses_num_final[index], course_name = courses_name_final[index], Instructor = request.user)
        new_course.save()
        index += 1

    courses_num_final.sort()

    return courses_num_final

def get_custom_issue_list(request):
    '''
    '''
    classId = request.GET.get("course_id")
    try:
        course = Course.objects.get(id=classId)
        issues = CustomIssueSet.objects.filter(course=course)
        issueList = []
        ids = []
        for i in issues:
            ids.append(i.issue.id)
            pair = [i.id, i.issue.issue] 
            issueList.append(pair) 
        
        selectList = CommonStudentIssue.objects.exclude(id__in=ids).values('id','issue')

        data = {
            'bool':"true",
            'selectList': list(selectList),
            'issueList': list(issueList) 
        }
    except:
        print("Unexpected error:", sys.exc_info())
        data = {
            'bool':"false",
        }

    return HttpResponse(
        json.dumps(data),
        content_type="application/json"
    )


def add_custom_issue_list(request):
    '''
    '''
    classId = request.POST.get("course_id")
    issueList = request.POST.getlist("issue_list[]")
    try:
        course = Course.objects.get(id=classId)
        for issueId in issueList:
            issue = CommonStudentIssue.objects.get(id=issueId)
            newIssue = CustomIssueSet.objects.create(
                course=course,
                issue=issue
            )
        issues = CustomIssueSet.objects.filter(course=course)
        newIssueList = []
        ids = []
        for i in issues:
            ids.append(i.issue.id)
            pair = [i.id, i.issue.issue] 
            newIssueList.append(pair) 

        selectList = CommonStudentIssue.objects.exclude(id__in=ids).values('id','issue')

        # print(list(newIssueList))
        data = {
            'bool': "true",
            'newIssueList': list(newIssueList),
            'selectList': list(selectList)
        }
    except:
        data = {
            'bool': "false"
        }

    return HttpResponse(
        json.dumps(data),
        content_type="application/json"
    )


def delete_from_custom_list(request):
    '''
    '''
    issueId = request.POST.get('issue_id')
    classId = request.POST.get("class_id")
    try:
        deleteIssue = CustomIssueSet.objects.get(id=issueId)
        deleteIssue.delete()
        course = Course.objects.get(id=classId)
        issues = CustomIssueSet.objects.filter(course=course)
        issueList = []
        ids = []
        for i in issues:
            ids.append(i.issue.id)
            pair = [i.id, i.issue.issue] 
            issueList.append(pair) 
        
        selectList = CommonStudentIssue.objects.exclude(id__in=ids).values('id','issue')

        data = {
            'bool':"true",
            'selectList': list(selectList),
            'issueList': list(issueList) 
        }
    except:
        data = {
            'bool':"false"
        }
    return HttpResponse(
        json.dumps(data),
        content_type="application/json"
    )


def get_students(request):
    '''
    '''
    try:
        classId = request.GET.get("course_id")
        course = Course.objects.get(id=classId)
        studentQS = classStudent.objects.filter(courses=course).order_by('-last_name')
        student_list = list(studentQS.values_list('first_name', 'last_name', 'studentID'))
        data = {
            'bool':"true",
            'student_list':student_list
        }
    except:
        print("Unexpected error:", sys.exc_info()[0])
        data = {
            'bool':"false",
            'msg':'Error occurred'
        }
    return HttpResponse(
        json.dumps(data),
        content_type="application/json"
    )


def add_students_to_class(request):
    '''
    ADDS STUDENTS TO A CLASS BY READING FROM UPLOADED XLS 
    '''
    try:
        if request.method == 'POST' and request.FILES['file']:
            classId = request.POST.get("course_id")
            xlsFile = request.FILES['file']
            
            new_student_count = 0
            try:
                course = Course.objects.get(id=classId)
            except:
                data = {
                    'bool':"false",
                    'msg':"Course does not exist"
                }
                return HttpResponse(
                    json.dumps(data),
                    content_type="application/json"
                )
            try:
                fs = FileSystemStorage()
                filename = fs.save(xlsFile.name, xlsFile)
                sheet = pe.get_sheet(file_name=fs.path(xlsFile.name), name_columns_by_row=0)
                records = sheet.to_records()
                for record in records:
                    keys = sorted(record.keys())
                    for key in keys:
                        if key == "First Name":
                            first_name = record[key]
                        elif key == "Last Name": 
                            last_name = record[key]
                        elif key == "Username":
                            username = record[key]
                    new_student, created = classStudent.objects.get_or_create(
                        course = course,
                        studentID = username,
                        name = first_name + " " + last_name
                    )
                    if(created):
                        new_student_count += 1
                            
                fs.delete(xlsFile.name)
                data = {
                    "bool":"true",
                    "new_count":new_student_count
                }
                return HttpResponse(
                    json.dumps(data),
                    content_type="application/json"
                )
            except XLRDError:
                import codecs
                fs = FileSystemStorage()
                filename = fs.save(xlsFile.name, xlsFile)
                print("XLRDError error for file '" + filename +"': ", sys.exc_info()[0])
                with codecs.open(fs.path(xlsFile.name), encoding='utf16') as f:
                    for rowx, row in enumerate(f):
                        if row.endswith(u'\r\n'): row = row[:-2]
                        data = row.split(u'\t ,')
                        for colx, datum in enumerate(data):
                            if(rowx == 0):
                                if( datum.strip('"') == 'Last Name'):
                                    # print("last name = col[" + str(colx) +"]")
                                    lastCol = colx
                                elif( datum.strip('"') == 'First Name'):
                                    # print("first name = col[" + str(colx) +"]")
                                    firstCol = colx
                                elif( datum.strip('"') == 'Username'):
                                    # print("username = col[" + str(colx) +"]")
                                    userCol = colx
                            else:
                                if(colx == lastCol):
                                    last_name = datum.strip('"')
                                elif(colx == firstCol):
                                    first_name = datum.strip('"')
                                elif(colx == userCol):
                                    username = datum.strip('"')

                        if(rowx > 0):
                            new_student, created = classStudent.objects.get_or_create(
                                course = course,
                                studentID = username,
                                name = first_name + " " + last_name
                            )
                            if(created):
                                new_student_count += 1
                if(fs.exists(filename)):
                    # print("deleting file 2: ", xlsFile.name)
                    fs.delete(xlsFile.name)
                if(fs.exists(filename)):
                    # print("deleting file 1: ", filename)
                    fs.delete(filename)
                data = {
                    "bool":"true",
                    "new_count":new_student_count
                }
                return HttpResponse(
                    json.dumps(data),
                    content_type="application/json"
                )
            except:
                data = {
                    "bool":"false",
                    "msg": "Unexpected error"
                }
                print("Unexpected error 1:", sys.exc_info()[0])
                return HttpResponse(
                    json.dumps(data),
                    content_type="application/json"
                )
        else:
            data = {
                    "bool":"false",
                    "msg":"Get request"
                }
            return HttpResponse(
                json.dumps(data),
                content_type="application/json"
            )
    except Exception as e:
        data = {
            "bool":"false",
            "msg": e
        }
        print("Unexpected error 2:", e)
        return HttpResponse(
            json.dumps(data),
            content_type="application/json"
        )
    if filename:
        fs.delete(xlsFile.name)