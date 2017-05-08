from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, Group
try:
    from django.contrib.sites.shortcuts import get_current_site
except ImportError:
    from django.contrib.sites.models import get_current_site
from django.core import serializers, signing
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

from .models import Student, Queue
from .forms import ApptDateForm
from home.models import App_Course, CommonStudentIssue
from instructor.models import Course, CustomIssueSet, Student as courseStudent
from survey.models import Survey, Question
from ta_tutor.models import ApptDate, Event

from pusher import pusher
import json, sys, threading, time

pusher_client = pusher.Pusher(app_id=settings.PUSHER_APP_ID,
                        key=settings.PUSHER_KEY,
                        secret=settings.PUSHER_SECRET)

#LOADS STUDENT BASE PAGE AND BASIC INFO
def student(request):
    if request.user.is_active:
        student = get_object_or_404(Student, student=request.user)
    
        pusher_client.trigger(u'ch1',u'enqueue',{u'msg':'somehting else'})
        if not request.user.groups.filter(name='Student').exists():
            return HttpResponseRedirect('/')
        return render(request, 'student/home.html', {'student_info':student})
    else:
        return HttpResponseRedirect('/')

# CREATE NEW STUDENT
def createStudent(request):
    if request.method == "POST":
        first = request.POST.get('first')
        last = request.POST.get('last')
        username = request.POST.get('abc123')
        prefered_email = request.POST.get('email')
        email = username + "@my.utsa.edu"
        print(first, last, username, prefered_email, email)
        if first is None or first == "":
            return HttpResponse(
                # all fields are needed
                    json.dumps("false2"),
                    content_type="application/json"
                )
        elif last is None or last == "":
            return HttpResponse(
                    json.dumps("false2"),
                    content_type="application/json"
                )
        elif username is None or username == "":
            return HttpResponse(
                    json.dumps("false2"),
                    content_type="application/json"
                )
        elif prefered_email is None or prefered_email == "":
            return HttpResponse(
                    json.dumps("false2"),
                    content_type="application/json"
                )
        try:
            print("get student")
            get_object_or_404(User, username=username)
            print("got student")
            return HttpResponse(
                # student aldredy exists
                json.dumps("false1"),
                content_type="application/json"
            )
        except:
            try:
                print("no student")
                user = User.objects.create_user(username, prefered_email)
                user.first_name = first
                user.last_name = last
                user.is_active = False
                user.save()
                group = Group.objects.get(name='Student') 
                group.user_set.add(user)
                student = Student.objects.create(
                        student=user,
                        first_name=first,
                        last_name=last,
                        abc123=username
                    )
                student.save()
                if not send_activation(request, username, email):
                    print("no email")
                    student.delete()
                    user.delete()
                    return HttpResponse(
                        # could not send email, delete account
                        json.dumps("false4"),
                        content_type="application/json"
                    )
                return HttpResponse(
                        # every thing works
                        json.dumps("true"),
                        content_type="application/json"
                    )
            except ValueError:
                return HttpResponse(
                    # some value is incorrect
                    json.dumps("false2"),
                    content_type="application/json"
                )
            except:
                print("Unexpected error:", sys.exc_info()[0])
                return HttpResponse(
                    # could not create student
                    json.dumps("false3"),
                    content_type="application/json"
                )
    else:
        return render(request, 'student/newuser.html')

# SEND AN ACTIVATION EMAIL TO THE STUDENT 
def send_activation(request, username, email):
    try:
        # GET EMAIL TEMPLETS
        email_body = 'student/email_temps/activation_body.txt'
        email_subject = 'student/email_temps/activation_subject.txt'
        user = User.objects.get(username=username)
        token = signing.dumps(username, salt=settings.SECRET_KEY)
        user.student.token = token
        user.student.save()
        
        # CONTEXT FOR EMAIL
        context = {
            'site': get_current_site(request),
            'username': user.get_full_name(),
            'token': token,
            'secure': request.is_secure(),
        }
        body = loader.render_to_string(email_body,
                                        context).strip()
        subject = loader.render_to_string(email_subject,
                                            context).strip()
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL,
                    [email])
        return True
    except:
        print("Unexpected error:", sys.exc_info()[0])
        return False


# ACTIVATE STUDENT
def activateStudent(request, token):
    try:
        abc123 = signing.loads(token,
                        max_age=(3600 * 24), #expires in one day
                        salt=settings.SECRET_KEY)
        user = get_object_or_404(User, username=abc123)
        if not user.student.token == token:
            raise Http404("Your token is not valid")
        elif request.method == 'POST':
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
                        user.student.token = None
                        user.student.save()
                        return HttpResponse(
                            json.dumps("/student"),
                            content_type="application/json"
                        )
        else:
            return render(request, 'student/activate_student.html')
    except signing.BadSignature:
        raise Http404("Invalid token")

