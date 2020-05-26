import os
from datetime import timedelta
from decouple import config, Csv
import dj_database_url

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
CORS_ALLOW_METHODS = ("GET", "POST", "OPTIONS")
CORS_ORIGIN_WHITELIST = config("DJANGO_CORS_ORIGIN_WHITELIST", cast=Csv())
CORS_ORIGIN_REGEX_WHITELIST = [r"^https://[\w-]+--aecworks\.netlify\.app$"]

# Social Auth
GITHUB_CLIENT_ID = config("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = config("GITHUB_CLIENT_SECRET")

# JWT Config
SIMPLE_JWT = {
    "AUTH_HEADER_TYPES": ("JWT",),
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=5),
}
# Auth
AUTH_USER_MODEL = "users.User"

# Sites
SITE_ID = 1
INTERNAL_IPS = ["localhost"]

# Email
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

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
    # "django.contrib.sites",
    # Extensions
    "rest_framework",
    "rest_framework.authtoken",
    "djoser",
    "corsheaders",
    "mptt",
    "django_extensions",
    "debug_toolbar",
    # Apps
    "api.users",
    "api.community",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    # // Start Default
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # // End Default
    "querycount.middleware.QueryCountMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

ROOT_URLCONF = "api.aecworks.urls"

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

WSGI_APPLICATION = "api.aecworks.wsgi.application"

DATABASES = {"default": dj_database_url.parse(config("DATABASE_URL"), conn_max_age=600)}


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

# Rest Framework Settings

REST_FRAMEWORK = {
    "PAGE_SIZE": 25,
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_RENDERER_CLASSES": (
        "djangorestframework_camel_case.render.CamelCaseJSONRenderer",
        "djangorestframework_camel_case.render.CamelCaseBrowsableAPIRenderer",
    ),
    "DEFAULT_PARSER_CLASSES": (
        "djangorestframework_camel_case.parser.CamelCaseFormParser",
        "djangorestframework_camel_case.parser.CamelCaseMultiPartParser",
        "djangorestframework_camel_case.parser.CamelCaseJSONParser",
    ),
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_ROOT = os.path.join(ROOT_DIR, "staticfiles")
STATIC_URL = "/static/"

STATICFILES_DIRS = [os.path.join(ROOT_DIR, "static")]
MEDIA_ROOT = os.path.join(ROOT_DIR, "media")
MEDIA_URL = "/media/"

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# DEFAULT_FILE_STORAGE = "django.contrib.staticfiles.storage.FileSystemStorage"
DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
# TODO S3 for Media
# STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
# DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

#
AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")
AWS_S3_REGION_NAME = "us-west-1"
AWS_STORAGE_BUCKET_NAME = "aecworks-prod"
AWS_DEFAULT_ACL = "public-read"
