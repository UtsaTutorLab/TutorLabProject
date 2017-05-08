from django.conf import settings 
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core import signing
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail
from django.forms.formsets import formset_factory
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.template.context_processors import csrf
try:
    from django.contrib.sites.shortcuts import get_current_site
except ImportError:
    from django.contrib.sites.models import get_current_site
from pusher import pusher
from .forms import SessionForm
from .models import Tutor, ApptDate, Notification, Event
from student.models import Student, Queue
from survey.models import Survey
from home.models import App_Course
from collections import OrderedDict
import json

# Initialize pusher
pusher_client = pusher.Pusher(app_id=settings.PUSHER_APP_ID,
                    key=settings.PUSHER_KEY,
                    secret=settings.PUSHER_SECRET)

# TUTOR HOME PAGE INFO
def ta_tutor(request):
    if request.user.is_active:
        tutor = get_object_or_404(Tutor, tutor=request.user)
        student_queue = Queue.objects.order_by('id')
        student_list = Student.objects.order_by('id')
        course_list = App_Course.objects.all()
        requested_appts = ApptDate.objects.filter(tutor_approved = False).order_by('pk')
        request_num = requested_appts.count()
        notifications = Notification.objects.filter(tutor = tutor).order_by('-send_date')
        notification_num = notifications.filter(viewed=False).count()
    
        context = {
            'requested_appts':requested_appts,
            'request_num':request_num,
            'notifications':notifications,
            'notification_num':notification_num,
            'student_queue':student_queue,
            'tutor_info':tutor,
            'student_list':student_list,
            'course_list':course_list,
        }
        if not request.user.groups.filter(name='Tutor').exists():
            messages.error(request, "You do not have access to this page")
            return HttpResponseRedirect('/')
        return render(request, 'ta_tutor/home.html', context)
    else:
        messages.error(request, "You must login to see this page")
        return HttpResponseRedirect('/')

# ACTIVATE TUTOR ACCOUNT
def activate_account(request, token):
    try:
        abc123 = signing.loads(token,
                        max_age=(3600 * 24) * 7, #expires in one week
                        salt=settings.SECRET_KEY)
        user = get_object_or_404(User, username=abc123)
        if not user.tutor.token == token:
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
                        user.tutor.token = None
                        user.tutor.save()
                        return HttpResponse(
                            json.dumps("/ta_tutor"),
                            content_type="application/json"
                        )
        else:
            return render(request, 'ta_tutor/activate_account.html')
    except signing.BadSignature:
        raise Http404("Invalid token")

# GET ALL CALENDAR EVENTS FOR THIS TUTOR
def get_events(request):
    if request.method == 'GET':
        tutor = get_object_or_404(Tutor, tutor=request.user)
        calendar_events = Event.objects.filter(tutor = tutor).order_by('pk')
        #create calendar jason array from events model
        events = []
        for event in calendar_events:
            temp = OrderedDict()
            temp['id'] = event.id
            temp['title'] = event.student.student.username
            temp['student'] = event.student.student.first_name + " " + event.student.student.last_name
            temp['start'] = event.start
            temp['end'] = event.end
            temp['description'] = event.description
            temp['confirmed'] = event.confirmed
            temp['course'] = event.course
            events.append(temp)
        return HttpResponse(
            json.dumps(events),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps('This is only a \'GET\' API')
        )

# ADD REQUEST TO CALENDAR AS AN EVENT
def add_event(request):
    if request.method == 'POST':
        appt_pk = request.POST.get('appt_pk')
        appt = ApptDate.objects.get(pk=appt_pk)
        tutor = get_object_or_404(Tutor, tutor=request.user)
        event = Event.create(tutor)
        event.student = appt.student
        event.start = appt.appt_date
        event.course = appt.course_number
        event.description = appt.comments
        event.save()
        appt.event = event
        appt.tutor = tutor
        appt.tutor_approved = True
        appt.save()
        pusher_client.trigger(u'appt', u'new',{})
        return HttpResponse(
            json.dumps('appt added'),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps('appt was not added'),
            content_type="application/json"
        )

# DELETE EVENT FROM CALENDAR
def delete_event(request):
    if request.method == 'POST':
        delete_id = request.POST.get('deleted_appt')
        event = Event.objects.get(id=delete_id)
        appt = ApptDate.objects.get(event=event)
        appt.delete()
        event.delete()
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

# SEND NEW DATE BACK TO STUDENT
def send_date(request):
    if request.method == 'POST':
        event_id = request.POST.get('event_ID')
        new_date = request.POST.get('appt_date')
        if not new_date:
            return HttpResponse(
                json.dumps("false"),
                content_type="application/json"
            )
        else:
            event = get_object_or_404(Event, id=event_id)
            return_appt = get_object_or_404(ApptDate, event=event)
            event.start = new_date
            event.confirmed = False
            event.save()
            return_appt.old_appt_date = return_appt.appt_date
            return_appt.appt_date = new_date
            return_appt.student_approved = False
            return_appt.tutor_approved = True
            return_appt.save()
            pusher_client.trigger(u'appt', u'new',{})
            return HttpResponse(
                json.dumps(str(event_id) + " " + str(new_date)),
                content_type="application/json"
            )

