import os

import dj_database_url
import sentry_sdk
from decouple import Csv, config
from sentry_sdk.integrations.django import DjangoIntegration

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
API_DIR = os.path.dirname(PROJECT_DIR)
ROOT_DIR = os.path.dirname(API_DIR)

# Security Config
SECRET_KEY = config("DJANGO_SECRET_KEY")
DEBUG = config("DJANGO_DEBUG", default=False, cast=bool)
ALLOWED_HOSTS = config("DJANGO_ALLOWED_HOSTS", cast=Csv())

# SSL
SECURE_SSL_REDIRECT = config("DJANGO_SECURE_SSL_REDIRECT", cast=bool, default=False)
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# CORS
CORS_ORIGIN_ALLOW_ALL = False
CORS_ALLOW_METHODS = ("GET", "POST", "PUT", "PATCH", "OPTIONS")
CORS_ORIGIN_WHITELIST = config("DJANGO_CORS_ORIGIN_WHITELIST", default="", cast=Csv())
CORS_ORIGIN_REGEX_WHITELIST = [r"^https://[\w-]+--aecworks\.netlify\.app$"]

# CRSF
CSRF_TRUSTED_ORIGINS = config("DJANGO_CSRF_TRUSTED_ORIGINS", default="", cast=Csv())

# Cookies
SESSION_COOKIE_SECURE = config(
    "DJANGO_SESSION_COOKIE_SECURE", cast=bool, default=not DEBUG
)

# Social Auth
OAUTH_GITHUB_CLIENT_ID = config("OAUTH_GITHUB_CLIENT_ID")
OAUTH_GITHUB_CLIENT_SECRET = config("OAUTH_GITHUB_CLIENT_SECRET")
OAUTH_LINKEDIN_CLIENT_ID = config("OAUTH_LINKEDIN_CLIENT_ID")
OAUTH_LINKEDIN_CLIENT_SECRET = config("OAUTH_LINKEDIN_CLIENT_SECRET")

# Auth
AUTH_USER_MODEL = "users.User"

# Sites
SITE_ID = 1
INTERNAL_IPS = ["localhost", "127.0.0.1"]

# Email
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Application definition
INSTALLED_APPS = [
    # "whitenoise.runserver_nostatic",
    # Extensions
    "jet",
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",  # sitemaps
    "django.contrib.sitemaps",  # sitemaps
    # Extensions
    "rest_framework",
    "rest_framework.authtoken",
    "djoser",
    "corsheaders",
    "django_extensions",
    "debug_toolbar",
    "django_cleanup",
    "versatileimagefield",
    # Apps
    "api.users",
    "api.community",
    "api.images",
    "api.webhooks",
]

MIDDLEWARE = [
    "api.middlewares.EnsureCsrfCookie",
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
    "PAGE_SIZE": 10,
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.LimitOffsetPagination",
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
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

# Static
STATIC_ROOT = os.path.join(ROOT_DIR, "staticfiles")
STATIC_URL = "/static/"

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

use_s3 = config("DJANGO_S3_STORAGE", cast=bool)

if use_s3:
    DEFAULT_FILE_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"
    # AWS
    AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = config("DJANGO_S3_BUCKET_NAME")
    AWS_S3_CUSTOM_DOMAIN = config("DJANGO_S3_DOMAIN", default=None)  # prod only
    AWS_S3_REGION_NAME = "us-west-1"
    AWS_DEFAULT_ACL = "public-read"
    AWS_QUERYSTRING_AUTH = False  # Remove Query Auth from Image Url
    AWS_S3_OBJECT_PARAMETERS = {
        "CacheControl": "max-age=86400",
    }
else:
    DEFAULT_FILE_STORAGE = "django.core.files.storage.FileSystemStorage"
    MEDIA_ROOT = os.path.join(ROOT_DIR, "storage")
    MEDIA_URL = "/storage/"


# CACHE
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
    }
}
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"


# Sentry
if not DEBUG:
    sentry_sdk.init(
        dsn="https://3dedba3c033348c2ae0cdd9033ef2aa8@o179529.ingest.sentry.io/5414395",
        integrations=[DjangoIntegration()],
        traces_sample_rate=1.0,
        send_default_pii=True,
    )


explicit_log_level = config("DJANGO_LOG_LEVEL", default="INFO")
if explicit_log_level not in ["DEBUG", "INFO", "WARN", "ERROR", "CRITICAL", "FATAL"]:
    explicit_log_level = "DEBUG"
log_level = explicit_log_level or "DEBUG" if DEBUG else "INFO"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "loggers": {
        "": {"handlers": ["console"], "level": log_level, "propagate": True},
        "django": {"handlers": ["console"], "level": log_level, "propagate": False},
        "django.utils.autoreload": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "PIL": {"handlers": ["console"], "level": "INFO", "propagate": False},
    },
}
