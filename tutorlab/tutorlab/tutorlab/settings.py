"""
Django settings for tutorlab project.

Generated by 'django-admin startproject' using Django 1.9.7.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'cdyna7f^!8c=#$-#nw5@j&$7ig-)li8@53$-=z78vccn0b+(y#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Credentials for pusherable app
PUSHER_APP_ID = u"262197"
PUSHER_KEY = u"4a389ab4ef763883473e"
PUSHER_SECRET = u"074bfac4fe9d5afcc868"

#for gmail account
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'utsatutorlab@gmail.com'
EMAIL_HOST_PASSWORD = 'computerscience'
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER

#experation tokens (in seconds)
SURVEY_TOKEN_EXPIRES = 3600 * 24 #one day
PASSWORD_RESET_TOKEN_EXPIRES = 3600 #one hour
ROOM_TOKEN_EXPIRES = 3600 #one hour

#!!!!!! MUST CHANGE LATER TO STATIC VALUE!!!!!!!
ALLOWED_HOSTS = ['*'] 

# Application definition

INSTALLED_APPS = [
    'home',
    'student',
    'instructor',
    'ta_tutor',
    'tutor_admin',
    'forum.apps.ForumConfig',
    'survey.apps.SurveyConfig',
    'pusherable',
    'channels',
    'messenger',
    'nested_admin',
    'password_reset',
    'datetimewidget',
    'admin_tools',
    'admin_tools.theming',
    'admin_tools.menu',
    'admin_tools.dashboard',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

ROOT_URLCONF = 'tutorlab.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        # 'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'loaders': {
            'admin_tools.template_loaders.Loader',
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        }
        },
        
    },
]

WSGI_APPLICATION = 'tutorlab.wsgi.application'

CHANNEL_LAYERS = {
	"default": {
		#"BACKEND": "asgiref.inmemory.ChannelLayer",
		 "BACKEND": "asgi_redis.RedisChannelLayer",
		 "CONFIG": {
		 	"hosts": [os.environ.get('REDIS_URL', 'redis://localhost:6379')],
		 },
		"ROUTING": "tutorlab.routing.channel_routing",
	},
}

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
	'ENGINE': 'django.db.backends.mysql',
	# 'NAME': 'bifrost_larry',
	# 'USER': 'bifrost_larry',
	# 'PASSWORD': 'BaBaarJRerTsR1py',
	# 'HOST': 'easel2.fulgentcorp.com',
    	'NAME':'tutorlabdb',
    	'USER':'root',
    	'PASSWORD':'computerscience',
    	'HOST':'localhost',
	'PORT': '3306',
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

ADMIN_TOOLS_INDEX_DASHBOARD = 'dashboard.CustomIndexDashboard'
ADMIN_TOOLS_APP_INDEX_DASHBOARD = 'dashboard.CustomAppIndexDashboard'

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Chicago'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'

#STATIC_ROOT = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static")
]
STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static_cdn")

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), "media_cdn")


# Blackboard oAuth
# Application Key:  10e5ab5a-fea2-49e7-9d18-48cdec9247f8
# Secret:	        aFu2rBTBFJat9EiuLY5VBWFWUZ4ddoJm