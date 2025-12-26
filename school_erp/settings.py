from pathlib import Path
import sys
from decouple import config
import os
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
SECRET_KEY = "demo"
DEBUG = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
    '.onrender.com'
]

# AUTH_USER_MODEL = "core.User"

INSTALLED_APPS = [
    # "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework.authtoken",
    
    'core',
    
]
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'whitenoise.middleware.WhiteNoiseMiddleware',
    "school_erp.middleware.CASJWTAuthenticationMiddleware",
]

# CAS Integration Settings
CAS_VERIFY_ENDPOINT = "http://127.0.0.1:8000/api/tokens/verify/"  # your CAS verify endpoint
CAS_TIMEOUT = 5  # seconds
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

ROOT_URLCONF = "school_erp.urls"
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]
WSGI_APPLICATION = "school_erp.wsgi.application"
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT', default='5432'),
    }
}
AUTH_PASSWORD_VALIDATORS = []
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [BASE_DIR / "static"]
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    )
}
CAS_SERVER_URL = "http://127.0.0.1:8000"  # Your central auth system
CAS_VERIFY_ENDPOINT = f"{CAS_SERVER_URL}/api/tokens/verify/"
CAS_LOGIN_URL = f"{CAS_SERVER_URL}/api/auth/login/"
