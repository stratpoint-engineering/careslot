# CareSlot web image for AWS ECS Fargate (ADR-CARESLOT-E001-003).
# Day 1 runs the Celery worker and beat from this same image with a different command.
FROM python:3.13-slim AS base

COPY --from=ghcr.io/astral-sh/uv:0.13.6 /uv /bin/uv

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    PATH="/opt/venv/bin:$PATH" \
    DJANGO_SETTINGS_MODULE=config.settings.prod

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev --no-install-project

COPY . .

# collectstatic needs settings to import; these build-time values are not used at runtime.
RUN DJANGO_SECRET_KEY=build-only DJANGO_ALLOWED_HOSTS=build DATABASE_URL=postgres://build@localhost/build \
    CLINIC_TIME_ZONE=UTC python manage.py collectstatic --noinput

RUN useradd --system --uid 10001 careslot
USER careslot

EXPOSE 8000
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--access-logfile", "-"]
