
import os
from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv
from cryptography.fernet import Fernet

# Load environment variables from .env
load_dotenv()

CHAT_ENCRYPTION_KEY = os.getenv("CHAT_ENCRYPTION_KEY")
if CHAT_ENCRYPTION_KEY is None:
    raise ValueError("Encryption key is missing! Set CHAT_ENCRYPTION_KEY in .env")

CIPHER_SUITE = Fernet(CHAT_ENCRYPTION_KEY) # Global encryption object

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

AUTH_USER_MODEL = 'accounts.CustomUser'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-v(5%b%3mhspnyu&nn&qu2ox4f#(51w@8^sl-9@awbue0=sfd&3'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'channels',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.accounts',
    'apps.projects',
    'apps.customers',
    'apps.employes',
    'rest_framework',
    'rest_framework_nested',
    'apps.api',
    'apps.api.accounnts_api',
    'apps.api.project_api',
    'apps.api.employ_api',
    'apps.api.customer_api',
    'apps.api.payments_api',
    'apps.api.chat_api',
    'apps.api.complain_api',
    'corsheaders',
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'client_management_system.urls'
CORS_ORIGIN_ALLOW_ALL = True # Allow all origins to access the API(Not recommended for production)
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

# WSGI_APPLICATION = 'client_management_system.wsgi.application'
ASGI_APPLICATION = 'client_management_system.asgi.application'

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',  # JWT
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    # 'DEFAULT_PERMISSION_CLASSES': [
    #     'rest_framework.permissions.IsAuthenticated',
    # ]

}


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=1440),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=10),
}

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Khalti Configuration (Development)
KHALTI_SECRET_KEY = 'live_secret_key_68791341fdd94846a146f0457ff7b455'  # Test secret key
# FRONTEND_URL = 'https://abc123.ngrok.io'  #frontend URL
# FRONTEND_URL = 'http://localhost:3000'  #frontend URL
FRONTEND_URL = "http://127.0.0.1:8000"

# SECURE_SSL_REDIRECT = True
# SECURE_HSTS_SECONDS = 31536000  # Force HTTPS for 1 year
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True

# SECURE_SSL_REDIRECT = False
# SECURE_HSTS_SECONDS = 0  # Disable HTTP Strict Transport Security
# SECURE_HSTS_INCLUDE_SUBDOMAINS = False  # Disable for subdomains
# SECURE_HSTS_PRELOAD = False  # Disable preloading