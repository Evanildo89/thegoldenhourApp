
from pathlib import Path
import dj_database_url
import os

import os

# Segredos e config do ambiente
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-temporaria')
DEBUG = os.getenv('DEBUG', 'False') == 'True'


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
    "thegoldenlight.com",
    "www.thegoldenlight.com",
    "thegoldenhourapp.onrender.com",
    "thegoldenhour-frontend.onrender.com",
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'services',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'backend.urls'

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

WSGI_APPLICATION = 'backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

USE_SQLITE_LOCAL = os.environ.get("USE_SQLITE_LOCAL", "False") == "True"

if DEBUG or USE_SQLITE_LOCAL:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    # Usando PostgreSQL (produção ou teste local)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('PG_DB', 'thegoldenhour_local'),  # seu banco local
            'USER': os.getenv('PG_USER', 'myuserr'),           # seu usuário local
            'PASSWORD': os.getenv('PG_PASSWORD', 'Rodrigues89&'),  # senha
            'HOST': os.getenv('PG_HOST', 'localhost'),        # localhost para teste
            'PORT': os.getenv('PG_PORT', '5432'),             # porta padrão
        }
    }

MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

# Emails
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', EMAIL_HOST_USER)


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = '/static/'
# STATICFILES_DIRS = [
#     BASE_DIR / "frontend_build",
# ]
STATIC_ROOT = BASE_DIR / "staticfiles"

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # desenvolvimento
    "https://thegoldenhour-frontend.onrender.com",  # produção
]

if DEBUG:
    # Ambiente de desenvolvimento (localhost)
    BASE_URL = "http://localhost:3000"  # ou porta que usas para servir o HTML/React
else:
    # Ambiente de produção
    BASE_URL = "https://thegoldenhour-frontend.onrender.com"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {'class': 'logging.StreamHandler'},
    },
    'root': {'handlers': ['console'], 'level': 'DEBUG'},
}