# STARTS TUTORING SESSION
def startSession(request):
    studentName = request.POST.get('session-student-name')
    studentID = request.POST.get('studentID')
    classID = request.POST.get('class')
    tutor = get_object_or_404(Tutor, tutor=request.user)
    data = {
            'whole_name': studentName,
            'student': studentID,
            'classID': classID,
            'duration': '0',
            'notes':'',
            }
    form = SessionForm(data)
    form.fields['whole_name'].widget.attrs.update({'readonly':True, 'style':'border:0px'})
    form.fields['student'].widget.attrs.update({'readonly':True, 'style':'border:0px'})
    form.fields['classID'].widget.attrs.update({'readonly':True, 'style':'border:0px'})
    form.fields['duration'].widget.attrs.update({'readonly':True, 'style':'border:0px'})
    
    if request.user.is_active:
        if not request.user.groups.filter(name='Tutor').exists():
            messages.error(request, "You do not have access to this page")
            return HttpResponseRedirect('/')
        #pusher_client.trigger(u'ch1',u'enqueue',{u'data':'in session'})
        try:
            #if student is in queue list
            cur_stud = Queue.objects.get(abc123=studentID)
            # if student isn't in a session, set to True
            if cur_stud.inSession is False:
                cur_stud.inSession = True
                cur_stud.save()
                pusher_client.trigger(u'ch1',u'enqueue',{u'data':'in session'})
                return render(request, 'ta_tutor/session.html', {'studentName':studentName, 'studentID': studentID, 'classID': classID, 'form':form})
            #if student is in a session, just refresh page
            #elif cur_stud.inSession is True:
                #cur_stud.delete()
                
        except ObjectDoesNotExist:
            return render(request, 'ta_tutor/session.html', {'studentName':studentName, 'studentID': studentID, 'classID': classID, 'form':form})
        
        return HttpResponseRedirect('../')
    else:
        messages.error(request, "You must login to see this page")
        return HttpResponseRedirect('../')
    
# INSIDE TUTOR SESSION
def inSession(request):
    studentID = request.POST.get('student')
    tutor = get_object_or_404(Tutor, tutor=request.user)
    
    if request.method == "POST":
        form = SessionForm(request.POST)
        if form.is_valid():
            cur_session = form.save()
            cur_session.tutor = tutor
            cur_session.save()
            
            # Remove student object from queue list
            try:
                # CHECK IF STUDENT IS IN THE QUEUE
                cur_stud = Queue.objects.get(abc123=studentID)

                # CREATE NEW SURVEY OBJECT 
                survey = Survey.objects.create(
                    tutor = tutor,
                    student = studentID,
                )

                token = signing.dumps(survey.id, salt=settings.SECRET_KEY)
                survey.token = token
                survey.save()

                # DELETE STUDENT FROM QUEUE
                cur_stud.delete()

            except ObjectDoesNotExist:
                # send email if not chat or desktop request
                Send_Survey(request, studentID)
                print("student was not in the queue")
            
            # pusher_client.trigger(u'ch1',u'enqueue',{u'evansucks':'end session', u'student':studentID, u'tutor':tutor.id   })

            return HttpResponseRedirect('../')
        else:
            return render(request, 'ta_tutor/session.html', {'form':form})
    else:
        form = SessionForm()
        return render(request, 'ta_tutor/session.html', {'form':form})

# SEND SURVEY EMAIL FUNCTION
def Send_Survey(request, studentID):
    try:
        # GET EMAIL TEMPLETS
        email_template_name = 'ta_tutor/email_temps/survey_body.txt'
        email_subject_template_name = 'ta_tutor/email_temps/survey_subject.txt'

        # GET TUTOR OBJECT
        tutor = get_object_or_404(Tutor, tutor=request.user)

        # FIND STUDENT OBJECT IF THEY HAVE ACCOUNT
        try:
            student = User.objects.filter(groups__name__in=['Student']).get(username=studentID)
            studentEmail = student.email
            studentName = student.get_full_name()

        # ELSE USE THE ABC123
        except:
            studentEmail = studentID + "@my.utsa.edu"
            studentName = studentID

        # CREATE NEW SURVEY OBJECT 
        survey = Survey.objects.create(
            tutor = tutor,
            student = studentID,
        )

        token = signing.dumps(survey.id, salt=settings.SECRET_KEY)
        survey.token = token
        survey.save()

        # CONTEXT FOR EMAIL
        context = {
            'site': get_current_site(request),
            'username': studentName,
            'token': token,
            'secure': request.is_secure(),
        }

        # COMPILE EMAIL AND SEND
        body = loader.render_to_string(email_template_name,
                                        context).strip()
        subject = loader.render_to_string(email_subject_template_name,
                                            context).strip()
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL,
                    [studentEmail])
        return True
    except:
        # COULD NOT SEND EMAIL
        return False

# MARK TUTOR NOTIFICATIONS AS VIEWED
def viewed_notifications(request):
    try:
        tutor_id = request.POST.get('tutor_id')
        tutor = Tutor.objects.get(id=tutor_id)
        notifications = Notification.objects.filter(tutor=tutor)
        for note in notifications:
            note.viewed = True
            note.save()
        return HttpResponse(
            json.dumps('true'),
            content_type="application/json"
        )
    except:
        return HttpResponse(
            json.dumps('false'),
            content_type="application/json"
        )

def delete_notification(request):
    try:
        note_id = request.POST.get('note_id')
        note = Notification.objects.get(id=note_id)
        note.delete()
        return HttpResponse(
            json.dumps('true'),
            content_type="application/json"
        )
    except:
        return HttpResponse(
            json.dumps('false'),
            content_type="application/json"
        )