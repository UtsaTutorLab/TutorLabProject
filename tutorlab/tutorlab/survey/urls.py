from django.conf.urls import url

from . import views

app_name = 'survey'
urlpatterns = [
    url(r'take-survey/(?P<token>[\w:-]+)/$', views.survey, name = 'survey'),
    url(r'thank-you/$', views.thankyou, name = 'thankyou'),
    url(r'survey-404/(?P<token>[\w:-]+)/$', views.survey_404, name = 'thankyou'),

]