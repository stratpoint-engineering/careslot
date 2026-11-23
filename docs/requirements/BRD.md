# BRD — CareSlot

<!-- Business Requirements Document. Written with /brd; edit freely. The headings below are the
     ones the requirements guide checks — keep them, add your own under them.
     IDs: BR-001, BR-002 … never renumbered; a changed rule keeps its ID. -->

| Field | Value |
|---|---|
| Version | 1.0 |
| Date | 2026-11-23 |
| Owner | Product owner |
| Status | Draft |
| Sources | `sources/kickoff-notes.md` (kickoff workshop); `sources/no-show-report.md` (operations report, clinic manager); `sources/front-desk-interview.md` (interview, front-desk lead); answers from the product owner, 2026-11-23 |

## 1. Purpose

This document sets out the business problem, goals, scope and business rules for CareSlot, the online booking system
for the client's three outpatient clinics. The product owner, clinic management, the data protection officer and the
delivery team use it to agree what the first release must achieve and which rules it must obey. The PRD (`/prd`)
turns these rules into user stories and requirements.

## 2. Problem

Booking at the three outpatient clinics is **phone only**. Each doctor has one shared schedule, kept in a
spreadsheet that is printed every morning (kickoff; front-desk interview).

- **No-shows:** 18% of booked appointments last quarter were no-shows. Doctors sit idle while other patients can't
  get a slot. The clinic manager reports that most no-shows say afterwards that they forgot. Some patients book 4–5
  slots "just in case" and then don't come (no-show report; kickoff).
- **Phone load:** about 140 booking calls a day, with an average wait of 6 minutes at peak. Patients hang up
  (no-show report; kickoff).
- **Double bookings:** about 2 a week. Two front-desk staff can take the same slot at the same time, and nobody
  notices until both patients arrive. "It has to be impossible, not just rare" (front-desk lead; no-show report).

## 3. Business Goals

| # | Goal | Metric (section 7) |
|---|---|---|
| G1 | Reduce no-shows so that doctors' time is used | No-show rate |
| G2 | Move booking from the phone to online self-service | Share of bookings made online |
| G3 | Reduce the front desk's phone load | Booking calls per day |
| G4 | Make double bookings impossible | Double bookings |

## 4. Stakeholders

| Stakeholder | Interest | Decides on |
|---|---|---|
| Clinic manager (Dr. Lina Ocampo) | Fewer no-shows, fair access to slots, online booking | Booking, cancellation and reminder rules; success-metric targets (confirmed) |
| Front-desk lead (Joy) | Fewer calls, no double bookings, one view of every doctor's day | Front-desk working rules (e.g. walk-ins) |
| Doctors (represented by Dr. Ana Reyes) | See their own day each morning | — (read-only users) |
| Data protection officer (Mark) | Patient-data residency, access control, access log, sign-in security | Data-protection and security rules |
| Patients | Book, see and cancel their own appointments, mostly on their phones | — |
| Product owner | Owns this BRD and the product backlog | BRD content and release scope |
| Delivery team (2 developers, 1 designer) | Clear, testable rules and a fixed deadline | — |

## 5. Scope

**In scope**
- Patients book online at any time of day, up to 30 days ahead, in 20-minute slots inside each doctor's working hours.
- Patients see their own upcoming appointments and cancel online (outside the last 2 hours).
- Front desk: one view per day of every doctor's appointments; book (phone callers and walk-ins), move and cancel.
- Doctors: their own day's list, read-only.
- Email reminder before every appointment.
- Sign-in with email and password, account lockout, idle sign-out, and a log of access to patient data.

**Out of scope**
- Payments and insurance — later release (kickoff).
- Video consultations — no plans (kickoff).
- Link to the hospital's medical records — release 2 (kickoff).

## 6. Business Rules