# CREATE NEW APPT REQUEST
def createAppt(request):
    if request.user.is_active:
        student = get_object_or_404(Student, student=request.user)
        appts = ApptDate.objects.filter(student=student).order_by('pk')

        if request.method == 'POST':
            form = ApptDateForm(request.POST)
            if form.is_valid():
                form.save()
                pusher_client.trigger(u'appt', u'new',{})
                return HttpResponse(
                    json.dumps("true"),
                    content_type="application/json"
                )
            else:
                return HttpResponse(
                    json.dumps("false"),
                    content_type="application/json"
                )
        else:
            form = ApptDateForm(initial={'student':student})
            try:
                form.fields['course_number'].queryset = courseStudent.objects.get(studentID=student.abc123).courses
            except:
                form.fields['course_number'].queryset = []
        return render(request, 'student/appointment.html', {'form': form, 'appts':appts})
    else:
        messages.error(request, 'Please Login ')
        return HttpResponseRedirect('/')

# DELETE STUDENT APPT REQUEST
def deleteAppt(request):
    if request.method == 'POST':
        try:
            appt_id = request.POST.get("appt_id")
            appt = get_object_or_404(ApptDate, id=appt_id)
            appt.delete()
            pusher_client.trigger(u'appt', u'new',{})
            return HttpResponse(
                json.dumps("true"),
                content_type="application/json"
            )
        except:
            return HttpResponse(
                json.dumps("false"),
                content_type="application/json"
            )
    else:
        return HttpResponse(
            json.dumps("This is a post request only"),
            content_type="application/json"
        )

# DELETE STUDENT APPT IN TUTOR CALENDAR
def deleteEvent(request):
    if request.method == 'POST':
        try:
            appt_id = request.POST.get("appt_id")
            appt = get_object_or_404(ApptDate, id=appt_id)
            event = appt.event
            event.delete()
            pusher_client.trigger(u'appt', u'new',{})
            return HttpResponse(
                json.dumps("true"),
                content_type="application/json"
            )
        except:
            return HttpResponse(
                json.dumps("false"),
                content_type="application/json"
            )
    else:
        return HttpResponse(
            json.dumps("This is a post request only"),
            content_type="application/json"
        )

# CONFIRM TUTOR NEW APPT DATE
def confirmAppt(request):
    if request.method == 'POST':
        try:
            appt_id = request.POST.get("appt_id")
            appt = get_object_or_404(ApptDate, id=appt_id)
            event = appt.event
            appt.old_appt_date = None
            appt.student_approved = True
            event.confirmed = True
            appt.save()
            event.save()
            pusher_client.trigger(u'appt', u'new',{})
            return HttpResponse(
                json.dumps("true"),
                content_type="application/json"
            )
        except:
            return HttpResponse(
                json.dumps("false"),
                content_type="application/json"
            )
    else:
        return HttpResponse(
            json.dumps("This is a post request only"),
            content_type="application/json"
        )

# STUDENT REQUEST FOR NEW TUTOR INSTEAD OF CONFIRM NEW DATE
def newTutor(request):
    if request.method == 'POST':
        try:
            appt_id = request.POST.get("appt_id")
            appt = get_object_or_404(ApptDate, id=appt_id)
            event = appt.event
            appt.appt_date = appt.old_appt_date
            appt.student_approved = True
            appt.tutor_approved = False
            appt.event = None
            appt.save()
            event.delete()
            pusher_client.trigger(u'appt', u'new',{})
            return HttpResponse(
                json.dumps("true"),
                content_type="application/json"
            )
        except:
            return HttpResponse(
                json.dumps("false"),
                content_type="application/json"
            )
    else:
        return HttpResponse(
            json.dumps("This is a post request only"),
            content_type="application/json"
        )


#-------- CODE FOR DESKTOP APPLICATION --------#


def getClasses(request):
    abc123 = request.GET.get('abc123')
    names = [["---Select Class---",0]]
    
    if courseStudent.objects.filter(studentID=abc123):
        student = courseStudent.objects.get(studentID=abc123)
        courses = student.courses.all()
        for course in courses:
            name = []
            name.append(course.course_name)
            name.append(course.id)
            names.append(name)
    else:
        courses = App_Course.objects.all()
        for ndx, course in enumerate(courses):
            if ndx == 14:
                break
            name = []
            name.append(course.course_name)
            name.append(0)
            names.append(name)
    return HttpResponse(
        json.dumps(names),
        content_type="application/json"
    )

