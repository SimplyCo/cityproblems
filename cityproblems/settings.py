import os
from django.core.urlresolvers import reverse_lazy
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

try:
    from .settings_mail import *
except ImportError:
    MAIL_SENDER_SERVER = 'smtp.example.com'
    MAIL_SENDER_PORT = 25
    MAIL_SENDER_USER = 'test@example.com'
    MAIL_SENDER_PASSWORD = 'passwd'
    MAIL_SENDER_SENDER = 'test@example.com'
    MAIL_SENDER_ORGANIZATION = u'Cityproblems'
    MAIL_SENDER_MAILER = u'Cityproblems mail'

SECRET_KEY = 'so-cl*fc+ua7(=pjv#ehkt+hn$b9z55))c6t^3^7&n&47kq_a$'

DEBUG = True
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = ['*']

AUTH_USER_MODEL = 'accounts.User'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'cityproblems',
    'cityproblems.common',
    'cityproblems.site',
    'cityproblems.mailsender',
    'cityproblems.accounts',
    'cityproblems.admin',

    'bootstrapform',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    #'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'django.core.context_processors.i18n',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'cityproblems.site.context_processors.get_settings',
    )

ROOT_URLCONF = 'cityproblems.urls'

#WSGI_APPLICATION = 'cityproblems.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Kiev'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = 'static/'
MEDIA_ROOT = u'{}'.format(BASE_DIR)
MEDIA_URL = '/media/'
LOGIN_REDIRECT_URL = reverse_lazy("site_user_cabinet")
ADMIN_USER_OBJECTS_PER_PAGE = 20
# celery
BROKER_URL = 'redis://localhost:6379/0'