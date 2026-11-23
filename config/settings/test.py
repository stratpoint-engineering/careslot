"""Test settings: in-memory SQLite (CI also runs migrations on PostgreSQL), fast hashing."""

from .base import *  # noqa: F403

DEBUG = False
SECRET_KEY = "test-only-key"  # noqa: S105
ALLOWED_HOSTS = ["testserver", "localhost"]
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"}}
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]
STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
}
CARESLOT_DEMO_STATES = True
# Serve static files straight from static/ (no collectstatic needed outside production).
WHITENOISE_AUTOREFRESH = True
WHITENOISE_USE_FINDERS = True
