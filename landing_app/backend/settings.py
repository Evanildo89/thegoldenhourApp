from pathlib import Path
import dj_database_url
import os
from decouple import config
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# garante que o .env seja carregado
dotenv_path = BASE_DIR / '.env'
dotenv_local_path = BASE_DIR / '.env.local'

if config("DEBUG", default=False, cast=bool):
    # Em desenvolvimento carrega .env.local
    if dotenv_local_path.exists():
        load_dotenv(dotenv_local_path)
else:
    # Em produção, ignora .env.local e usa apenas .env
    if dotenv_path.exists():
        load_dotenv(dotenv_path)

EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
print("DEBUG EMAIL_HOST_USER:", EMAIL_HOST_USER)  # debug

# Segredos e config do ambiente
SECRET_KEY = config('SECRET_KEY', default='django-insecure-temporaria')
DEBUG = config('DEBUG', default=False, cast=bool)
DATABASE_URL = config('DATABASE_URL')


# Allowed hosts
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

MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

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
USE_SQLITE_LOCAL = config("USE_SQLITE_LOCAL", default=False, cast=bool)
DATABASE_URL = config("DATABASE_URL", default=f"sqlite:///{BASE_DIR}/db.sqlite3")

if DEBUG or USE_SQLITE_LOCAL:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    # Configuração para PostgreSQL em produção com SSL
    DATABASES = {
        "default": dj_database_url.parse(DATABASE_URL, conn_max_age=600, ssl_require=True)
    }

# Emails
EMAIL_BACKEND = "sgbackend.SendGridBackend"
SENDGRID_API_KEY = config("SENDGRID_API_KEY")
DEFAULT_FROM_EMAIL = "evanildovrodrigues@gmail.com"
ADMIN_EMAIL = "evanildovrodrigues@gmail.com"

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# CORS
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "https://thegoldenhour-frontend.onrender.com",
]

# Permite credenciais (cookies, autenticação)
CORS_ALLOW_ALL_ORIGINS = True

# Permite todos os métodos HTTP
CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]

# Permite todos os cabeçalhos necessários
CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]

# Base URL
BASE_URL = config('BASE_URL', default='http://localhost:3000')
print("BASE_URL final:", BASE_URL)

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {'console': {'class': 'logging.StreamHandler'}},
    'root': {'handlers': ['console'], 'level': 'DEBUG'},
}