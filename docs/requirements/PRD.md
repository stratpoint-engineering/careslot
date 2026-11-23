# PRD — CareSlot

<!-- Product Requirements Document. Written with /prd from the BRD; edit freely. The headings below
     are the ones the requirements guide checks. Every user story and functional requirement cites
     the BR- rule it serves. IDs are never renumbered; a changed requirement keeps its ID. -->

| Field | Value |
|---|---|
| Version | 1.0 |
| Date | 2026-11-23 |
| Owner | Product owner |
| BRD | [BRD.md](BRD.md), v1.0 (BR-001 – BR-018) |
| Status | Draft |

Sources: the BRD v1.0 and its sources; answers from the product owner, 2026-11-23 (devices, patient accounts, clinic
admin, booking path, reason for visit, moving appointments, speed and availability, language, browsers and
accessibility, release scope).

## 1. Overview

CareSlot release 1 lets patients of the three outpatient clinics register, book, see and cancel appointments online.
It gives the front desk one view of every doctor's day, where they book (phone and walk-in), move and cancel. Doctors
get a read-only list of their day, and a clinic admin manages staff accounts and doctors' working hours. Every
patient gets an email reminder the evening before each appointment. Booking enforces the rules that matter most to
the clinics: one appointment per slot and at most 2 future appointments per patient. Patient data stays in the
Philippines, and every access to it is logged.

This release serves all four BRD goals: fewer no-shows (G1), booking moved online (G2), fewer booking calls (G3) and
no double bookings (G4). It must be live by 2027-10-01.

## 2. Personas

| Persona | Who | Goal | Device |
|---|---|---|---|
| Patient | A patient of one of the three clinics | Book, see and cancel their own appointments without calling | Phone and desktop (PO, 2026-11-23) |
| Front-desk staff | Front-desk team, led by Joy | See every doctor's day; book for callers and walk-ins, move, cancel; no double bookings | Desktop (PO, 2026-11-23) |
| Doctor | A clinic doctor; each doctor works at one clinic only | See their own day each morning | Desktop (PO, 2026-11-23) |
| Clinic admin | Clinic staff with the admin role | Manage staff accounts and doctors' weekly working hours | Not stated (Open Question 8) |
| Data protection officer | DPO (Mark) | Know who accessed which patient's data, and when | No screen in release 1 (Open Question 7) |

## 3. User Stories

### US-001 — Register as a patient
As a patient, I want to create an account with my email and a password, so that I can book online. *(serves BR-016)*

Acceptance criteria:
- AC-001 A patient can register with name, email address and password, and is then able to sign in.
- AC-002 Registration with an email address that already belongs to an account is refused with a message.

### US-002 — Sign in
As any user, I want to sign in with my email and password, so that only I can see my data. *(serves BR-016, BR-017, BR-018)*

Acceptance criteria:
- AC-003 Without signing in, no page shows patient data. Opening such a page leads to the sign-in page.
- AC-004 After 5 wrong passwords for an account, sign-in to that account is refused for 15 minutes, even with the
  correct password. After 15 minutes, the correct password signs in.
- AC-005 A signed-in user who does nothing for 30 minutes is signed out. Their next action leads to the sign-in page.

### US-003 — Book an appointment online
As a patient, I want to choose a clinic, a doctor, a date and a free slot, and say what the visit is for, so that I
get an appointment without calling. *(serves BR-001, BR-002, BR-003, BR-004, BR-005, BR-007)*

Acceptance criteria:
- AC-006 The patient chooses in this order: clinic → doctor (only doctors of that clinic) → date → free slot.
- AC-007 Only free 20-minute slots are offered. They lie inside the doctor's weekly working hours, start within the
  next 30 days, and have not started yet.
- AC-008 A slot that has not started yet can be booked, including one that starts in the next minutes.
- AC-009 The booking is refused when the reason for visit is empty.
- AC-010 When two people try to book the same slot, exactly one booking succeeds. The other is refused with a
  message, and the slot is no longer offered.
- AC-011 A patient who already holds 2 future appointments cannot book a third. They are told why.
- AC-012 Booking works at any hour of any day.

### US-004 — See my upcoming appointments
As a patient, I want to see my upcoming appointments, so that I know when and where to go. *(serves BR-009)*

