Epic: E005 — Reminders
Covers: US-006, FR-NOTIF-001

An email reminder for every appointment at 18:00 (clinic time) on the day before, which must not be lost if a process
crashes or the email provider is briefly down.

## ADR-CARESLOT-E005-001: Send reminders from a PostgreSQL outbox, using a Celery job that runs every minute
### Status
Proposed
### Type
Decision
### Context
BR-008 / FR-NOTIF-001 require a reminder at 18:00 on the day before every appointment. Nobody is on call at night.
The system must recover on its own from a crashed process, and reminders must not be lost if the provider is
briefly down (team-constraints). Managed Redis is available.
### Options Considered
1. One Celery task scheduled at booking time for the exact due time (ETA): it's lost if Redis is flushed, and it's
   hard to move or cancel.
2. One beat job at exactly 18:00 that sends everything for tomorrow: if beat or the worker is down at 18:00, that
   day's reminders are missed.
3. Outbox: the booking service writes a `Reminder` row (due_at) in the same transaction as the appointment. It moves
   due_at on a move, and cancels the row on a cancel. Celery beat triggers a task **every minute** that claims
   reminders with `due_at ≤ now`, `sent_at IS NULL`, status pending (`FOR UPDATE SKIP LOCKED`), and sends them
   through SES. A failure increases `attempts`, and the reminder is retried with backoff until the appointment
   starts.
### Decision
Option 3, with Celery 5 and Redis (ElastiCache) as the broker. The outbox in PostgreSQL is the source of truth.
### Rationale
A crash or outage only delays sending, because the next run picks up everything still due. Nothing lives only in
Redis. `SKIP LOCKED` prevents duplicate sends if two workers run. Cancelled appointments never get a reminder
(AC-019), and front-desk bookings get one like online bookings (AC-020).
### Consequences
A CloudWatch alarm fires on reminders still unsent 1 hour after due_at. It is read in working hours. The answer to
ARCH §9 Q3 (late bookings) only changes how due_at is computed.
### Affected Epics
E002, E005
### Architecture Document Reference
ARCH-CARESLOT-v1 §4 "Background jobs", §5 Reminder, §7

## ADR-CARESLOT-E005-002: Send email through Amazon SES; the clinic's SMS provider isn't used in release 1
### Status
Proposed. The region is pending ARCH §9 Q1.
### Type
Decision
### Context
The PO chose email-only reminders (PRD NFR-005; PO, 2026-11-23). The clinic has an SMS provider account
(team-constraints), but SMS isn't in the PRD.
### Options Considered
1. Amazon SES in the clinic's AWS account and hosting region.
2. A third-party email service: another vendor contract and data-location review.
3. The clinic's SMS provider: not what the PO decided.
### Decision
Amazon SES, called from the Celery worker with IAM role credentials. The SMS provider isn't integrated in release 1.
### Rationale
It stays inside the clinic's AWS account, with no extra vendor and no stored secrets.
### Consequences
SES needs a verified sending domain and production access before launch. Whether SES runs in the region chosen for
Q1 was not checked.
### Affected Epics
E005
### Architecture Document Reference
ARCH-CARESLOT-v1 §4 "Email delivery", §6
