# CareSlot

Online appointment booking for three outpatient clinics: patients book, see and cancel online;
the front desk runs every doctor's day; doctors see their own list; email reminders the evening before.

- Requirements: [BRD](docs/requirements/BRD.md) · [PRD](docs/requirements/PRD.md)
- Architecture: [ARCH-CARESLOT-v1](docs/arch-docs/careslot/ARCH-CARESLOT-v1.md) + one ADR file per epic (E001–E006)
- Designs: [docs/designs/careslot](docs/designs/careslot) (open any `Frame - *.dc.html` in a browser)
- Rules for people and AI agents: [AGENTS.md](AGENTS.md)

## Stack

Python 3.13 · Django 6.1 · Django templates + htmx · PostgreSQL (SQLite locally) · deployed on AWS ECS Fargate.
Day 1 adds Celery + Redis (reminder outbox), Amazon SES and django-axes.

## Run it locally (no services or credentials needed)

Prerequisite: [uv](https://docs.astral.sh/uv/). uv installs Python 3.13 if you don't have it.

```bash
uv sync                                         # install exact locked versions
uv run python manage.py migrate                 # SQLite: db.sqlite3
uv run python manage.py seed_demo               # optional demo data (idempotent)
uv run python manage.py runserver               # http://127.0.0.1:8000
uv run pre-commit install --hook-type pre-commit --hook-type commit-msg   # once per clone
```

**Sign in (Day 0 mock):** any email and password; pick a role on the sign-in page.

| Role | Lands on | Screens |
|---|---|---|
| Patient | /me/appointments | /book → /book/time → /book/confirm, /me/appointments |
| Front desk | /desk/day | /desk/day, /desk/book, /desk/appointments/1 |
| Doctor | /doctor/day | /doctor/day |
| Clinic admin | /manage/staff | /manage/staff, /manage/hours |

**Design states:** in development add `?state=…` to see a screen's states with mock data, e.g.
`/desk/day?state=empty`, `/book/confirm?state=limit`. The states per screen are listed in each template's first comment.

Day 0 is the shell only: pages render mock data, forms don't save (POST answers 405 until Day 1).

### Against PostgreSQL

```bash
docker compose up -d postgres
DATABASE_URL=postgres://careslot:careslot@localhost:5432/careslot uv run python manage.py migrate
```

## Checks (the same ones CI runs)

```bash
uv run ruff check . && uv run ruff format --check .
uv run mypy .
uv run python manage.py makemigrations --check --dry-run
uv run pytest
uv run pip-audit
```

## Configuration

Every environment-specific value is an environment variable: see [.env.example](.env.example).
Settings: `config.settings.dev` (default for `manage.py`), `config.settings.test` (pytest), `config.settings.prod`
(staging and production; `wsgi.py` default). Business numbers (30 days, 2 appointments, 2 hours, 18:00 …)
are constants in `core/rules.py`, each citing its business rule.

## Open questions that affect the code

- ARCH §9 Q1 — AWS region vs. BR-013 (data stored only in the Philippines). Blocks deployment, not development.
- ARCH §9 Q2 — clinic time zone (`CLINIC_TIME_ZONE`).
