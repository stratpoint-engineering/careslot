Epic: E004 — Front Desk & Doctor Views
Covers: US-007, US-008, US-009, US-010, US-011, FR-DESK-001, FR-DESK-002, FR-DESK-003, FR-DESK-004, FR-DOC-001

Desktop staff screens: the front-desk day view of every doctor (with an empty-day message); finding or creating a
patient record and booking for callers and walk-ins; moving and cancelling, including in the last 2 hours; and the
doctor's read-only list for today.

This epic has no decision of its own. It follows:
- ADR-CARESLOT-E002-001: every book, move and cancel goes through the booking service, so the slot and
  2-appointment rules hold for staff too (AC-025, AC-026, AC-028).
- ADR-CARESLOT-E003-001: Django templates + htmx (day grid updates).
- ADR-CARESLOT-E001-002: server-side role checks. Front desk sees all doctors, a doctor sees only their own day and
  can't change it (AC-033, AC-034).
- ADR-CARESLOT-E006-001: every view of a day list or patient record is logged.

Open items affecting this epic: ARCH §9 Q4 (linking records), Q5 (30-day limit for staff), Q6 (email on staff move or
cancel).
