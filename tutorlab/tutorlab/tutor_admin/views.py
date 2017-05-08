import json, sys
from django.conf import settings 
from django.contrib.auth.models import User, Group
try:
    from django.contrib.sites.shortcuts import get_current_site
except ImportError:
    from django.contrib.sites.models import get_current_site
from django.core import signing
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from django.template import loader
from datetime import date, datetime
from ta_tutor.models import Session, Tutor, Notification
from .models import Term
from .forms import AddTermForm
from survey.models import Choice, Question, Survey
from home.models import CommonStudentIssue

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_RIGHT
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

from pusher import pusher
import datetime
from decimal import Decimal

# Attempt with Selenium
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# Initialize pusher
pusher_client = pusher.Pusher(app_id=settings.PUSHER_APP_ID,
                    key=settings.PUSHER_KEY,
                    secret=settings.PUSHER_SECRET)

def tutor_admin(request):
    if request.user.is_active:
        if not request.user.groups.filter(name='Tutor_Admin').exists():
            return HttpResponseRedirect('/')

        courses = populate_courses(request)
        print(courses)

        for course in courses:
            print(course)

        

        return render(request, 'instructor/home.html')
    else:
        return HttpResponseRedirect('/')

def student_sessions(request, abc123, classID):
    session_list = Session.objects.filter(student=abc123).filter(classID=classID).order_by('sessionID')

    return render(request, 'tutor_admin/studentdetail.html', {"student":abc123, "session_list":session_list})

def session_detail(request, id):
    session = get_object_or_404(Session, id=id)
    return render(request, 'tutor_admin/studentdata.html', {"session":session})

def tutor_sessions(request, id):
    tutor_obj = get_object_or_404(Tutor, id=id)
    session_list = Session.objects.filter(tutor=tutor_obj).order_by('-sessionID')
    return render(request, 'tutor_admin/tutordetail.html', {"tutor":tutor_obj, "session_list":session_list, "id":id})

def tutor_detail(request, id):
    session = get_object_or_404(Session, id=id)
    return render(request, 'tutor_admin/tutordata.html', {"session":session})

