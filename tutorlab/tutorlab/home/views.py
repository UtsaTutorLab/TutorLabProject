from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.core.exceptions import ObjectDoesNotExist

from datetime import datetime
try:
    from django.contrib.sites.shortcuts import get_current_site
except ImportError:
    from django.contrib.sites.models import get_current_site
from django.core import signing
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

from .models import App_Course
from instructor.models import Instructor, Course, Student
from tutor_admin.models import Term
from ta_tutor.models import Session
from survey.models import Survey
from student.models import Student as StudentAccount

from pusher import Pusher, pusher
import codecs, json, sys, pyexcel as pe
from collections import defaultdict
from xlrd import XLRDError

# LOAD HOME PAGE
def index(request):
    return render(request, 'home/home.html')

# CONTACT US PAGE
def contact(request):
    context = {
        'contact': ['Email: UtsaTutorLab@gmail.com'],
        'title': "Contact Us",
    }
    return render(request, 'home/contact.html', context)

# LOGIN USER, REDIRECT TO THEIR PROFILE
def submit_login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            if user.groups.filter(name='Student').exists():
                return HttpResponse(
                    json.dumps("/student"),
                    content_type="application/json"
                )
            if user.groups.filter(name='Tutor').exists():
                return HttpResponse(
                    json.dumps("/ta_tutor"),
                    content_type="application/json"
                )
            if user.groups.filter(name='Tutor_Admin').exists():
                return HttpResponse(
                    json.dumps("/tutor_admin"),
                    content_type="application/json"
                )
            if user.groups.filter(name='Instructor').exists():
                return HttpResponse(
                    json.dumps("/instructor"),
                    content_type="application/json"
                )
            if username == 'admin' or username == 'bifrost_larry':
                return HttpResponse(
                    json.dumps("/admin"),
                    content_type="application/json"
                )
        else:
            return HttpResponse(
                json.dumps("false-1"),
                content_type="application/json"
            )
    else:
        return HttpResponse(
            json.dumps("false-2"),
            content_type="application/json"
        )

# LOGOUT USER
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

# REDIRECT TO USER PROFILE
def profile(request):
    user = request.user
    if user is not None:
        if user.is_active:
            if user.groups.filter(name='Student').exists():
                return HttpResponseRedirect('/../student/')
            if user.groups.filter(name='Tutor').exists():
                return HttpResponseRedirect('/../ta_tutor/')
            if user.groups.filter(name='Instructor').exists():
                return HttpResponseRedirect('/../instructor/')
            if user.groups.filter(name='Tutor_Admin').exists():
                return HttpResponseRedirect('/../instructor/')
            if user.username == 'admin' or  user.username == 'bifrost_larry':
                return HttpResponseRedirect('/../admin/')
        else:
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')

@csrf_exempt
def pusher_authentication(request):
	pusher_client = pusher.Pusher(app_id=settings.PUSHER_APP_ID,key=settings.PUSHER_KEY,secret=settings.PUSHER_SECRET)
	pusher_client.trigger(u'ch1',u'enqueue',{})	

	return HttpResponse("Ooh secret")

# SHOWS ALL TUTORS SCHEDULES
def ta_schedule(request):
    context = {
        'title': "Tutor Schedule",
    }
    return render(request, 'home/schedule.html', context)




