"""E003 Patient Self-Service screens: DES-005 … DES-008. Patients only (FR-AUTH-005).

Day 0 renders mock data. Day 1: reads and writes go through scheduling.services
(ADR-CARESLOT-E002-001), and every view of patient data writes an AuditLog row (ADR-CARESLOT-E006-001).
"""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET

from core.auth import role_required
from core.demo import demo_state
from core.roles import Role
from core.rules import MAX_FUTURE_APPOINTMENTS
from patient_portal import mock


@require_GET
@role_required(Role.PATIENT)
def book_doctor(request: HttpRequest) -> HttpResponse:
    """DES-005 step 1: clinic → doctor (US-003, FR-BOOK-001, AC-006)."""
    state = demo_state(request, frozenset({"loading", "error", "disabled"}))
    return render(
        request,
        "patient_portal/book_doctor.html",
        {
            "state": state,
            "clinic_options": mock.clinic_options(),
            "doctor_options": mock.doctor_options(),
        },
    )


@require_GET
@role_required(Role.PATIENT)
def book_time(request: HttpRequest) -> HttpResponse:
    """DES-006 step 2: date → free 20-minute time (FR-BOOK-002, FR-BOOK-003, AC-007, AC-008)."""
    state = demo_state(request, frozenset({"empty", "loading", "error"}))
    slots = mock.free_slots() if state == "default" else []
    return render(
        request,
        "patient_portal/book_time.html",
        {"state": state, "choice": mock.booking_choice(), "slots": slots},
    )


@require_GET
@role_required(Role.PATIENT)
def book_confirm(request: HttpRequest) -> HttpResponse:
    """DES-007 step 3: reason and confirm (FR-BOOK-004/005/006, AC-009 – AC-011)."""
    state = demo_state(request, frozenset({"error", "taken", "limit", "disabled"}))
    return render(
        request,
        "patient_portal/book_confirm.html",
        {
            "state": state,
            "appointment": mock.chosen_appointment(),
            "max_appointments": MAX_FUTURE_APPOINTMENTS,
        },
    )


@require_GET
@role_required(Role.PATIENT)
def my_appointments(request: HttpRequest) -> HttpResponse:
    """DES-008 (US-004, US-005, FR-APPT-001, FR-APPT-002, AC-013 – AC-017)."""
    state = demo_state(
        request, frozenset({"booked", "empty", "loading", "error", "disabled", "confirm"})
    )
    if state in {"empty", "loading"}:
        appointments = []
    else:
        appointments = mock.my_appointments(two_with_one_soon=state == "disabled")
    return render(
        request,
        "patient_portal/my_appointments.html",
        {
            "state": state,
            "appointments": appointments,
            "at_limit": len(appointments) >= MAX_FUTURE_APPOINTMENTS,
            "max_appointments": MAX_FUTURE_APPOINTMENTS,
        },
    )
