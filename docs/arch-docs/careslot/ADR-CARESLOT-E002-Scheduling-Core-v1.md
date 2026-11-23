Epic: E002 — Scheduling Core
Covers: US-013, FR-ADMIN-002, FR-BOOK-003, FR-BOOK-004, FR-BOOK-005, FR-BOOK-006

Clinics, doctors, weekly working hours, slot generation, and the booking service: the single write path for book,
move and cancel that the patient portal (E003) and staff portal (E004) both call.

## ADR-CARESLOT-E002-001: Enforce one-appointment-per-slot with a database constraint, and the 2-appointment limit under a patient-row lock
### Status
Proposed
### Type
Decision
### Context
Double bookings happen about twice a week today, and "it has to be impossible, not just rare" (BRD; BR-004). A
patient may hold at most 2 future appointments on every channel, with no override (BR-003). Online and front-desk
bookings can hit the same slot at the same moment (AC-010, AC-025).
### Options Considered
1. Check in application code only ("is the slot free?" then insert): two requests can both pass.
2. Store pre-generated slot rows and lock them: many rows to maintain whenever working hours change.
3. Generate slots from working hours. Add a partial unique index on `Appointment(doctor_id, start) WHERE
   status = 'booked'`, and count future appointments inside a transaction holding `SELECT … FOR UPDATE` on the
   Patient row.
### Decision
Option 3, inside one booking service (`scheduling.services`) used by every channel. The service also checks the
20-minute grid and working hours (FR-BOOK-003) and the required reason (FR-BOOK-004). A unique-violation is turned
into a "slot just taken" message.
### Rationale
The database guarantees BR-004 even under concurrent writes from two channels. The patient-row lock serialises
bookings for the same patient, so two simultaneous requests can't both become appointment #2. Generating slots from
WorkingHours means an hours change (FR-ADMIN-002) takes effect at once (AC-039).
### Consequences
All writes must go through the booking service. A test fires concurrent bookings for the same slot and the same
patient. What happens to existing appointments when hours shrink is open (ARCH §9 Q5).
### Affected Epics
E002, E003, E004, E005, E006
### Architecture Document Reference
ARCH-CARESLOT-v1 §5 Data Model, §6 Booking service