Acceptance criteria:
- AC-013 The list shows each of the patient's future appointments with date, time, clinic and doctor.
- AC-014 A patient never sees another patient's appointments, whether in the list, a slot view or by changing an
  address in the browser.

### US-005 — Cancel my appointment online
As a patient, I want to cancel an appointment myself, so that the slot can go to someone else. *(serves BR-006)*

Acceptance criteria:
- AC-015 A patient can cancel their own appointment up to 2 hours before it starts. The slot then becomes free for
  booking.
- AC-016 Within the last 2 hours before the start, the patient cannot cancel online and is told to call the front
  desk.
- AC-017 A cancelled appointment no longer counts toward the patient's limit of 2 future appointments.

### US-006 — Get an email reminder
As a patient, I want an email reminder before every appointment, so that I don't forget it. *(serves BR-008)*

Acceptance criteria:
- AC-018 At 18:00 (clinic local time) on the day before an appointment, its patient is sent one reminder email with
  the date, time, clinic and doctor.
- AC-019 No reminder is sent for an appointment that was cancelled before 18:00 on the day before.
- AC-020 A reminder is also sent for appointments booked by the front desk, when the patient record has an email
  address.

### US-007 — See every doctor's day
As front-desk staff, I want one screen per day with every doctor's appointments, so that I can answer callers and
walk-ins quickly. *(serves BR-010)*

Acceptance criteria:
- AC-021 For a chosen date, the screen shows every doctor's slots, with each appointment's time, patient name and
  reason for visit, and which slots are free.
- AC-022 A day with no appointments shows a message saying so, not an empty grid.

### US-008 — Book for a caller or walk-in
As front-desk staff, I want to book a slot for a patient who calls or walks in, so that every appointment is in the
one schedule. *(serves BR-010, BR-011, BR-003, BR-004)*

Acceptance criteria:
- AC-023 Staff can find an existing patient, or create a patient record with name, email and phone, without the
  patient having an online account.
- AC-024 Staff book a free slot for that patient with a required reason for visit. The slot is then no longer
  offered online.
- AC-025 Booking a slot that is already taken is refused for staff too, including when a patient books it online at
  the same moment.
- AC-026 Booking a third future appointment for a patient who already holds 2 is refused. Staff cannot override this.

### US-009 — Move an appointment
As front-desk staff, I want to move an appointment to another free slot, so that the patient keeps an appointment
without a cancel and rebook. *(serves BR-010, BR-004)*

Acceptance criteria:
- AC-027 Staff can move any appointment to a free slot. The old slot becomes free, and the new slot is taken.
- AC-028 Moving to a slot that is already taken is refused, and the appointment stays where it was.
- AC-029 Patients have no way to move an appointment themselves. They cancel and rebook (PO, 2026-11-23).

### US-010 — Cancel for a patient
As front-desk staff, I want to cancel any appointment, also in the last 2 hours, so that patients who call late can
still free the slot. *(serves BR-006, BR-010)*

Acceptance criteria:
- AC-030 Staff can cancel any appointment at any time before it starts, including within 2 hours of the start.
- AC-031 The cancelled slot becomes free for booking.

### US-011 — See my day as a doctor
As a doctor, I want to see my own appointments for today, so that I can prepare each morning. *(serves BR-012)*

Acceptance criteria:
- AC-032 The doctor sees a list of their own appointments for today, with time, patient name and reason for visit,
  in time order.
- AC-033 The doctor cannot book, move or cancel any appointment.
- AC-034 The doctor sees no other doctor's appointments.

### US-012 — Manage staff accounts
As a clinic admin, I want to create and disable staff accounts with a role, so that only clinic staff can see patient
data. *(serves BR-014, BR-016)*

Acceptance criteria:
- AC-035 The admin can create an account with the role front desk, doctor or clinic admin. A doctor account is linked
  to one doctor at one clinic.
- AC-036 A disabled account can no longer sign in.
- AC-037 A patient account cannot be given a staff role through registration.

### US-013 — Manage doctors' working hours
As a clinic admin, I want to set each doctor's weekly working hours, so that patients and staff are offered the right
slots. *(serves BR-005)*

Acceptance criteria:
- AC-038 The admin can set, for each doctor and each day of the week, the hours that doctor works.
- AC-039 After a change, the slots offered for that doctor are 20-minute slots inside the new hours.

### US-014 — Access to patient data is logged
As the data protection officer, I want every access to patient data logged, so that I can tell who saw a patient's
data and when. *(serves BR-015)*

