import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = 'so-cl*fc+ua7(=pjv#ehkt+hn$b9z55))c6t^3^7&n&47kq_a$'

DEBUG = True
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'cityproblems',
    'cityproblems.common',
    'cityproblems.site',
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