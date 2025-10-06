import os
from pathlib import Path
from socket import gethostbyname
from socket import gethostname

BASE_DIR = Path(__file__).resolve().parent.parent


# Allow ALB to send healthchecks
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "localhost").split(",")
ALLOWED_HOSTS.append(gethostbyname(gethostname()))

CORS_ALLOWED_ORIGINS = os.environ.get(
    "CORS_ALLOWED_ORIGINS",
    "http://localhost:3000",
).split(",")

SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "fake-django-key")
DEBUG = bool(os.getenv("DJANGO_DEV_SERVER", "False"))

INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "corsheaders",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
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
