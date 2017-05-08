"""tutorlab URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    url(r'^', include('home.urls')),
    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^nested_admin/', include('nested_admin.urls')),
    url(r'^student/', include('student.urls')),
    url(r'^instructor/', include('instructor.urls')),
    url(r'^ta_tutor/',include('ta_tutor.urls')),
    url(r'^tutor_admin/', include('tutor_admin.urls')),
    url(r'^survey/', include('survey.urls')),
    url(r'^password_reset/',include('password_reset.urls')),
    url(r'^msg/',include('messenger.urls')),
    url(r'^forum/', include('forum.urls')),
]

#if settings.DEBUG:
#    urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
#    urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)