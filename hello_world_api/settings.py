import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "fake-django-secret-key"  # noqa: S105
DEBUG = bool(os.getenv("DJANGO_DEBUG", "False"))
ALLOWED_HOSTS = [os.getenv("ALLOWED_HOST", "localhost")]

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "corsheaders",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
]

CORS_ALLOWED_ORIGINS = [
    os.getenv("CORS_ALLOWED_ORIGIN", "http://localhost:3000"),
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "/tmp/db.sqlite3",  # noqa: S108
    },
}

ROOT_URLCONF = "hello_world_api.urls"

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = False
USE_TZ = True
