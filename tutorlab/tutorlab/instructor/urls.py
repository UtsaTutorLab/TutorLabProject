from django.conf.urls import url, include
from . import views
from django.views.generic import ListView, DetailView

from instructor.models import Student

app_name = 'instructor'
urlpatterns = [
    url(r'^$', views.instructor, name='instructor'),
    url(r'^(?P<abc123>[A-z]{3}[0-9]{3})/$', views.student_sessions, name='sessions'),
    url(r'^(?P<abc123>[A-z]{6})/$', views.student_sessions, name='sessions'),
    url(r'^(?P<abc123>[A-z]{3}[0-9]{3})/(?P<classID>[0-9]{4}.[0-9]{3})/$', views.student_sessions, name='sessions'),
    url(r'^(?P<abc123>[A-z0-9]+)/(?P<classID>[0-9]{4}.[0-9]{3})/$', views.student_sessions, name='sessions'),#needs to be removed
    url(r'^[A-z]{3}[0-9]{3}/([0-9]{4}.[0-9]{3})/(?P<id>\d+)/$', views.session_detail, name='detail'),
    url(r'^[A-z]{6}/([0-9]{4}.[0-9]{3})/(?P<id>\d+)/$', views.session_detail, name='detail'),#needs to be removed
    url(r'^activate-account/(?P<token>[\w:-]+)/$', views.activate_account, name='activate_account'),
    url(r'^delete-issue-from-set/$', views.delete_from_custom_list, name='delete-issue-from-set'),
    url(r'^get-students/$', views.get_students, name='get-students'),
    url(r'^get-custom-issue-list/$', views.get_custom_issue_list, name='get-custom-issue-list'),
    url(r'^add-custom-issue-list/$', views.add_custom_issue_list, name='add-custom-issue-list'),
    url(r'^add-students-to-class/$', views.add_students_to_class, name='add-students-to-class'),
    # url(r'^studentdetail/$', ListView.as_view(queryset=Student.objects.all().order_by("name"), template_name="instructor/studentdetail.html")),
    # url(r'^studentdetail/(?P<pk>\d+)$', DetailView.as_view(model=Student, template_name="instructor/studentdata.html")),

]