Acceptance criteria:
- AC-040 Every time a user views or changes a patient's data (patient record, appointment, day list), a log entry
  records who did it, which patient it was and when.
- AC-041 Log entries are kept for 5 years.

## 4. Functional Requirements

| ID | Requirement | Serves | Stories |
|---|---|---|---|
| FR-AUTH-001 | Patients self-register with name, email address and password. Each email address belongs to at most one account. | BR-016 | US-001 |
| FR-AUTH-002 | Every user signs in with email address and password before any patient data is shown. | BR-016 | US-002 |
| FR-AUTH-003 | After 5 wrong passwords, the account is locked for 15 minutes. | BR-017 | US-002 |
| FR-AUTH-004 | A user idle for 30 minutes is signed out. | BR-018 | US-002 |
| FR-AUTH-005 | Access by role: a patient sees only their own data; a doctor sees only their own day; front desk and clinic admin see what their stories need. No one outside these roles sees patient data. | BR-009, BR-014 | US-004, US-007, US-011, US-012 |
| FR-BOOK-001 | Patients browse clinic → doctor → date → free slots. Each doctor belongs to one clinic. | BR-001, BR-005 | US-003 |
| FR-BOOK-002 | Online, only slots that start within the next 30 days and have not started yet are offered. | BR-002, BR-007 | US-003 |
| FR-BOOK-003 | Slots are 20 minutes long and are generated inside each doctor's weekly working hours. | BR-005 | US-003, US-013 |
| FR-BOOK-004 | Every booking (online or front desk) requires a free-text reason for visit. | BR-012 | US-003, US-008 |
| FR-BOOK-005 | A slot holds at most one appointment. A booking or move into a taken slot is refused on every channel, including simultaneous attempts. | BR-004 | US-003, US-008, US-009 |
| FR-BOOK-006 | A booking that would give a patient more than 2 future appointments is refused on every channel, with no staff override. | BR-003 | US-003, US-008 |
| FR-APPT-001 | Patients see a list of their own future appointments. | BR-009 | US-004 |
| FR-APPT-002 | Patients cancel their own appointment online up to 2 hours before its start. After that, online cancel is blocked and the patient is told to call the front desk. | BR-006 | US-005 |
| FR-NOTIF-001 | At 18:00 (clinic local time) on the day before each appointment that isn't cancelled, an email reminder goes to the patient's email address. | BR-008 | US-006 |
| FR-DESK-001 | Front desk sees a day view of every doctor's appointments and free slots. An empty day shows a message instead of an empty grid. | BR-010 | US-007 |
| FR-DESK-002 | Front desk finds or creates a patient record (name, email, phone) and books a free slot for that patient, including walk-ins. | BR-010, BR-011 | US-008 |
| FR-DESK-003 | Front desk moves an appointment to another free slot. Patients cannot move appointments. | BR-004, BR-010 | US-009 |
| FR-DESK-004 | Front desk cancels any appointment before it starts, including within the last 2 hours. | BR-006, BR-010 | US-010 |
| FR-DOC-001 | A doctor sees today's list of their own appointments (time, patient name, reason for visit), read-only. | BR-012 | US-011 |
| FR-ADMIN-001 | A clinic admin creates and disables staff accounts with a role (front desk, doctor, clinic admin). A doctor account is linked to one doctor at one clinic. | BR-014, BR-016 | US-012 |
| FR-ADMIN-002 | A clinic admin maintains each doctor's weekly working hours. | BR-005 | US-013 |
| FR-AUDIT-001 | Every view or change of a patient's data is logged with who, which patient and when. | BR-015 | US-014 |

## 5. Non-Functional Requirements

| ID | Requirement (measurable) | Serves |
|---|---|---|
| NFR-001 | Pages load in ≤ 2 s at the 95th percentile on a mobile 4G connection (PO, 2026-11-23). | BR-001 |
| NFR-002 | Monthly availability ≥ 99.5% (PO, 2026-11-23). | BR-001 |
| NFR-003 | Works in the latest 2 versions of Chrome, Safari and Edge, including Safari on iOS and Chrome on Android (PO, 2026-11-23). | BR-001 |
| NFR-004 | Meets WCAG 2.1 level AA (PO, 2026-11-23). | BR-001 |
| NFR-005 | The user interface and reminder emails are in English only (PO, 2026-11-23). | BR-008 |
| NFR-SEC-001 | 100% of patient data is stored in the Philippines. | BR-013 |
| NFR-SEC-002 | Account lockout after 5 consecutive wrong passwords, lasting 15 minutes. | BR-017 |
| NFR-SEC-003 | Idle sign-out after 30 minutes without activity. | BR-018 |
| NFR-SEC-004 | Access-log entries are retained for 5 years. | BR-015 |

