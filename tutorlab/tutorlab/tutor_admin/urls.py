from django.conf.urls import url, include
from . import views
from instructor import views as ins_views
from django.views.generic import ListView, DetailView

from instructor.models import Student

app_name = 'tutor_admin'
urlpatterns = [
    # url(r'^$', views.tutor_admin, name='tutor_admin'),
    url(r'^$', ins_views.instructor, name='tutor_admin'),
    url(r'^add-issue-list/$', views.add_issue_list, name='add_issue_list'),
    url(r'^add-range-value/$', views.add_range_value, name='add_range_value'),
    url(r'^add-term/$', views.add_term, name='add_term'),
    url(r'^create-tutor/$', views.create_tutor, name='create_tutor'),
    url(r'^delete-issue-list/$', views.delete_issue_list, name='delete_issue_list'),
    url(r'^delete-range-value/$', views.delete_range_value, name='delete_range_value'),
    url(r'^delete-term/$', views.delete_term, name='delete_term'),
    url(r'^edit-questions/$', views.edit_questions, name='edit_questions'),
    url(r'^edit-term/$', views.edit_term, name='edit_term'),
    url(r'^send-notification/$', views.send_notification, name='send_notification'),
    url(r'^tutor_report/$', views.tutor_report, name='tutor_report'),
    url(r'^(?P<abc123>[A-z]{3}[0-9]{3})/(?P<classID>[0-9]{4}.[0-9]{3})/$', views.student_sessions, name='sessions'),
    url(r'^(?P<abc123>[A-z0-9]+)/(?P<classID>[0-9]{4}.[0-9]{3})/$', views.student_sessions, name='sessions'),#needs to be removed
    url(r'^[A-z]{3}[0-9]{3}/[0-9]{4}.[0-9]{3}/(?P<id>\d+)/$', views.session_detail, name='detail'),
    url(r'^[A-z]{6}/([0-9]{4}.[0-9]{3})/(?P<id>\d+)/$', views.session_detail, name='detail'),#needs to be removed
    url(r'^(?P<id>\d+)/$', views.tutor_sessions, name='tutor'),
    url(r'^[0-9]+/(?P<id>\d+)/$', views.tutor_detail, name='tutor_sessions'),

]