@login_required(login_url='/admin/')
def admin_import(request):
    if request.user.is_active:
        if not request.user.is_superuser:
            return HttpResponseRedirect('/profile')
        if request.method == "GET":
            return render(request, "home/admin_import.html")
        if request.method == "POST" and request.FILES['file']:
            xlsFile = request.FILES['file']
            i_first_name = i_last_name = i_user_name = i_email = class_name = class_num = s_first_name = s_last_name = s_user_name = ' '
            num_i = num_c = num_s = 0
            try:
                fs = FileSystemStorage()
                filename = fs.save(xlsFile.name, xlsFile)
                print("File name =", xlsFile)
                sheet = pe.get_sheet(file_name=fs.path(xlsFile.name), name_columns_by_row=0)
                records = sheet.to_records()
                for record in records:
                    keys = sorted(record.keys())
                    for key in keys:
                        if key == "Instructor First Name":
                            print(str(record[key]))
                            i_first_name = record[key]
                        elif key == "Instructor Last Name": 
                            print(str(record[key]))
                            i_last_name = record[key]
                        elif key == "Instructor Username": 
                            print(str(record[key]))
                            i_user_name = record[key]
                        elif key == "Instructor Email":
                            print(str(record[key]))
                            i_email = record[key]
                        elif key == "Class Name":
                            print(str(record[key]))
                            class_name = record[key]
                        elif key == "Class Number":
                            print(str(record[key]))
                            class_num = record[key]
                        elif key == "Student abc123":
                            print(str(record[key]))
                            s_user_name = record[key]
                        elif key == "Student First Name":
                            print(str(record[key]))
                            s_first_name = record[key]
                        elif key == "Student Last Name":
                            print(str(record[key]))
                            s_last_name = record[key]

                    # Get or create user
                    user, user_created = User.objects.get_or_create(username=i_user_name, first_name=i_first_name, last_name=i_last_name, email=i_email)
                    group = Group.objects.get(name='Instructor')
                    group.user_set.add(user)
                    # Get or create current instructor
                    cur_instructor,created = Instructor.objects.get_or_create(user=user, first_name=i_first_name, last_name=i_last_name, email=i_email)
                    cur_instructor.save()

                    if(user_created):
                        # send email to setup password
                        send_activation(request, user.username, user.email)
                        num_i+=1

                    # Get or create current course and associate with instructor
                    cur_course, course_created = Course.objects.get_or_create(course_num=class_num, course_name=class_name)
                    cur_course.save()
                    cur_course.Instructor = cur_instructor
                    cur_course.save()
                    if(course_created):
                         num_c+=1                    
                    
                    # Get or create current student and associate with course
                    cur_student, student_created = Student.objects.get_or_create(first_name=s_first_name, last_name=s_last_name, studentID=s_user_name)
                    cur_student.save()
                    cur_student.courses.add(cur_course)
                    cur_student.save()
                    if(student_created):
                        num_s+=1
        
                fs.delete(xlsFile.name)
                data = {
                    "bool":"true",
		    "i_created":num_i,
                    "c_created":num_c,
                    "s_created":num_s
                }
                return HttpResponse(
                    json.dumps(data),
                    content_type="application/json"
                )


            except XLRDError:
                print("xlrd error")
                lastCol = firstCol = userCol = 0
                i_last_name = i_first_name = i_email = class_name = class_num = s_first_name = s_last_name = s_user_name = ""
                fs = FileSystemStorage()
                filename = fs.save(xlsFile.name, xlsFile)
                with codecs.open(fs.path(xlsFile.name), encoding='UTF-16') as f:
                    for rowx, row in enumerate(f):
                        if row.endswith(u'\r\n'): row = row[:-2]
                        data = row.split(u'\t ,')
                        for colx, datum in enumerate(data):
                            info = datum.strip("'\"")
                            if(rowx == 0):
                                if( info == 'Instructor First Name'):
                                    print(info)
                                    iFirstCol = colx
                                elif( info == 'Instructor Last Name'):
                                    print(info + str(colx))
                                    iLastCol = colx
                                elif( info == 'Instructor Email'):
                                    print(info + str(colx))
                                    iEmailCol = colx
                                elif( info == 'Class Name'):
                                    print(info + str(colx))
                                    cNameCol = colx
                                elif( info == 'Class Number'):
                                    print(info + str(colx))
                                    cNumCol = colx
                                elif( info == 'Student First Name'):
                                    print(info + str(colx))
                                    sFirstCol = colx
                                elif( info == 'Student Last Name'):
                                    print(info + str(colx))
                                    sLastCol = colx
                                elif( info == 'Student abc123'):
                                    print(info + str(colx))
                                    sUserCol = colx
                            else:
                                if(colx == iLastCol):
                                    # print("Instructor last name = col[" + str(colx) +"]", info)
                                    i_last_name = info
                                elif(colx == iFirstCol):
                                    # print("Instructor first name = col[" + str(colx) +"]", info)
                                    i_first_name = info
                                elif(colx == iEmailCol):
                                    # print("Instructor Email = col[" + str(colx) +"]", info)
                                    i_email = info
                                elif(colx == cNameCol):
                                    # print("Class name = col[" + str(colx) +"]", info)
                                    class_name = info
                                elif(colx == cNumCol):
                                    # print("Class num = col[" + str(colx) +"]", info)
                                    class_num = info
                                elif(colx == sUserCol):
                                    # print("username = col[" + str(colx) +"]", info)
                                    s_user_name = info
                                elif(colx == sFirstCol):
                                    # print("Student first name = col[" + str(colx) +"]", info)
                                    s_first_name = info
                                elif(colx == sLastCol):
                                    # print("Student last name = col[" + str(colx) +"]", info)
                                    s_last_name = info

                        if(rowx > 0):
                            # Get or create user
                            user, user_created = User.objects.get_or_create(username=i_user_name, first_name=i_first_name, last_name=i_last_name, email=i_email)
                            group = Group.objects.get(name='Instructor')
                            group.user_set.add(user)
                            # Get or create current instructor
                            cur_instructor,created = Instructor.objects.get_or_create(first_name=i_first_name, last_name=i_last_name, email=i_email)
                            cur_instructor.save()
                            # Get or create current course and associate with instructor
                            cur_course, created = Course.objects.get_or_create(course_num=class_num, course_name=class_name)
                            cur_course.save()
                            cur_course.Instructor = cur_instructor
                            cur_course.save()
                            # Get or create current student and associate with course
                            cur_student,created = Student.objects.get_or_create(first_name=s_first_name, last_name=s_last_name, studentID=s_user_name)
                            cur_student.save()
                            cur_student.courses.add(cur_course)
                            cur_student.save()
                    
            except Exception as e:
                print("Error in upload:", e)

            if(fs.exists(filename)):
                # print("deleting file 2: ", xlsFile.name)
                fs.delete(xlsFile.name)
            if(fs.exists(filename)):
                # print("deleting file 1: ", filename)
                fs.delete(filename)
            
            data = {
                'bool': 'false'
            }

            return HttpResponse(
                json.dumps(data),
                content_type = "application/json"
            )
        
