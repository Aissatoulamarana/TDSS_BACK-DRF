# -*- encoding: utf-8 -*-
"""
Copyright (c) 2022 - OD
"""

import os
import decouple
from pathlib import Path
from datetime import timedelta


from django.contrib.messages import constants as messages

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = Path(__file__).parent.parent
CORE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = decouple.config(
    "SECRET_KEY",
    default="django-insecure-#4$gu+*w)!tnyja2bb-#1=+gw=636m*4y73a31e1yoqx)jcq@o",
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = decouple.config("DEBUG", default=True, cast=bool)

# load production server from .env
ALLOWED_HOSTS = ['*']

# ALLOWED_HOSTS = decouple.config(
#     "ALLOWED_HOSTS", cast=decouple.Csv(), default="127.0.0.1"
# )

CSRF_TRUSTED_ORIGINS = decouple.config("CSRF_TRUSTED_ORIGINS", cast=decouple.Csv(), default='http://localhost:3033')


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "apps.authentication",  # Enable the authentication app
    # "apps.administration",
    "apps.home",  # Enable the inner home (home)
    "apps.paiement",
    "corsheaders",
    "rest_framework",
    "rest_framework_api_key",
    'rest_framework.authtoken',
    'djoser',
    'rest_framework_simplejwt.token_blacklist',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
]

ROOT_URLCONF = "core.urls"
LOGIN_REDIRECT_URL = "apps/paiement"  # Route defined in home/urls.py
LOGOUT_REDIRECT_URL = "apps/paiement"  # Route defined in home/urls.py
TEMPLATE_DIR = os.path.join(BASE_DIR, "apps/templates")  # ROOT dir for templates

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [TEMPLATE_DIR],
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

WSGI_APPLICATION = "core.wsgi.application"

# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": decouple.config("DB_ENGINE", default="django.db.backends.sqlite3"),
        "NAME": decouple.config("DB_NAME", default=BASE_DIR / "db.sqlite3"),
        "USER": decouple.config("DB_USER", default=""),
        "PASSWORD": decouple.config("DB_PASSWORD", default=""),
        "HOST": decouple.config("DB_HOST", default=None),
        "PORT": decouple.config("DB_PORT", default=None),
        "CONN_MAX_AGE": 600,
    },
    "sqlite": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "mydatabase.sqlite",
    },
}

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

#############################################################
# SRC: https://devcenter.heroku.com/articles/django-assets

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/
# STATIC_ROOT = os.path.join(CORE_DIR, 'staticfiles')
# STATIC_URL = '/static/'

# # Extra places for collectstatic to find static files.
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'apps/static'),
)

# # Media files for user uploaded files
# MEDIA_ROOT = os.path.join(CORE_DIR, 'media')
# MEDIA_URL = 'media/'


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Authentication purpose
AUTH_USER_MODEL = 'authentication.CustomUser'


#Allowed frontend
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3033",  # Adresse du frontend Next.js
    "http://192.168.137.1:3033",
    "http://127.0.0.1:3033",
    
]


# Allowing non active users to try to log in.
AUTHENTICATION_BACKENDS = ["django.contrib.auth.backends.AllowAllUsersModelBackend"]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        "rest_framework.authentication.SessionAuthentication",
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',  # Bloque les endpoints sans token
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=7),  # Durée du token d'accès
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),  # Durée du refresh token
    'AUTH_HEADER_TYPES': ('Bearer',),
    'BLACKLIST_AFTER_ROTATION': True,  # Active la blacklist des refresh tokens après déconnexion
}

DJOSER = {
    'PASSWORD_RESET_CONFIRM_URL': 'password/reset/confirm/{uid}/{token}',
    "ACTIVATION_URL": "#/activate/{uid}/{token}",
    'SEND_ACTIVATION_EMAIL': True,
    'PASSWORD_RESET_CONFIRM_RETYPE': True,
    'LOGIN_FIELD': "email",
    'USERNAME_FIELD': "email",  # Désactive l'activation d'email (on le gère nous-mêmes)
    'SERIALIZERS': {
        'user_create': 'apps.authentication.serializers.CustomUserSerializer',
        'user': 'apps.authentication.serializers.CustomUserSerializer',
        'current_user': 'apps.authentication.serializers.CustomUserSerializer',

    },
    'SITE_NAME': "Declaration web site",
    'PASSWORD_RESET_SHOW_EMAIL_NOT_FOUND': True,
    'PERMISSIONS': {
        'user_list': ['rest_framework.permissions.IsAuthenticated'],  # Tous les utilisateurs connectés peuvent voir la liste
    }
}


# Settings for email configuration

EMAIL_BACKEND = decouple.config(
    "EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend"
)
EMAIL_USE_TLS = decouple.config("EMAIL_USE_TLS", default=False, cast=bool)
EMAIL_HOST = decouple.config("EMAIL_HOST", default='mail.tdss.com.gn')
EMAIL_PORT = int(decouple.config("EMAIL_PORT", default=1025))
EMAIL_HOST_USER = decouple.config("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = decouple.config("EMAIL_HOST_PASSWORD", default="mypassword")

#############################################################
#############################################################
#  Messages customize

MESSAGE_TAGS = {
    messages.DEBUG: "alert-info",
    messages.INFO: "alert-info",
    messages.SUCCESS: "alert-success",
    messages.WARNING: "alert-warning",
    messages.ERROR: "alert-danger",
}

# https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html
if decouple.config("USE_S3", default=False, cast=bool):
    AWS_S3_CUSTOM_DOMAIN = decouple.config(
        "AWS_S3_CUSTOM_DOMAIN", default="localhost:9000"
    )
    AWS_S3_URL_PROTOCOL = decouple.config("AWS_S3_URL_PROTOCOL", default="https:")

    STORAGES = {
        "default": {
            "BACKEND": "storages.backends.s3.S3Storage",
            "OPTIONS": {
                "location": "mediafiles",
                "default_acl": "public-read",
            },
        },
        "staticfiles": {
            "BACKEND": "storages.backends.s3.S3Storage",
            "OPTIONS": {
                'location': 'static',
                "default_acl": "public-read",
                "file_overwrite": False,
                "custom_domain": AWS_S3_CUSTOM_DOMAIN,
            },
        },
        # "staticfiles": {
        #     "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        # },
    }
    AWS_S3_SESSION_PROFILE = decouple.config("AWS_S3_SESSION_PROFILE", default=None)
    AWS_S3_ACCESS_KEY_ID = decouple.config("AWS_S3_ACCESS_KEY_ID", default=None)
    AWS_SECRET_ACCESS_KEY = decouple.config("AWS_SECRET_ACCESS_KEY", default=None)
    AWS_STORAGE_BUCKET_NAME = decouple.config(
        "AWS_STORAGE_BUCKET_NAME", default="raya-s3"
    )
    AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "max-age=86400"}
    AWS_S3_REGION_NAME = decouple.config("AWS_S3_REGION_NAME", default="eu-west-1")
    AWS_S3_ENDPOINT_URL = decouple.config(
        "AWS_S3_ENDPOINT_URL", default="http://minio:9000"
    )
    AWS_S3_VERIFY = decouple.config("AWS_S3_VERIFY", default=True, cast=bool)

    STATIC_URL = f'{AWS_S3_CUSTOM_DOMAIN}/static/'
    MEDIA_URL = f'{AWS_S3_CUSTOM_DOMAIN}/mediafiles/'
else:
    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/4.2/howto/static-files/

    MEDIA_ROOT = os.path.join(BASE_DIR, "media")
    MEDIA_URL = "/media/"

    STATIC_URL = "/static/"
    STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