def tutor_report(request):
    # Term Selection
    term_selection = request.POST.getlist('term-report-list')
    if not term_selection:
        return HttpResponseRedirect("../")
    term_list = []
    if term_selection[0] == '--Include All--':
        term_list = Term.objects.all()
    else:
        for term in term_selection:
            term_list.append(Term.objects.get(name=term))

    #Tutor Selection
    tutor_selection = request.POST.getlist('tutor-report-list')
    if not tutor_selection:
        return HttpResponse("../")

                
    tutor_list = []
    if tutor_selection[0] == '--Include All--':
        for tutor in Tutor.objects.all():
            for term in term_list:
                if term.beforeTerm(tutor.tutor.date_joined.date()) is True:
                    tutor_list.append(Tutor.objects.get(name=tutor))
                elif term.inTerm(Tutor.objects.get(name=tutor).tutor.date_joined.date()) is True:
                    tutor_list.append(Tutor.objects.get(name=tutor))
                    
    else:
        for tutor in tutor_selection:
            for term in term_list:
                if term.beforeTerm(Tutor.objects.get(name=tutor).tutor.date_joined.date()) is True: 
                    tutor_list.append(Tutor.objects.get(name=tutor))
                elif term.inTerm(Tutor.objects.get(name=tutor).tutor.date_joined.date()) is True:
                    tutor_list.append(Tutor.objects.get(name=tutor))
                    
    tutors = []
    for tutor in tutor_list:
        if tutor not in tutors:
            tutors.append(Tutor.objects.get(name=tutor))

    # Survey Questions
    survey_questions = Question.objects.order_by('id')

    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="tutorreport_'+datetime.date.today().strftime("%m-%d-%Y")+'"'

    # # Create the PDF object, using the response object as its "file."
    # p = canvas.Canvas(response, pagesize=letter)
    doc = SimpleDocTemplate(response,pagesize=letter,
                        rightMargin=60,leftMargin=60,
                        topMargin=60,bottomMargin=18)
    Story = []

    # STYLES FOR DOCUMENT
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY, leading=18))
    styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER, leading=18))
    styles.add(ParagraphStyle(name='Right', alignment=TA_RIGHT, leading=18))
    styles.add(ParagraphStyle(name='Indent1', alignment=TA_JUSTIFY, leftIndent=15, leading=18))
    styles.add(ParagraphStyle(name='Indent2', alignmenet=TA_JUSTIFY, leftIndent=30, leading=18))

    ## TITLE AND DATE
    ptext = '<font size=12>TutorLab Tutor Report</font>'
    Story.append(Paragraph(ptext,styles['Center']))

    ptext = '<font size=12> {0} </font>'.format(datetime.date.today().strftime('%b %d, %Y'))
    Story.append(Paragraph(ptext,styles['Right']))

    ## LIST TERMS
    ptext = '<font size=12> Terms: </font>'
    Story.append(Spacer(1,18))
    Story.append(Paragraph(ptext,styles['Justify']))
    for term in term_list:
        ptext = '<font size=12> {0} </font>'.format(term.name)
        Story.append(Paragraph(ptext,styles['Indent1']))
    Story.append(Spacer(1,12))

    ## TUTOR STATISTICS
    for tutor in tutors:
        score = 0

        # Filter surveys by semester
        survey_all = tutor.survey_set.all()
        survey_list = []
        for survey in survey_all:
            for term in term_list:
                try:
                    if term.inTerm(survey.date_completed.date()) is True:
                        survey_list.append(survey)
                except:
                    pass                
        
        # Filter sessions by semester
        session_all = tutor.session_set.all()
        session_list = []
        for session in session_all:
            for term in term_list:
                try:
                    if term.inTerm(session.sessionID.date()) is True:
                        session_list.append(session)
                except:
                    pass

        # Average Total Survey Score
        for survey in survey_list:
            score += survey.score
        try:
            score = Decimal(score / len(survey_list))
            score = round(score, 2)
        except:
            print("except")
            score = 0

        ptext = '<font size=12> Tutor: {0} </font>'.format(str(tutor))
        Story.append(Paragraph(ptext,styles['Justify']))
        ptext = '<font size=12> Total Sessions: {0} </font>'.format(str(len(session_list)))
        Story.append(Paragraph(ptext,styles['Indent1']))
        ptext = '<font size=12> Surveys Completed: {0} </font>'.format(str(len(survey_list)))
        Story.append(Paragraph(ptext,styles['Indent1']))
        ptext = '<font size=12> Survey Feedback Score Average: {0} </font>'.format(str(score))
        Story.append(Paragraph(ptext,styles['Indent1']))

        qScores = [0,0,0,0,0]
        qIndex = 0

        for survey in survey_list:
            qScores[0] += int(survey.ans1[-1])
            qScores[1] += int(survey.ans2[-1])
            qScores[2] += int(survey.ans3[-1])
            qScores[3] += int(survey.ans4[-1])
            qScores[4] += int(survey.ans5[-1])

        for q in survey_questions:
            try:
                qScores[qIndex] = round(Decimal(qScores[qIndex] / len(survey_list)), 2)
            except:
                qScores[qIndex] = 0
            ptext = '<font size=12> -{0}:  {1}</font>'.format(q.question_text, qScores[qIndex])
            Story.append(Paragraph(ptext,styles['Indent2']))
            qIndex += 1

        ptext = '<font size=12> Survey Feedback Comments </font>'
        Story.append(Paragraph(ptext,styles['Indent1']))

        for survey in survey_list:
            if survey.comment:
                ptext = '<font size=12> -{0} </font>'.format(survey.comment)
                Story.append(Paragraph(ptext,styles['Indent2']))
        Story.append(Spacer(1,18))

    doc.build(Story)
    return response
    

