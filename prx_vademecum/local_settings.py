# -*- coding: utf-8 -*-

from django.utils.translation import ugettext as _
ADMINS = (
     ('Narbe', 'narbelys@gmail.com'),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'vademecum14', #'audit',#'APS', #'PCAFarmaJulio', #'APS', #'Farma15-4', #'APSAon', #'IntegracionAPS', #'APS', #''pcaaudit0508', #'PCAfarma', # 'PCAaudit14-02-14',#'caroni11-11-13',#'aon05-12-13',#' ''backupaon', #sanitas',#, #,  # #'pcaaudit0508',#'pcaaudit',#'prxsys',                          # Or path to database file if using sqlite3.
        'USER': 'root',                      # Not used with sqlite3.
        'PASSWORD': 'root',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.                      # Set to empty string for default. Not used with sqlite3.
    }
}

 # Desactivar sentry local: Unset your DSN value
RAVEN_CONFIG = {}

ADMIN_MEDIA_PREFIX = '/home/narbe/Documentos/vademecum_eeuu/admin/'
#STATIC_ROOT = '/home/narbe/Documentos/PCAaudit/PRXAnalyzer/static/'
STATIC_ROOT = '/home/narbe/Documentos/vademecum/vademecum_eeuu/static/'

# URL prefix for static files.
STATIC_URL  = '/static/'
#STATIC_URL  = 'http://pcaaudit.com/static/'

MEDIA_ROOT = '/home/narbe/vademecum_eeuu/'

TEMPLATE_DIRS = (
    '/home/narbe/Documentos/vademecum_eeuu/my_templates'
)

INSTALLED_APPS = (
    'django.contrib.staticfiles',
    'vademecum',
    'raven.contrib.django.raven_compat',
    'django.contrib.staticfiles',
    #'django.contrib.admin',
)

#MEDIA_ROOT = '/home/narbe/vademecum'

LOG_PATH = '/home/narbe/Documentos/logs/'
CODIGOS_PATH = '/home/narbe/Documentos/codigosBR/'
INFORMES_URL = 'http://localhost:8081/static/informes/'
INFORMES_PATH = '/home/narbe/Documentos/vademecum_eeuu/static/informes/'

#EMAIL_HOST = 'smtp.sendgrid.net'
#EMAIL_HOST_USER = 'prxsolutions'
#EMAIL_HOST_PASSWORD = 'prx400881390'
ALT_EMAIL_HOST = 'smtp.sendgrid.net'
ALT_EMAIL_HOST_PASSWORD = 'prx400881390'
ALT_EMAIL_HOST_USER = 'prxsolutions'

DEBUG = True

APIKEY_MERCANTIL = 'd3822d68357ccf6284e2a9c1bb874baa'
APIKEY_PCA_MERCANTIL = '8dc9a76d227626ebae23c266b56699db'



#LOGIN_CARONI = True#False#



LOCALE_PATHS = (
    '/home/narbe/Documentos/vademecum_eeuu/locale',
)

LANGUAGE_COOKIE_NAME='langcookiei18n'

LANGUAGES = (
  ('es', _('Spanish')),
  ('en', _('English')),
)

IDIOMA_PRINCIPIOS = 'ES'#'ES'#

PAIS_VADEMECUM = 'CO'

LANGUAGE_CODE = 'es'

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

