from django.conf.urls import url, include
from . import views

app_name = 'ta_tutor'
urlpatterns = [
    url(r'^$', views.ta_tutor, name='ta_tutor'),
    url(r'activate-tutor/(?P<token>[\w:-]+)/$', views.activate_account, name='activate_account'),
    url(r'add-event/$', views.add_event, name='add_appt'),
    url(r'delete-event/$', views.delete_event, name='delete_appt'),
    url(r'delete-notification/$', views.delete_notification, name='delete_notification'),
    url(r'get-events/$', views.get_events, name='get_appts'),
    url(r'send-date/$', views.send_date, name='send_date'),
    url(r'^session/$', views.inSession, name='inSession'), 
    url(r'start-session/$', views.startSession, name='start_session'),
    url(r'viewed/$', views.viewed_notifications, name='viewed'), 
]