def populate_courses(request):
    first_name = request.user.first_name
    last_name = request.user.last_name

    driver = webdriver.PhantomJS()
    driver.get("https://bluebook.utsa.edu")
    #assert "bluebook" in driver.title
    
    searchType_radioBUTTON = driver.find_element_by_id("ctl00_MainContentSearchQuery_searchCriteriaEntry_SearchTypeRBL_1")
    searchType_radioBUTTON.click()
    searchBox = driver.find_element_by_name("ctl00$MainContentSearchQuery$searchCriteriaEntry$FacultyTitleTxtBox")
    searchBox.clear()
    searchBox.send_keys(last_name + ", " + first_name)
    submitSearch_button = driver.find_element_by_id("ctl00_MainContentSearchQuery_searchCriteriaEntry_SearchBtn")
    submitSearch_button.click()

    term_radioBUTTON = driver.find_element_by_id("ctl00_MainContent_mainContent1_CourseTermSelectRBL_1")
    term_radioBUTTON.click()

    courses_div = driver.find_element_by_id("ctl00_MainContent_mainContent1_MainContentAccordion")
    courses = courses_div.find_elements_by_class_name("accordionMasterPane")
    course_list = []
    courses_final = []
    course_index = 0
    for course in courses:
        course_name = course.find_element_by_id("ctl00_MainContent_mainContent1_MainContentAccordion_Pane_"+str(course_index)+"_header_CourseLbl")
        course_list.append(course_name.find_element_by_xpath("..").text)
        course_index += 1

    for course in course_list:
        courses_final.append(course[3:])

    return courses_final

# CREATE A NEW USER AND TUTOR
def create_tutor(request):
    if request.method == 'POST':
        first = request.POST.get('tutor-first-name')
        last = request.POST.get('tutor-last-name')
        tutor_type = request.POST.get('tutor-type')
        username = request.POST.get('tutor-abc123')
        email = username + "@my.utsa.edu"
        try:
            get_object_or_404(User, username=username)
            return HttpResponse(
                json.dumps("false1"),
                content_type="application/json"
            )
        except:
            try:
                user = User.objects.create_user(username, email)
                user.first_name = first
                user.last_name = last
                user.is_active = False
                user.save()
                group = Group.objects.get(name='Tutor')
                group.user_set.add(user)
                tutor = Tutor.create(user)
                tutor.name = first + " " + last
                tutor.tutor_type = tutor_type
                tutor.save()
                if not send_activation(request, username, email):
                    return HttpResponse(
                        json.dumps("false4"),
                        content_type="application/json"
                    )
                return HttpResponse(
                    json.dumps("true"),
                    content_type="application/json"
                )
            except ValueError:
                return HttpResponse(
                    json.dumps("false2"),
                    content_type="application/json"
                )
            except:
                print("Unexpected error:", sys.exc_info()[0])
                return HttpResponse(
                    json.dumps("false3"),
                    content_type="application/json"
                )
    else:
        return HttpResponse(
            json.dumps("Post method only"),
            content_type="application/json"
        )

# SEND AN ACTIVATION EMAIL TO THE TUTOR 
def send_activation(request, username, email):
    try:
        # GET EMAIL TEMPLETS
        email_body = 'tutor_admin/email_temps/activation_body.txt'
        email_subject = 'tutor_admin/email_temps/activation_subject.txt'
        user = User.objects.get(username=username)
        token = signing.dumps(username, salt=settings.SECRET_KEY)
        user.tutor.token = token
        user.tutor.save()
        
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

# SEND NOTIFICATION TO TUTORS
def send_notification(request):
    if request.method == 'POST':
        tutorList = request.POST.getlist('tutor-list')
        message_title = request.POST.get('title')
        message = request.POST.get('message')
        all_tutors = Tutor.objects.all()
        if tutorList[0] == '--Send to All--':
            for tutor in all_tutors:
                notification = Notification.create(tutor)
                notification.message_title = message_title
                notification.message_content = message
                notification.save()
                pusher_client.trigger(u'notes', u'new',{})
                return HttpResponse(
                    json.dumps("true"),
                    content_type="application/json"
                )
        else:
            try:
                for name in tutorList:
                    for tutor in all_tutors:
                        if name == tutor.tutor.get_full_name():
                            notification = Notification.create(tutor)
                            notification.message_title = message_title
                            notification.message_content = message
                            notification.save()
                            break  
                pusher_client.trigger(u'notes', u'new',{})                     
                return HttpResponse(
                    json.dumps("true"),
                    content_type="application/json"
                )
            except:
                return HttpResponse(
                    json.dumps("false1"),
                    content_type="application/json"
                )
    else:
        return HttpResponse(
            json.dumps("GET METHOD"),
            content_type="application/json"
        )

