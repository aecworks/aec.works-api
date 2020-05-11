import os
from decouple import config, Csv

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
API_DIR = os.path.dirname(PROJECT_DIR)
ROOT_DIR = os.path.dirname(API_DIR)

# Security Config
SECRET_KEY = config("DJANGO_SECRET_KEY")
DEBUG = config("DJANGO_DEBUG", default=False, cast=bool)
ALLOWED_HOSTS = config("DJANGO_ALLOWED_HOSTS", default="", cast=Csv())

# SSL
SECURE_SSL_REDIRECT = config("DJANGO_SECURE_SSL_REDIRECT", cast=bool, default=False)
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# CORS
CORS_ORIGIN_ALLOW_ALL = False
CORS_ALLOW_METHODS = ("GET", "OPTIONS")
CORS_ORIGIN_WHITELIST = config("DJANGO_CORS_ORIGIN_WHITELIST", default="", cast=Csv())
# CORS_ORIGIN_WHITELIST = ["http://localhost:8080/"]
# CORS_ORIGIN_REGEX_WHITELIST = [r"^https://aec.guide$"]
# SECURITY WARNING: define the correct hosts in production!

# Auth
AUTH_USER_MODEL = "users.User"


# Application definition

INSTALLED_APPS = [
    # Extensions
    "jet",
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Extensions
    "rest_framework",
    "corsheaders",
    "mptt",
    "django_extensions",
    # Apps
    "api.users",
    "api.community",
    # "api.search",
    # "api.people",
    # "api.blog",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # Cors
    "querycount.middleware.QueryCountMiddleware",
    # //
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "api.aecguide.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "api.aecguide.wsgi.application"


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DJANGO_DB_NAME"),
        "USER": config("DJANGO_DB_USER"),
        "PASSWORD": config("DJANGO_DB_PASSWORD"),
        "HOST": config("DJANGO_DB_HOST"),
        "PORT": "5432",
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# REST FRAMEWORK
REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": (
        "djangorestframework_camel_case.render.CamelCaseJSONRenderer",
        "djangorestframework_camel_case.render.CamelCaseBrowsableAPIRenderer",
        # Any other renders
    ),
    "DEFAULT_PARSER_CLASSES": (
        "djangorestframework_camel_case.parser.CamelCaseFormParser",
        "djangorestframework_camel_case.parser.CamelCaseMultiPartParser",
        "djangorestframework_camel_case.parser.CamelCaseJSONParser",
        # Any other parsers
    ),
    "PAGE_SIZE": 25,
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/
STATIC_ROOT = os.path.join(ROOT_DIR, "staticfiles")
STATIC_URL = "/static/"

# STATICFILES_DIRS = [os.path.join(PROJECT_DIR, "public")]
MEDIA_ROOT = os.path.join(ROOT_DIR, "media")
MEDIA_URL = "/media/"

SERVE_STATIC = config("SERVE_STATIC", default=False)
if SERVE_STATIC:
    STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"
    DEFAULT_FILE_STORAGE = "django.contrib.staticfiles.storage.FileSystemStorage"
else:
    STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
    DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

# Where To Store File Medie
# AWS_S3_CUSTOM_DOMAIN = 'cdn.mydomain.com'


EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
