"""
Django settings for OpenWasteMap project.

Generated by 'django-admin startproject' using Django 1.11.10.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = []

# some actions may not be performed in the test environment
IS_TEST = "test" in sys.argv

# can be overwritten in local_settings to check for existing tiles
# in the development environment
# in production this is performed by the webserver
CHECK_TILE_CACHE_HIT = False
TILES_ROOT = "/tiles"

# Application definition

INSTALLED_APPS = [
    "accounts.apps.AccountsConfig",
    "map_viewer.apps.MapViewerConfig",
    "waste_samples.apps.WasteSamplesConfig",
    "tile_server",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_sass",
    "django_email_verification",
    "mailer",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "openwastemap.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "openwastemap.wsgi.application"


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}

BROKER_TRANSPORT = "redis"
BROKER_URL = "redis://redis:6379/0"
CELERY_RESULT_BACKEND = BROKER_URL
CELERYBEAT_SCHEDULE_FILENAME = "/tmp/celerybeat"


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",  # noqa: E501
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Europe/Berlin"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = "/static/"
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static/"),)

# settings for account verification email
# overwrite in local_settings as necessary

EMAIL_BACKEND = "mailer.backend.DbBackend"
EMAIL_USE_TLS = True
EMAIL_SERVER = ""
EMAIL_ADDRESS = ""
EMAIL_FROM_ADDRESS = ""
EMAIL_PASSWORD = ""
EMAIL_PORT = 587
EMAIL_USER_MODEL_FK = "user"
EMAIL_USER_MODEL = "accounts.OWMUser"
EMAIL_ACTIVE_FIELD = "email_verified"
EMAIL_MAIL_SUBJECT = "OpenWasteMap Email Verification"
EMAIL_MAIL_HTML = "registration/verify_email.html"
EMAIL_MAIL_PLAIN = "registration/verify_email.txt"
EMAIL_PAGE_TEMPLATE = "registration/process_email_verification.html"
EMAIL_PAGE_DOMAIN = "http://www.openwastemap.org/"

OWM_VERSION = "0.6"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
