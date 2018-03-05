"""
Django settings for britecore project.

Generated by 'django-admin startproject' using Django 2.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
try:
    from britecore.local_settings import local_settings  # @UnresolvedImport
except:
    local_settings = {}

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'yf*e^dqt2b4^lnf8$1kqotk&2w!-ab!nc83jl$++g-ztn8xd^+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["127.0.0.1", "localhost", "f2uddx7bli.execute-api.us-east-2.amazonaws.com"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',
    'main',
    'rest_framework'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'britecore.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'britecore.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': local_settings.get('DB_DEFAULT_SETTINGS', {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'britecoretest',
        'USER': 'britecoretestadmin7bli',
        'PASSWORD': 'fhuryg^&^%3et64%&&*derrf2390',
        'HOST': 'rds-postgresql-7bli.cth7mcrqx10m.us-east-2.rds.amazonaws.com',
        'PORT': '5432',
    }), #super user credentials: admin (Adm!n123@#$)
}


# Fixtuers
# https://docs.djangoproject.com/en/2.0/howto/initial-data/#providing-initial-data-with-fixtures
FIXTURE_DIRS = (
    os.path.join(BASE_DIR, 'fixtures')
)


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

#STATIC_URL = '/static/'


# Static files on Amazon S3
# http://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html

AWS_S3_HOST = 's3.us-east-2.amazonaws.com'

AWS_STORAGE_BUCKET_NAME = 'zappa-static-7bli'

AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

AWS_HEADERS = {'Cache-Control': 'max-age=86400', }

STATIC_URL = local_settings.get('STATIC_URL', "https://%s/" % AWS_S3_CUSTOM_DOMAIN)

STATICFILES_STORAGE = local_settings.get('STATICFILES_STORAGE', 'storages.backends.s3boto.S3BotoStorage')

DEPLOYMENT_STAGE = 'dev'

# Login Specific Settings

LOGIN_URL = local_settings.get('LOGIN_URL', '/%s/login/' % DEPLOYMENT_STAGE)

LOGOUT_REDIRECT_URL = 'url_default'