# EDIT SURVEY QUESTIONS
def edit_questions(request):
    if request.method == 'POST':
        questions = request.POST.getlist('questions[]')
        for q in questions:
            qID, qText, cID = q.split(",")
            print(qID, qText, cID)
            try:
                question = Question.objects.get(id=qID)
                question.question_text = qText
                question.scale_choice = Choice.objects.get(id=cID)
                question.save()
            except:
                print("could not save question", q)

        return HttpResponse(
            json.dumps("true"),
            content_type="application/json"
        )
    else:
        print('get')
        return HttpResponse(
            json.dumps("GET METHOD"),
            content_type="application/json"
        )

# ADD RANGE VALUE FOR QUESTIONS
def add_range_value(request):
    if request.method == 'POST':
        low = request.POST.get('lowValue')
        high = request.POST.get('highValue')
        try:
            choice = Choice.objects.create(
                low = low,
                high = high,
            )
            data = {
                'bool':"true",
                'id':choice.id
            }
        except:
            data = {
                'bool':false
            }
        return HttpResponse(
                json.dumps(data),
                content_type="application/json"
            )

def delete_range_value(request):
    if request.method == 'POST':
        valueId = request.POST.get('id')
        try:
            choice = Choice.objects.get(id=valueId)
            choice.delete()
            data = {
                'bool':"true"
            }
        except:
            data = {
                'bool':"false"
            }
        return HttpResponse(
                    json.dumps(data),
                    content_type="application/json"
                )

def add_term(request):
    name = request.POST['term_name']
    start = request.POST['start_date']
    start = datetime.datetime.strptime(start, '%m/%d/%Y').strftime('%Y-%m-%d')
    end = request.POST['end_date']
    end = datetime.datetime.strptime(end, '%m/%d/%Y').strftime('%Y-%m-%d')

    new_term = Term.create(name,start,end)

    terms = Term.objects.all()
    names = []
    for term in terms:
        names.append(term.name)

    if name not in names:
        new_term.save()
        return HttpResponse(
            json.dumps("true"),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps("duplicate"),
            content_type="application/json"
        )
        

def delete_term(request):
    term = request.POST.get('delete-term-list')
    print(term)
    try:
        toDelete = Term.objects.get(name=term)
        toDelete.delete()
    except ObjectDoesNotExist:
        return HttpResponse(
            json.dumps("doesNotExist"),
            content_type="application/json"
        )
    
    return HttpResponse(
        json.dumps("true"),
        content_type="application/json"
    )

def edit_term(request):
    name = request.POST['edit-term-list']
    start = request.POST['edit_start_date']
    start = datetime.datetime.strptime(start, '%m/%d/%Y').strftime('%Y-%m-%d')
    end = request.POST['edit_end_date']
    end = datetime.datetime.strptime(end, '%m/%d/%Y').strftime('%Y-%m-%d')


    try:
        cur_term = Term.objects.get(name=name)
        cur_term.start = start
        cur_term.end = end
        cur_term.save()
    except ObjectDoesNotExist:
        return HttpResponse(
            json.dumps("doesnotexist"),
            content_type="application/json"
        )

    return HttpResponse(
        json.dumps("true"),
        content_type="application/json"
    )

def add_issue_list(request):
    if request.method == 'POST':
        issue = request.POST.get('issue')
        if issue == "":
            return HttpResponse(
                json.dumps("false1"),
                content_type="application/json"
            )
        try:
            new_issue = CommonStudentIssue.objects.create(
                issue = issue
            )
        except:
            return HttpResponse(
                json.dumps("false2"),
                content_type="application/json"
            )
        # pusher_client.trigger(u'admin_view', u'new',{})
        data = {"bool":'true', "id":new_issue.id}
        return HttpResponse(
            json.dumps(data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps("GET METHOD"),
            content_type="application/json"
        )

def delete_issue_list(request):
    if request.method == 'POST':
        issue_id = request.POST.get('issue_id')
        try:
            issue = CommonStudentIssue.objects.get(id = issue_id)
            issue.delete()
        except:
            return HttpResponse(
                json.dumps("false"),
                content_type="application/json"
            )
        # pusher_client.trigger(u'admin_view', u'new',{})
        return HttpResponse(
            json.dumps("true"),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps("GET METHOD"),
            content_type="application/json"
        )