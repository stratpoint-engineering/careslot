"""Local development: DEBUG on, SQLite unless DATABASE_URL is set, design states viewable."""

from .base import *  # noqa: F403
from .base import env, env_list

DEBUG = True
SECRET_KEY = env("DJANGO_SECRET_KEY", "dev-only-insecure-key-never-use-in-production")
ALLOWED_HOSTS = env_list("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1")
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
}
CARESLOT_DEMO_STATES = True
# Serve static files straight from static/ (no collectstatic needed outside production).
WHITENOISE_AUTOREFRESH = True
WHITENOISE_USE_FINDERS = True
