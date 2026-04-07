from pathlib import Path
import os
import dj_database_url
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG', 'False') == 'True'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '*').split(',')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'main.middleware.LoginRequiredMiddleware',
]

ROOT_URLCONF = 'bestlogs.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'bestlogs.wsgi.application'

DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///db.sqlite3'
    )
}

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

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

LOGOUT_REDIRECT_URL = 'login'
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'home'

# FLUTTERWAVE SETTINGS
FLW_PUBLIC_KEY = os.getenv('FLW_PUBLIC_KEY')
FLW_SECRET_KEY = os.getenv('FLW_SECRET_KEY')
FLW_REDIRECT_URL = os.getenv('FLW_REDIRECT_URL')


#
# LANGUAGE_CODE = 'en-us'
# TIME_ZONE = 'UTC'
# USE_I18N = True
# USE_TZ = True
#
# STATIC_URL = 'static/'
# STATIC_ROOT = BASE_DIR / 'staticfiles'
#
# DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
#
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
#
# EMAIL_HOST_USER = 'bestlogsfeedback@gmail.com'
# EMAIL_HOST_PASSWORD = 'akhc zmdb uqfk ytgw'
#
# DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
#
# LOGOUT_REDIRECT_URL = 'login'
# LOGIN_URL = 'login'
# LOGIN_REDIRECT_URL = 'home'
#
#
# # =========================
# # FLUTTERWAVE SETTINGS
# # =========================
# FLW_PUBLIC_KEY = "FLWPUBK-bf440c08ef5889a363b693ea34911e30-X"
# FLW_SECRET_KEY = "FLWSECK-b5f8da225aadffb318f2586d831ed348-19d0b97b9bfvt-X"
# FLW_REDIRECT_URL = "http://127.0.0.1:8000/flutterwave/callback/"
#
#
#
#
#
#
