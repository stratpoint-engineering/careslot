# AGENTS.md — CareSlot

Rules for everyone who changes this repository: developers and AI coding agents (Claude Code, Cursor,
Copilot, …). Read this before writing code. When a rule here and a habit disagree, this file wins.

## What this is

Online booking for three outpatient clinics. Patients book, see and cancel online (phone and desktop);
the front desk books for callers and walk-ins and moves/cancels; doctors see their own day read-only;
a clinic admin manages staff accounts and working hours; every appointment gets an email reminder at
18:00 the day before. Live by 2027-10-01.

| Source of truth | Where |
|---|---|
| Business rules (BR-001 … BR-018) | docs/requirements/BRD.md |
| Stories, FR, NFR, AC | docs/requirements/PRD.md |
| Architecture, epics E001–E006, ADRs | docs/arch-docs/careslot/ |
| Screens DES-001 … DES-013 | docs/designs/careslot/ (+ design.json) |
| Design system for code | knowledge/design-system.md, static/css/tokens.css |
| Coding standards | knowledge/rules/coding-standards.md |

## Stack (decided — change only with an ADR)

Python 3.13 · Django 6.1 (move to the next Django LTS before go-live) · Django templates + htmx (no React,
no SPA — ADR-CARESLOT-E003-001) · PostgreSQL · Celery 5 + Redis · Amazon SES · django-axes · AWS ECS Fargate.
Dependencies are pinned exactly in pyproject.toml and locked in uv.lock. Add one with `uv add <pkg>==<exact>`.

## Layout

```
config/          settings (base/dev/test/prod), urls
core/            roles, rules (business numbers), auth guard, middleware, logging, health, seed_demo
accounts/        E001 Accounts & Access      — User, Patient, sign-in, register, staff accounts
scheduling/      E002 Scheduling Core        — Clinic, Doctor, WorkingHours, Appointment, booking services
patient_portal/  E003 Patient Self-Service   — booking steps, my appointments
staff_portal/    E004 Front Desk & Doctor    — day view, book for patient, move/cancel, doctor's day
notifications/   E005 Reminders              — Reminder outbox, reminder email
audit/           E006 Audit Log              — AuditLog (append-only)
templates/       base, components/, pages per app, 403/404/500
static/          css/tokens.css, css/components.css, fonts/, js/htmx.min.js, js/app.js
```

## Architecture rules (non-negotiable)

1. **Modular monolith.** An app calls another app's `services.py` functions, never its models or tables directly.
2. **One write path for appointments.** Every book, move and cancel — online and front desk — goes through
   `scheduling.services`. It enforces: slot free (DB unique constraint), max 2 future appointments
   (patient-row lock), reason required, 20-minute grid inside working hours, and writes the Reminder and
   AuditLog rows in the same transaction (ADR-CARESLOT-E002-001, E005-001, E006-001).
3. **Authorization is server-side.** Every view has `@role_required(...)`; services check ownership too.
   Hiding a button is never the check. A test fails if a new URL is neither public nor guarded.
4. **Every view or change of patient data writes an AuditLog row.** AuditLog is insert-only: never update or delete.
5. **Business numbers live in `core/rules.py`**, each with its BR/NFR id. Never hard-code 30, 2, 18:00, … elsewhere.
6. **Views are thin; templates read view-models only** (dataclasses in `<app>/viewmodels.py`), never ORM objects.
7. **Secrets come from the environment** (AWS Secrets Manager in AWS). Never in the repo, never in logs.
8. **Patient data stays in the clinic's region** (BR-013). No third-party services that receive patient data
   without an ADR.

## Frontend rules

- Use only the design system: Card (`.card`), Button (`components/button.html`), Field (`components/field.html`),
  Hint, Status (`.ok` / `.warn` / `.err`). Colours only through `var(--token)`. A new colour or component is a
  question for the designer, not a code change.
- Every screen shows its states: empty, loading ("Loading…" Hint), error (inline `.err`, next to its cause —
  **no toasts**), disabled (and busy "…ing" labels). Destructive actions confirm by a second click.
- Patient screens: one 420 px card, phones first. Staff screens: desktop.
- No inline `style=""` or inline `<script>` — the Content-Security-Policy blocks them. Put CSS in
  components.css, JS in static/js/.
- Accessibility (WCAG 2.1 AA, NFR-004): labels on every input, `aria-invalid` + `aria-describedby` on errors,
  visible focus, `role="alert"` for errors.
- htmx: send the CSRF header (base.html does it); return HTML fragments, not JSON.

## Backend standards

- Type hints everywhere; `mypy --strict` passes. Ruff lint + format pass.
- Logging: `logger = logging.getLogger(__name__)`; JSON to stdout with request id. Never `print`, never log
  patient names, emails, phones or reasons for visit.
- Errors: forms → inline field errors; pages → 403/404/500 templates; htmx → `.err` fragment. JSON only for `/healthz`.
- Database: migrations for every model change (`makemigrations --check` runs in CI and pre-commit);
  constraints in the database, not only in Python.
- Time: store UTC (`USE_TZ`); show clinic time (`CLINIC_TIME_ZONE`).

## Tests and quality gates

- Every story's acceptance criteria (AC-…) get tests; name the AC in the test docstring.
- Concurrency rules (double booking, 2-appointment limit) get a concurrent test against PostgreSQL.
- Before pushing: `uv run ruff check . && uv run ruff format --check . && uv run mypy . && uv run pytest`.
- CI also runs migrations on PostgreSQL, `check --deploy` with prod settings, and `pip-audit`.

## Git

- Branches: `feat/E00N-<short-name>`, `fix/…`, `docs/…`, `chore/…`. One dev task per PR where possible.
- Commits: Conventional Commits (`feat(booking): …`), enforced by the commitizen commit-msg hook.
  Install hooks once: `uv run pre-commit install --hook-type pre-commit --hook-type commit-msg`.
- PR description cites the task, stories and ACs it delivers.

## Day 0 → Day 1 hand-offs

- Mock auth (`core/auth.py` signed `mock-role` cookie) → Django auth + django-axes; keep `role_required`.
- Mock data (`<app>/mock.py`) → queries/services returning the same view-models; delete the mock module.
- `?state=` demo switch (`core/demo.py`) is dev/test only; real states come from real data.
- `config/settings/prod.py` silences `mail.E001`: remove it when SES is wired (E005).
- Open: ARCH §9 Q1 (AWS region vs BR-013), Q2 (clinic time zone), PRD open questions 1–8.
