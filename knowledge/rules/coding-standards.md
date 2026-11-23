# Coding standards — CareSlot (Python / Django)

Derived from ARCH-CARESLOT-v1 and its ADRs. AGENTS.md has the short version; this file explains the patterns.

## Layers

| Layer | Lives in | Does | Never |
|---|---|---|---|
| View | `<app>/views.py` | parse request, call one service, pick template, build view-models | query other apps' models, enforce business rules |
| Service | `<app>/services.py` | business rules, transactions, audit + reminder writes | render HTML, read `request` |
| Model | `<app>/models.py` | fields, DB constraints and indexes | business workflows |
| View-model | `<app>/viewmodels.py` | frozen dataclasses the template reads | hold ORM objects |
| Template | `templates/<app>/` | layout from components, every design state | logic beyond `if`/`for` |

## Booking service contract (Day 1, E002)

```python
# scheduling/services.py
def book(*, actor: User, patient: Patient, doctor: Doctor, start: datetime, reason: str, channel: Channel) -> Appointment: ...
def move(*, actor: User, appointment: Appointment, new_start: datetime) -> Appointment: ...
def cancel(*, actor: User, appointment: Appointment) -> Appointment: ...
```

Each runs in `transaction.atomic()`, locks the patient row (`select_for_update`) before counting future
appointments, relies on the `one_booked_appointment_per_slot` constraint for the slot, and raises a typed
error (`SlotTaken`, `LimitReached`, `TooLateToCancel`, `OutsideWindow`) that the view turns into the frame's
inline error text. It writes/updates the Reminder and an AuditLog row in the same transaction.

## Errors

- Expected business outcomes → typed exceptions from services → inline `.err` text from the design frame.
- Unexpected → let it raise; Django returns `500.html`, the log line has the request id.
- Never show stack traces or internal ids to users.

## Logging

`logging.getLogger(__name__)`, JSON to stdout, `request_id` on every line (core/logging.py). Log events and ids
(`appointment_id=…`), never patient names, emails, phones or reasons for visit.

## htmx

- Partial updates only where the design says (slot list, doctor list, day cards). Views check
  `request.htmx` and return a fragment template `templates/<app>/_<fragment>.html`.
- Failures show the `.err` pattern (static/js/app.js). No `hx-on` / inline script (CSP).

## Tests

pytest + pytest-django. One test module per view/service; AC id in each docstring. Concurrency tests run on
PostgreSQL in CI. `core/tests/test_shell.py` keeps every URL guarded and every design state rendering.
