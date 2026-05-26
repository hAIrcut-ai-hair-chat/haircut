import os

from pathlib import Path
from datetime import timedelta

import dj_database_url
import cloudinary

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

MODE = os.getenv("MODE", "DEVELOPMENT")

SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "django-insecure"
)

DEBUG = os.getenv("DEBUG", "False") == "True"

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "channels",
    "corsheaders",
    "cloudinary",
    "cloudinary_storage",
    "django_extensions",
    "django_filters",
    "drf_spectacular",
    "rest_framework",
    "rest_framework_simplejwt",
    "core",
    "uploader",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",

    "corsheaders.middleware.CorsMiddleware",

    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",

    "django.contrib.auth.middleware.AuthenticationMiddleware",

    "django.contrib.messages.middleware.MessageMiddleware",

    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "app.urls"

WSGI_APPLICATION = "app.wsgi.application"

ASGI_APPLICATION = "app.asgi.application"

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
            ],
        },
    },
]

DATABASES = {
    "default": dj_database_url.config(
        default=os.getenv(
            "DATABASE_URL",
            "sqlite:///" + str(BASE_DIR / "db.sqlite3")
        ),
        conn_max_age=600,
    )
}

AUTH_USER_MODEL = "core.User"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME":
        "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {
        "NAME":
        "django.contrib.auth.password_validation.MinimumLengthValidator"
    },
    {
        "NAME":
        "django.contrib.auth.password_validation.CommonPasswordValidator"
    },
    {
        "NAME":
        "django.contrib.auth.password_validation.NumericPasswordValidator"
    },
]

LANGUAGE_CODE = "pt-br"

TIME_ZONE = "America/Sao_Paulo"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"

STATIC_ROOT = os.path.join(
    BASE_DIR,
    "staticfiles"
)

MEDIA_URL = "/media/"

MEDIA_ROOT = os.path.join(
    BASE_DIR,
    "media/"
)

FILE_UPLOAD_PERMISSIONS = 0o640

cloudinary.config(
    cloud_name=os.getenv(
        "CLOUDINARY_CLOUD_NAME"
    ),

    api_key=os.getenv(
        "CLOUDINARY_API_KEY"
    ),

    api_secret=os.getenv(
        "CLOUDINARY_API_SECRET"
    ),
)

DEFAULT_FILE_STORAGE = (
    "cloudinary_storage.storage.MediaCloudinaryStorage"
)

CORS_ALLOW_ALL_ORIGINS = True

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://localhost:8000",

    "https://haircut-frontend-ppnf.vercel.app",
]

REST_FRAMEWORK = {

    "DEFAULT_PAGINATION_CLASS":
    "app.pagination.CustomPagination",

    "DEFAULT_SCHEMA_CLASS":
    "drf_spectacular.openapi.AutoSchema",

    "PAGE_SIZE": 10,

    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
}

SIMPLE_JWT = {

    "ACCESS_TOKEN_LIFETIME":
    timedelta(hours=1),

    "REFRESH_TOKEN_LIFETIME":
    timedelta(days=7),

    "ROTATE_REFRESH_TOKENS":
    False,

    "BLACKLIST_AFTER_ROTATION":
    False,

    "UPDATE_LAST_LOGIN":
    False,

    "ALGORITHM":
    "HS256",

    "SIGNING_KEY":
    SECRET_KEY,

    "AUTH_HEADER_TYPES":
    ("Bearer",),
}

CHANNEL_LAYERS = {
    "default": {
        "BACKEND":
        "channels_redis.core.RedisChannelLayer",

        "CONFIG": {
            "hosts": [
                ("127.0.0.1", 6379)
            ],
        },
    },
}

SPECTACULAR_SETTINGS = {
    "TITLE": "API",

    "DESCRIPTION":
    "Project API",

    "VERSION": "1.0.0",
}

CELERY_BROKER_URL = os.getenv(
    "CELERY_BROKER_URL"
)

CELERY_RESULT_BACKEND = os.getenv(
    "CELERY_RESULT_BACKEND"
)

CELERY_ACCEPT_CONTENT = ["json"]

CELERY_TASK_SERIALIZER = "json"

CELERY_RESULT_SERIALIZER = "json"

CELERY_TIMEZONE = "America/Sao_Paulo"

DEFAULT_AUTO_FIELD = (
    "django.db.models.BigAutoField"
)

APPEND_SLASH = False

FAL_API_KEY = os.getenv("FAL_API_KEY")

PASSAGE_APP_ID = os.getenv(
    "PASSAGE_APP_ID",
    "app_id"
)

PASSAGE_API_KEY = os.getenv(
    "PASSAGE_API_KEY",
    "api_key"
)

HF_TOKEN = os.getenv("HF_TOKEN")

HF_AI_MODEL = os.getenv("HF_AI_MODEL")

HF_BASE_URL = os.getenv("HF_BASE_URL")

DJANGO_URL = os.getenv("BACKEND_URL")

DOCUMENT_CONFIG = {
    "SUPPORTED_FORMATS": [
        "pdf",
        "txt",
        "csv",
        "md",
        "html",
    ],

    "MAX_FILE_SIZE":
    10 * 1024 * 1024,

    "UPLOAD_DIR":
    os.path.join(
        BASE_DIR,
        "media/documents"
    ),
}

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "martinsbarroskaua85@gmail.com"
EMAIL_HOST_PASSWORD = "yjmc vcjo zlhn lela "

print(f"MODE = {MODE}")

print(f"DEBUG = {DEBUG}")

print(
    f'DATABASE = {DATABASES["default"]["ENGINE"]}'
)

print(
    f'CLOUDINARY = {os.getenv("CLOUDINARY_CLOUD_NAME")}'
)