def getIssues(request):
    studentCourse = request.GET.get('course')
    issue_list = ["---Select Issue---"]
    try:
        course = Course.objects.get(id = studentCourse)
        if CustomIssueSet.objects.filter(course=course):
            customSet = CustomIssueSet.objects.filter(course=course)
        for custom in customSet:
            issue_list.append(custom.issue.issue)
    except:
        issues = CommonStudentIssue.objects.all()
        for issue in issues:
            issue_list.append(issue.issue)
    return HttpResponse(
        json.dumps(issue_list),
        content_type="application/json"
    )

@csrf_exempt
def postRequest(request):
    app_key = request.POST.get('app_key')
    if app_key == settings.SECRET_KEY:
        fullname = request.POST.get('fullname')
        abc123 = request.POST.get('abc123')
        chairNumber = request.POST.get('chairNumber')
        courseName = request.POST.get('className')
        courseID = request.POST.get('classId')
        question = request.POST.get('question')
        host = request.POST.get('host')
        port = request.POST.get('port')
        try:
            course = Course.objects.get(id=courseID)
            courseNum = course.course_num
        except:
            courseNum = 0
        try:
            queue_obj = Queue.objects.create(
                abc123 = abc123,
                whole_name = fullname,
                chair = chairNumber,
                className = courseName,
                classID = courseNum,
                question = question,
                host = host,
                port = port
            )
            pusher_client.trigger(u'ch1',u'enqueue',{})
            queue_num = Queue.objects.filter(id__lte = queue_obj.id).count()
            data = {
                'bool':"True",
                'num':queue_num
            }
        except Exception as e:
            print("Error in student app request: " + str(e))
            data = {
                'bool':"False",
                'message':"Could not add to queue,\nYou are probably already in the queue"
            }
        
    else:
        data = {
            'bool':"false",
            'message':"Invalid App Key"
        }
    return HttpResponse(
            json.dumps(data),
            content_type="application/json"
        )

@csrf_exempt
def cancelRequest(request):
    app_key = request.POST.get('app_key')
    if app_key == settings.SECRET_KEY:
        abc123 = request.POST.get('abc123')
        try:
            queue_obj = Queue.objects.get(abc123=abc123)
            queue_obj.delete()
            pusher_client.trigger(u'ch1',u'enqueue',{})
            data = {
                'bool':"true",
                'message':"Student found"
            }
        except:
            data = {
                'bool':"false", 
                'message':"No student found"
            }
    else:
        data = {
            'bool':"false", 
            'message':"Invalid App Key"
        }
    return HttpResponse(
        json.dumps(data),
        content_type="application/json"
    )

@csrf_exempt
def submitSurvey(request):
    app_key = request.POST.get('app_key')
    if app_key == settings.SECRET_KEY:
        surveyToken = request.POST.get('survey_token')
        ans = []
        for x in range(1,6):
            ans.append(request.POST.get('ans'+str(x)))
        comment = request.POST.get('comment')
        score = 0
        for a in ans:
            score += int(a[-1])
        try:
            survey = Survey.objects.get(token=surveyToken)
            survey.ans1 = ans[0]
            survey.ans2 = ans[1]
            survey.ans3 = ans[2]
            survey.ans4 = ans[3]
            survey.ans5 = ans[4]
            survey.comment = comment
            survey.score = score
            survey.token = None
            survey.save()
            data = {
                'bool':"True",
                'message':"Survey submitted"
            }
        except:
            data = {
                'bool':"False",
                'message':"Survey could not be found"
            }
    else:
        data = {
            'bool':"False",
            'message':"Invalid App Key"
        }
    return HttpResponse(
        json.dumps(data),
        content_type="application/json"
    )

@csrf_exempt
def deleteSurvey(request):
    app_key = request.POST.get('app_key')
    if app_key == settings.SECRET_KEY:
        surveyToken = request.POST.get('survey_token')
        try:
            survey = Survey.objects.get(token=surveyToken)
            survey.delete()
            data = {
                'bool':"True",
                'message':"Survey deleted"
            }
        except:
            data = {
                'bool':"False",
                'message':"Survey could not be found"
            }
    else:
        data = {
            'bool':"False",
            'message':"Invalid App Key"
        }
    return HttpResponse(
        json.dumps(data),
        content_type="application/json"
    )