| ID | Rule | Source |
|---|---|---|
| BR-001 | Patients can book an appointment online at any time of day, every day. | Kickoff (clinic manager) |
| BR-002 | A patient can book online only slots that start within the next 30 days. | Kickoff (clinic manager) |
| BR-003 | A patient can hold at most 2 future appointments. The limit applies to every booking, including front-desk bookings, and staff cannot override it. | Kickoff (agreed by all); product owner, 2026-11-23 |
| BR-004 | A slot holds at most one appointment. A booking for a slot that is already taken is refused, whether it comes from a patient online or from the front desk. | Kickoff (front-desk lead); front-desk interview |
| BR-005 | Slots are 20 minutes long and lie inside the doctor's weekly working hours. | Kickoff |
| BR-006 | A patient can cancel their own appointment online up to 2 hours before it starts. Within the last 2 hours, only the front desk can cancel it. | Kickoff (clinic manager); front-desk interview |
| BR-007 | A patient can book a free slot online up to the slot's start time. | Product owner, 2026-11-23 |
| BR-008 | Every patient receives an email reminder for every appointment at 18:00 on the day before the appointment. | Kickoff (clinic manager); product owner, 2026-11-23 |
| BR-009 | A patient can see only their own appointments. | Kickoff; front-desk interview |
| BR-010 | Front-desk staff can book, move and cancel appointments for any doctor and any patient. | Kickoff; front-desk interview |
| BR-011 | A walk-in patient is booked into a slot by the front desk, and that slot is then no longer available online. | Kickoff (open item); product owner, 2026-11-23 |
| BR-012 | A doctor can see their own appointments for the day (time, patient name, reason for the visit) and cannot change them. | Kickoff (Dr. Reyes); front-desk interview |
| BR-013 | Patient data is stored only in the Philippines. | Kickoff (DPO); product owner, 2026-11-23 |
| BR-014 | Only the patient and clinic staff can see a patient's data. | Kickoff (DPO) |
| BR-015 | Every access to patient data is logged with who, which patient and when, and the log is kept for 5 years. | Kickoff (DPO); product owner, 2026-11-23 |
| BR-016 | Every user signs in with an email address and a password before seeing any patient data. | Kickoff (DPO) |
| BR-017 | After 5 wrong passwords, the account is locked for 15 minutes. | Kickoff (DPO); product owner, 2026-11-23 |
| BR-018 | A user who is idle for 30 minutes is signed out. | Kickoff (DPO) |

## 7. Success Metrics

Targets were confirmed by the clinic manager (product owner, 2026-11-23). They are measured 3 months after launch,
and launch is due by 2027-10-01.

| Metric | Today | Target | Measured by | Serves |
|---|---|---|---|---|
| No-show rate (G1) | 18% of booked appointments (last quarter) | ≤ 8%, 3 months after launch | Monthly no-show report | BR-008, BR-003, BR-006 |
| Share of bookings made online (G2) | 0% (phone only) | ≥ 60%, 3 months after launch | Booking channel in the schedule | BR-001, BR-002, BR-007 |
| Booking calls per day (G3) | about 140 | ≤ 60, 3 months after launch | Phone system report | BR-001, BR-006 |
| Double bookings (G4) | about 2 per week | 0, 3 months after launch | Front-desk incident log | BR-004, BR-011 |
| Average wait on the phone at peak (G3, tracked only) | 6 minutes | No target; expected to follow from fewer calls | Phone system report | BR-001 |

## 8. Assumptions

- Most no-shows happen because patients forget, so a reminder will prevent a large share of them ("a reminder would
  fix half of it", clinic manager). This is the clinic manager's view and has not been measured.
- Most patients will book from their phones (front-desk interview).
- Double bookings today come from two people editing the same schedule at once (kickoff; front-desk interview).
- Doctors' working hours are fixed up to 30 days ahead (kickoff: beyond that they "aren't fixed yet").

## 9. Constraints

- **Deadline:** live by **2027-10-01**, before flu season (kickoff; year confirmed by the product owner, 2026-11-23).
- **Team:** 2 developers and 1 designer (kickoff).
- **Data residency and privacy:** patient data stays in the Philippines, with access restricted and logged (BR-013 – BR-015).
- **Operations:** 3 outpatient clinics, with one shared schedule per doctor (kickoff).

## 10. Open Questions

| # | Question | Owner | Due |
|---|---|---|---|
| 1 | An appointment booked after 18:00 on the day before, or on the same day, misses the BR-008 reminder time. Does it get a reminder, and when? | Clinic manager | — |
| 2 | The front-desk lead worries that patients give wrong contact details, so reminders won't reach them. Should the patient's email address be verified at sign-up? | Front-desk lead | — |