## 6. Flows

**F1 — Patient books online (US-001 – US-003)**
1. The patient registers (first time) or signs in.
2. They choose a clinic, then a doctor of that clinic, then a date within the next 30 days.
3. They pick a free 20-minute slot that has not started yet and type the reason for visit.
4. The system checks: the slot is still free (BR-004), and the patient holds fewer than 2 future appointments (BR-003).
5. If both checks pass, the appointment is booked and shows in the patient's list. Otherwise it is refused with the
   reason, and the patient picks again.

**F2 — Patient cancels (US-004, US-005)**
1. The patient opens their upcoming appointments.
2. More than 2 hours before the start, they cancel, and the slot becomes free.
3. Within 2 hours of the start, cancel is blocked and the patient is told to call the front desk (→ F4).

**F3 — Front desk books for a caller or walk-in (US-007, US-008)**
1. Staff open the day view for the date.
2. They find the patient, or create a record (name, email, phone).
3. They pick a free slot and type the reason for visit.
4. The same checks as F1 step 4 apply. On success, the slot is no longer offered online.

**F4 — Front desk moves or cancels (US-009, US-010)**
1. Staff open the appointment from the day view.
2. Move: they pick another free slot. The old slot is freed, and a taken target is refused.
3. Cancel: allowed at any time before the start, and the slot is freed.

**F5 — Reminder (US-006)**
1. Every day at 18:00 (clinic local time), the system finds all appointments for the next day that aren't cancelled.
2. It sends one reminder email per appointment to the patient's email address.

**F6 — Doctor's morning (US-011)**
1. The doctor signs in and sees today's list of their appointments: time, patient name, reason. They can't make
   changes.

## 7. Release Scope

**In this release:** US-001 – US-014; FR-AUTH-001 – 005, FR-BOOK-001 – 006, FR-APPT-001 – 002, FR-NOTIF-001,
FR-DESK-001 – 004, FR-DOC-001, FR-ADMIN-001 – 002, FR-AUDIT-001; NFR-001 – 005, NFR-SEC-001 – 004 (PO, 2026-11-23).
Live by 2027-10-01.

**Out of this release:**
- Payments and insurance — later release (BRD).
- Video consultations — no plans (BRD).
- Link to the hospital's medical records — release 2 (BRD).

## 8. Dependencies

- An email-sending service that can deliver the 18:00 reminders (FR-NOTIF-001). Not chosen yet; the architect's call.
- Hosting and data storage located in the Philippines (NFR-SEC-001). Not chosen yet; the architect's call.
- Each doctor's weekly working hours and clinic, entered by the clinic admin before launch (FR-ADMIN-002).
- Staff accounts for the front desk and doctors, created by the clinic admin before launch (FR-ADMIN-001).

## 9. Open Questions

| # | Question | Owner | Due |
|---|---|---|---|
| 1 | Bookings made after 18:00 on the day before, or on the same day, miss the reminder time (FR-NOTIF-001). Do they get a reminder, and when? (BRD Open Question 1) | Clinic manager | — |
| 2 | Should the patient's email address be verified at sign-up, so that reminders reach them? (BRD Open Question 2) | Front-desk lead | — |
| 3 | The front desk creates a record for a patient, who later self-registers with the same email. Are they the same patient (so that the limit of 2 appointments counts across both)? | Front-desk lead | — |
| 4 | Does the 30-day booking limit also apply to front-desk bookings and moves? | Clinic manager | — |
| 5 | When a doctor's working hours are reduced and appointments already exist in the removed hours, what happens to those appointments? | Clinic manager | — |
| 6 | Is the patient emailed when the front desk moves or cancels their appointment? | Clinic manager | — |
| 7 | Who can read the access log, and how (screen in the app, export, on request)? | Data protection officer | — |
| 8 | Is the clinic admin the clinic manager, or another person? On which device do they work? | Clinic manager | — |
