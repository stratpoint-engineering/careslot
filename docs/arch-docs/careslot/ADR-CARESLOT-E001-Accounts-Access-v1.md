Epic: E001 — Accounts & Access
Covers: US-001, US-002, US-012, FR-AUTH-001, FR-AUTH-002, FR-AUTH-003, FR-AUTH-004, FR-AUTH-005, FR-ADMIN-001

Patient self-registration, sign-in for every user, lockout, idle sign-out, roles and staff accounts. This epic also
holds the platform decisions every other epic builds on: framework and hosting.

## ADR-CARESLOT-E001-001: Build CareSlot in Python 3.13 and Django 6.1, moving to Django's next LTS before go-live
### Status
Proposed
### Type
Decision
### Context
There are 2 developers, both strong in Python and Django, and about 10 weeks of development before 2027-10-01
(team-constraints). The PRD needs registration, sign-in, roles, admin screens and form-heavy booking pages
(FR-AUTH-*, FR-ADMIN-*, FR-BOOK-*).
### Options Considered
1. Django (Python): the team's strength. It includes auth, sessions, ORM, migrations, forms and admin.
2. A Node/TypeScript stack: no team experience.
3. A React SPA + separate API: nobody has run one in production (team-constraints), and it means two codebases.
### Decision
Python 3.13 and Django 6.1 (6.1.3 is the latest on PyPI, checked 2026-11-23). Exact versions are pinned at scaffold.
Upgrade to Django's next LTS release before go-live.
### Rationale
It's the fastest path to a working release with the people available. The built-in auth and sessions directly cover
FR-AUTH-001/002/004, and the admin helps FR-ADMIN-001/002.
### Consequences
One language across web and jobs. An LTS upgrade must be planned before launch (ARCH §9 D1).
### Affected Epics
E001 – E006
### Architecture Document Reference
ARCH-CARESLOT-v1 §4 "Backend language and framework"

## ADR-CARESLOT-E001-002: Use Django auth with django-axes lockout, 30-minute idle sessions and server-side role checks
### Status
Proposed
### Type
Decision
### Context
BR-016 – BR-018 and FR-AUTH-001 – 005 require email + password sign-in, lockout after 5 wrong passwords for
15 minutes, idle sign-out after 30 minutes, and access by role. The DPO requires that only the patient and clinic
staff see patient data (BR-014).
### Options Considered
1. Django auth + django-axes + Django sessions.
2. A hosted identity provider (e.g. Cognito): another service to learn, and a region question again (Q1).
3. A custom lockout implementation.
### Decision
Option 1. Email is the login field. django-axes locks per account after 5 failures for 15 minutes. Sessions are
database-backed with `SESSION_COOKIE_AGE = 1800` and `SESSION_SAVE_EVERY_REQUEST = True`. Roles: `patient`,
`front_desk`, `doctor`, `clinic_admin`. Every view and every service function checks role and ownership on the
server (team pattern). Hiding a button is never the check.
### Rationale
It's a maintained, well-known package that meets NFR-SEC-002 and NFR-SEC-003 exactly. Server-side checks make
AC-014 and AC-033/034 testable.
### Consequences
Lockout state is kept in PostgreSQL. A lockout can be cleared by a clinic admin through Django admin.
### Affected Epics
E001, E003, E004
### Architecture Document Reference
ARCH-CARESLOT-v1 §4 "Authentication and authorization", §8 NFR-SEC-002/003

## ADR-CARESLOT-E001-003: Run on AWS ECS Fargate in a single region, with web, worker and beat as separate services
### Status
Proposed. The region is pending Q1.
### Type
Prescribed (AWS account and managed PostgreSQL/Redis given by the client) + Decision (ECS Fargate)
### Context
The clinic group has an AWS account, and everything must run in the clinic's region (team-constraints; BR-013).
Nobody is on call at night, so the system must recover from a crashed process on its own. The availability target
is 99.5% monthly (NFR-002).
### Options Considered
1. ECS Fargate services behind an ALB: no servers to patch, and crashed tasks are replaced automatically.
2. EC2 instances with systemd: patching and recovery are on the team.
3. Elastic Beanstalk: less control over separate worker/beat processes.
### Decision
ECS Fargate: web (≥ 2 tasks across 2 AZs, gunicorn), Celery worker (1 task), Celery beat (exactly 1 task). Also
RDS PostgreSQL Multi-AZ, ElastiCache Redis, Secrets Manager and CloudWatch. Staging and production have the same
shape, and every resource is in one region.
### Rationale
Self-healing without anyone on call. Two web tasks and Multi-AZ RDS serve NFR-002.
### Consequences
**NFR-SEC-001 is not met until Q1 is answered.** No AWS region in the Philippines was found (web search,
2026-11-23, not conclusive). If the clinic's region is outside the Philippines, BR-013 needs a DPO-approved change
request.
### Affected Epics
E001 – E006
### Architecture Document Reference
ARCH-CARESLOT-v1 §4 "Hosting and runtime", §7, §9 Q1
