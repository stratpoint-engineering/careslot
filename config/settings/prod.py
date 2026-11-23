"""Staging and production on AWS ECS behind an ALB (ADR-CARESLOT-E001-003).

Required env: DJANGO_SECRET_KEY, DJANGO_ALLOWED_HOSTS, DJANGO_CSRF_TRUSTED_ORIGINS, DATABASE_URL,
CLINIC_TIME_ZONE. Secrets come from AWS Secrets Manager via the task definition, never the repo.
"""

import dj_database_url

from .base import *  # noqa: F403
from .base import env, env_list

DEBUG = False
SECRET_KEY = env("DJANGO_SECRET_KEY")
ALLOWED_HOSTS = env_list("DJANGO_ALLOWED_HOSTS")
CSRF_TRUSTED_ORIGINS = env_list("DJANGO_CSRF_TRUSTED_ORIGINS")
TIME_ZONE = env("CLINIC_TIME_ZONE")

# PostgreSQL with psycopg 3's connection pool (Django's native pool support).
# With a pool, persistent connections (CONN_MAX_AGE) must stay off.
DATABASES = {
    "default": dj_database_url.parse(
        env("DATABASE_URL"), conn_max_age=0, conn_health_checks=False, ssl_require=True
    )
}
DATABASES["default"]["OPTIONS"] = {
    **DATABASES["default"].get("OPTIONS", {}),
    "pool": {"min_size": 2, "max_size": 10, "timeout": 10},
}

# HTTPS everywhere; the ALB terminates TLS and sets X-Forwarded-Proto.
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_SSL_REDIRECT = True
SECURE_REDIRECT_EXEMPT = [r"^healthz$"]
SECURE_HSTS_SECONDS = 31_536_000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Email: Day 0 has no real backend yet. Day 1 (epic E005) sets MAILERS["default"] to Amazon SES
# (ADR-CARESLOT-E005-002) and MUST delete this silence, so `check --deploy` guards it again.
SILENCED_SYSTEM_CHECKS = ["mail.E001"]
