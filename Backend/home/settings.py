"""
Django settings for home project.
"""

import os
from pathlib import Path
from datetime import timedelta
from urllib.parse import urlparse, parse_qsl
import dotenv

dotenv.load_dotenv()

# Base Directory
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', '(c@9=wl&3=c#nm@=5#hn$#dpw5zqm0vvmojfcr!d7%&7&ofz2n')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    'c00edd481226.ngrok-free.app',
]

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Django Sites Framework (REQUIRED for Allauth Social Accounts)
    'django.contrib.sites',

    # Custom apps
    'core',
    'users',
    'blogs',

    # Third-party
    'corsheaders',
    'rest_framework',
    'rest_framework.authtoken',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
]

SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'home.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'home.wsgi.application'

# Database Setup: Uses DATABASE_URL if available, otherwise defaults to SQLite
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    tmpPostgres = urlparse(DATABASE_URL)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': (tmpPostgres.path or '').lstrip('/'),
            'USER': tmpPostgres.username,
            'PASSWORD': tmpPostgres.password,
            'HOST': tmpPostgres.hostname,
            'PORT': tmpPostgres.port or 5432,
            'OPTIONS': dict(parse_qsl(tmpPostgres.query)),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Custom user model
AUTH_USER_MODEL = 'users.CustomUser'

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

# Default auto field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ---------------------------------------------------------------------------
# REST Framework Configuration
# NOTE: There must be ONLY ONE REST_FRAMEWORK dict in this file.
# Defining it twice means the second one silently overwrites the first,
# which was the root cause of the "token not valid for any token type" bug
# (JWTCookieAuthentication was overriding JWTAuthentication).
# ---------------------------------------------------------------------------
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.ScopedRateThrottle',
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ),
    'DEFAULT_THROTTLE_RATES': {
        'user': '1000/day',
        'anon': '100/day',
        'dj_rest_auth': '10/min',  # <--- Itha add pannunga!
    },
}

# JWT configuration
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}

# CORS for React frontend
CORS_ALLOW_ALL_ORIGINS = os.getenv("CORS_ALLOW_ALL_ORIGINS", "True") == "True"
CORS_ALLOWED_ORIGINS = os.getenv("CORS_ALLOWED_ORIGINS", "").split()
CORS_ALLOW_CREDENTIALS = True

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

# ---------------------------------------------------------------------------
# Redirect users back to your React frontend after successful login/signup.
# NOTE: Only one LOGIN_REDIRECT_URL is kept — point it at wherever you want
# Google/allauth logins to land. Change this if you want it to go to
# 'http://localhost:3000/' instead of the dashboard.
# ---------------------------------------------------------------------------
LOGIN_REDIRECT_URL = 'http://localhost:3000/dashboard'
ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'http'

SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        },
        'OAUTH_PKCE_ENABLED': True,
        'FETCH_USERINFO': True,
    }
}

SOCIALACCOUNT_STORE_TOKENS = True
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_LOGIN_ON_GET = True

ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_LOGIN_METHODS = {"email"}
ACCOUNT_SIGNUP_FIELDS = ["email*", "password1*", "password2*"]
ACCOUNT_ADAPTER = 'allauth.account.adapter.DefaultAccountAdapter'

# Email backend
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "True") == "True"
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", EMAIL_HOST_USER)
PASSWORD_RESET_TIMEOUT = 60 * 60 * 4

# CSRF
CSRF_COOKIE_NAME = "csrftoken"
CSRF_COOKIE_HTTPONLY = False

# API Keys (Fallback to dummy values in local dev to prevent crashes)
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY", "dummy_key_for_local_dev")
PLAGIARISM_API_HOST = os.getenv("PLAGIARISM_API_HOST", "dummy_host_for_local_dev")

# Celery Configuration
CELERY_BROKER_URL = os.getenv('REDIS_URL', 'redis://127.0.0.1:6379/0')
CELERY_RESULT_BACKEND = os.getenv('REDIS_URL', 'redis://127.0.0.1:6379/0')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Karachi'
CELERY_ENABLE_UTC = True

# Directory where generated PDFs will be stored temporarily
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'