# -*- coding: utf-8 -*-
# Django settings for prx_vademecum project.

DEBUG = False
TEMPLATE_DEBUG = DEBUG

CSRF_COOKIE_NAME = 'vademecumcsrfcookie'

ADMINS = (
     ('Help Desk', 'helpdesk@pcaaudit.com'),
     ('Miguel Ambrosio', 'miguel.ambrosio@pcaaudit.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'vademecum',
        'USER': 'leer_vademecum',
        'PASSWORD': 'PRX_password_9763',
        'HOST': '',
        'PORT': '',
    }
}


TIME_ZONE = 'America/Caracas'

LANGUAGE_CODE = 'es'

SITE_ID = 1




# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = ''

STATIC_ROOT = '/home/vademecum/vademecum/static'

#STATIC_URL = 'http://vademecum.pcaaudit.com/static/'
STATIC_URL = 'http://prxvademecum.com/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '0mr(p&amp;3gf$^5*)q-pn405q*^ie8j_)j^s#fs7+f9g-au0-2vrd'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    #'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'prx_vademecum.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'prx_vademecum.wsgi.application'

TEMPLATE_DIRS = (
    '/home/vademecum/my_templates'
)

# Set your DSN value
RAVEN_CONFIG = {
    'dsn': 'http://248162c1af154a7c9be886f409a7acc8:fe8bc50ce18f47f2bf41bad6c505d3f2@pcaaudit.com:9000/3',
}

INSTALLED_APPS = (
    'django.contrib.staticfiles',
    'vademecum',
    'raven.contrib.django.raven_compat',
    #'django.contrib.admin'
)

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
)

ALT_EMAIL_HOST = 'smtp.sendgrid.net'
ALT_EMAIL_HOST_PASSWORD = 'prx400881390'
ALT_EMAIL_HOST_USER = 'prxsolutions'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# Configuración de Correos Electrónicos de Django
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'info@pcaaudit.com'
EMAIL_HOST_PASSWORD = 'prxinfo2012'
EMAIL_PORT = 587 #Con TLS
EMAIL_USE_TLS = True 
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER

IDIOMA_PRINCIPIOS = 'ES'#'EN'#

PAIS_VADEMECUM = 'VE'

# LOCAL SETTINGS
try:
    from local_settings import *
except ImportError:
    pass
