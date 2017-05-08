from django.conf.urls import url, include
from . import views

app_name = 'home'
urlpatterns = [
    url(r'^$', views.index, name='home'),
    url(r'^contact/$', views.contact, name='contact'),
    url(r'^login/$', views.submit_login, name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'schedule/$', views.ta_schedule, name='schedule'),
    url(r'^pusher_authenticate/$', views.pusher_authentication, name='auth'),
    url(r'^admin_import/$', views.admin_import, name='admin_import'),
    url(r'^admin_purge/$', views.admin_purge, name='admin_purge'),
    url(r'^admin_manage/$', views.admin_manage, name='admin_manage')
]
