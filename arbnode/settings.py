"""
Django settings for arbnode project.

Generated by 'django-admin startproject' using Django 3.2.12.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/

"""

from pathlib import Path
import json
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
with open('/root/django_secret.txt') as f:
    SECRET_KEY = f.read().strip()

with open('/root/master_key.txt') as f:
    MASTER_KEY = f.read().strip()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1','arbitrum.ftkuhnsman.com','66.94.106.218','livepeer.ftkuhnsman.com','rpc.ftklivepeer.net','*']


# Application definition

INSTALLED_APPS = [
    'django_prometheus',
    'api.apps.ApiConfig',
    'infra.apps.InfraConfig',
    'django_celery_beat',
    'django_celery_results',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'redis_cache',
]


MIDDLEWARE = [
    #'request_profiler.middleware.ProfilingMiddleware',
    'django_prometheus.middleware.PrometheusBeforeMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_prometheus.middleware.PrometheusAfterMiddleware',
]

ROOT_URLCONF = 'arbnode.urls'

CSRF_TRUSTED_ORIGINS = ['https://rpc.ftklivepeer.net','https://arbitrum.ftkuhnsman.com','https://livepeer.ftkuhnsman.com','https://*.127.0.0.1']

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
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

WSGI_APPLICATION = 'arbnode.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases
#with open('/root/DATABASES.json') as json_file:
#    databases = json.load(json_file)

#DATABASES = databases

DATABASES = { 'default':
    {
        'ENGINE':'django.db.backends.sqlite3',
        'NAME':BASE_DIR / 'db.sqlite',
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


import os
STATIC_URL = '/static/'
STATIC_ROOT = '/etc/static'
STATICFILES_DIR = (
        os.path.join(BASE_DIR, "static"),
)

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CACHES = {
    "default": {
        "BACKEND": "redis_cache.RedisCache",
        "LOCATION": "localhost:6379",
    }
}

CACHALOT_UNCACHABLE_APPS = ('payments','lpdata','info')

CELERY_RESULT_BACKEND = "django-db"

DBBACKUP_STORAGE = 'django.core.files.storage.FileSystemStorage'
DBBACKUP_STORAGE_OPTIONS = {'location': '/home/ghost/arbnode_db_backups/'}

USE_X_FORWARDED_HOST = True

PROMETHEUS_METRICS_EXPORT_PORT_RANGE = range(8001, 8050)


STRIPE_PUBLISHABLE_KEY = 'pk_live_51Kod8AGJroezaJBhEM28vIk53IMygBiFtNdzbClTmZ1NBn5ffVx72usiFH0pmz1hK5FeKE5y1ES8mDd84nvXAo8M00C44zpc3R'
STRIPE_SECRET_KEY = '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'
STRIPE_WEBHOOK_SECRET = 'whsec_uG4XPfkSShiwDLKHpekmuWly7lhS5O7r'


X_FRAME_OPTIONS = 'SAMEORIGIN'

SILKY_PYTHON_PROFILER = False

SILKY_PYTHON_PROFILER_BINARY = False

SILKY_PYTHON_PROFILER_RESULT_PATH = os.path.join(BASE_DIR, "profiles")

SILKY_META = False

SILKY_INTERCEPT_PERCENT = 5