def admin_purge(request):
    if request.method == "GET":
        terms = Term.objects.all()
        context = {
            'terms':terms
        }
        return render(request, "home/admin_purge.html", context)
        
    if request.method == "POST":
        
        ######### DELETE TERMS, SESSIONS, SURVEYS #########

        termList = request.POST.getlist('selectedTerms[]')
        terms = []
        data = {}

        if "None" in termList:
            if len(termList) > 1:
                data['term-issue'] = "None selected in term selection list"
                data['bool-term'] = "false"
            else:
                data['term-issue'] = "No surveys or student-tutor sessions deleted"
                data['bool-term'] = "true"
        else:  
            for term in termList:
                terms.append(Term.objects.get(name=term))
            surveys = Survey.objects.all()
            sessions = Session.objects.all()
            surveysToDelete = []
            sessionsToDelete = []
            for term in terms:
                for survey in surveys:
                    if term.inTerm(survey.date_completed.date()):
                        surveysToDelete.append(survey)
                for session in sessions:
                    if term.inTerm(session.sessionID.date()):
                        sessionsToDelete.append(session)
            
            # Delete surveys and minus count from tutor
            for survey in surveysToDelete:
                survey.tutor.survey_count -= 1
                survey.tutor.save()
                survey.delete()
            # Delete sessions
            for session in sessionsToDelete:
                session.delete()
            # Delete terms
            for term in terms:
                term.delete()
        
        ######## DELETE COURSES AND STUDENTS AND STUDENT ACCOUNTS ###########
        Course.objects.all().delete()
        Student.objects.all().delete()
        for student in StudentAccount.objects.all():
            if student.student.last_login.date() < datetime.today().date().replace(year = datetime.today().year - 1):
                student.user.delete()

        data['bool-term'] = 'true'

        return HttpResponse(
            json.dumps(data),
            content_type = "application/json"
        )

@login_required(login_url='/admin/')
def admin_manage(request):
    if request.user.is_active:
        if not request.user.is_superuser:
            return HttpResponseRedirect('/profile')
        if request.method == "GET":
            instructors = Instructor.objects.all()
            tutor_admins = []
            for instructor in instructors:
                if instructor.user:
                    if instructor.user.groups.filter(name="Tutor_Admin"):
                        tutor_admins.append(instructor)
            context = {
                "instructors": instructors,
                "tutor_admins": tutor_admins
            }
            return render(request, "home/admin_manage.html", context)
        if request.method == "POST":
            action = request.POST.get("action")
            instructors = request.POST.getlist("selectedInstructors[]")
            
            if "None" not in instructors:
                if action == "delete":
                    try:
                        for instructor in instructors:
                            cur_instructor = Instructor.objects.get(email=instructor)
                            cur_instructor.user.delete()
                        data = {
                            "bool":"true",
                            "msg":"Instructor(s) deleted"
                        }
                    except ObjectDoesNotExist:
                        data = {
                            "bool":"false",
                            "msg":"Could not delete instructor (Does Not Exist)"
                        }
                elif action == "addAdmin":
                    group = Group.objects.get(name='Tutor_Admin')
                    for instructor in instructors:
                        cur_instructor = Instructor.objects.get(email=instructor)
                        group.user_set.add(cur_instructor.user)
                    data = {
                            "bool":"true",
                            "msg":"Instructor(s) given Tutor-Admin status"
                        }
                elif action == "remAdmin":
                    group = Group.objects.get(name='Tutor_Admin')
                    for instructor in instructors:
                        cur_instructor = Instructor.objects.get(email=instructor)
                        group.user_set.remove(cur_instructor.user)
                    data = {
                            "bool":"true",
                            "msg":"Instructor(s) revoked of Tutor-Admin status"
                        }
            else:
                data = {
                    "bool":"false",
                    "msg": "None selected in instructor selection"
                }

            return HttpResponse(
                json.dumps(data),
                content_type = "application/json"
            )
        
def send_activation(request, username, email):
    try:
        # GET EMAIL TEMPLETS
        email_body = 'home/email_temps/activation_body.txt'
        email_subject = 'home/email_temps/activation_subject.txt'
        user = User.objects.get(username=username)
        instructor = Instructor.objects.get(user = user)
        token = signing.dumps(username, salt=settings.SECRET_KEY)
        instructor.token = token
        instructor.save()
        
        # CONTEXT FOR EMAIL
        context = {
            'site': get_current_site(request),
            'username': user.get_full_name(),
            'token': token,
            'secure': request.is_secure(),
        }
        body = loader.render_to_string(email_body, context).strip()
        subject = loader.render_to_string(email_subject, context).strip()
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [email])
        return True
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return False
