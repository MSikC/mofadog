# -*- coding:utf-8 -*-
"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 1.10.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
from django.utils.translation import ugettext_lazy as _

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


ALLOWED_HOSTS = ['*']

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'pv0cfy=f#92jci%__tc#0bsj26xvem8@k*rqae7x3dd5@em-8l'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False



# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'django_crontab',
    'registration',
    'pages',
    'dashboard',
    'payment',
    'cron',
    'sudashboard',
]

AUTHENTICATION_BACKENDS = ['pages.backends.EmailBackend']


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mysite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR + "/templates/"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
            ],
        },
    },
]

WSGI_APPLICATION = 'mysite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'myproject',
        'USER': 'mxcpy',
        'PASSWORD': 'mxcpy529',
        'HOST': 'localhost',
        'PORT': '',
    }
}



# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/


TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
]


ACCOUNT_ACTIVATION_DAYS = 7
REGISTRATION_DEFAULT_FROM_EMAIL = True
REGISTRATION_AUTO_LOGIN = True
SITE_ID = 1


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp.gmail.com' # replace with your smtp server's address
EMAIL_PORT = 587 # replace with your smtp server's port
EMAIL_HOST_USER = 'mofadogofficial@gmail.com' # replace with your smtp server account username
EMAIL_HOST_PASSWORD = 'lbjame529' # replace with your smtp server account password
EMAIL_USE_TLS = True

#EFAULT_FROM_EMAIL = EMAIL_HOST_USER
'''
EMAIL_HOST = 'localhost' # replace with your smtp server's address
EMAIL_PORT = 25 # replace with your smtp server's port
EMAIL_HOST_USER = '' # replace with your smtp server account username
EMAIL_HOST_PASSWORD = '' # replace with your smtp server account password
EMAIL_USE_TLS = False
DEFAULT_FROM_EMAIL = 'mofadog@mofadog.com'
'''
LANGUAGES = (
    ('en', _('English')),
    ('zh-hans', _('Chinese')),
)

LANGUAGE_CODE = 'zh-hans'
LOCALE_PATHS = (
    "/root/myproject/locale/",
)


CRONJOBS = [
    ('00 * * * *', 'cron.cronbeat.beat'),
    ('00 08 01 * *', 'cron.cronbeat.month_beat')
]