from django.conf.urls import url, include
from . import views

app_name = 'student'
urlpatterns = [
   url(r'^$', views.student, name='student'),
   url(r'activate-student/(?P<token>[\w:-]+)$', views.activateStudent, name='activate_student'),
   url(r'confirm-appt/$', views.confirmAppt, name='confirm_appt'),
   url(r'create-appt/$', views.createAppt, name='create_appt'),
   url(r'create-student/$', views.createStudent, name='create_student'),
   url(r'delete-appt/$', views.deleteAppt, name='delete_appt'),
   url(r'delete-event/$', views.deleteEvent, name='delete_event'),
   url(r'request-new-tutor/$', views.newTutor, name='new_tutor'),
   url(r'api/cancel-request/$', views.cancelRequest, name='cancel_request'),
   url(r'api/delete-survey/$', views.deleteSurvey, name='delete_survey'),
   url(r'api/get-classes/$', views.getClasses, name='get_classes'),
   url(r'api/get-issue-list/$', views.getIssues, name='get_issues'),
   url(r'api/post-request/$', views.postRequest, name='post_request'),
   url(r'api/submit-survey/$', views.submitSurvey, name='submit_survey'),
]
 