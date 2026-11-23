"""E004 Front Desk & Doctor Views: DES-009 … DES-012.

Front desk sees every doctor; a doctor sees only their own day, read-only (FR-AUTH-005).
Day 1: book / move / cancel go through scheduling.services (ADR-CARESLOT-E002-001), and every
view of patient data writes an AuditLog row (ADR-CARESLOT-E006-001).
"""

from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET

from core.auth import role_required
from core.demo import demo_state
from core.roles import Role
from patient_portal.mock import SAMPLE_DAY
from staff_portal import mock


@require_GET
@role_required(Role.FRONT_DESK)
def desk_day(request: HttpRequest) -> HttpResponse:
    """DES-009 (US-007, FR-DESK-001, AC-021, AC-022): one card per doctor, side by side."""
    state = demo_state(request, frozenset({"empty", "loading", "error"}))
    doctors = mock.desk_day() if state == "default" else []
    return render(
        request,
        "staff_portal/desk_day.html",
        {"state": state, "day": SAMPLE_DAY, "doctors": doctors},
    )


@require_GET
@role_required(Role.FRONT_DESK)
def desk_book(request: HttpRequest) -> HttpResponse:
    """DES-010 (US-008, FR-DESK-002, AC-023 – AC-026): book for a caller or walk-in."""
    state = demo_state(request, frozenset({"empty", "error", "taken", "limit", "disabled"}))
    results = [] if state == "empty" else mock.patient_search_results()
    return render(
        request,
        "staff_portal/desk_book.html",
        {
            "state": state,
            "results": results,
            "slot": mock.desk_day()[0].slots[1],
            "doctor_name": "Dr. Ana Reyes",
            "clinic_name": "Clinic A",
        },
    )


@require_GET
@role_required(Role.FRONT_DESK)
def desk_appointment(request: HttpRequest, appointment_id: int) -> HttpResponse:
    """DES-011 (US-009, US-010, FR-DESK-003, FR-DESK-004, AC-027, AC-028, AC-030, AC-031)."""
    appointment = mock.appointment(appointment_id)
    if appointment is None:
        raise Http404
    state = demo_state(request, frozenset({"confirm", "error", "loading", "disabled"}))
    return render(
        request,
        "staff_portal/desk_appointment.html",
        {"state": state, "appointment": appointment, "move_slots": mock.move_slots()},
    )


@require_GET
@role_required(Role.DOCTOR)
def doctor_day(request: HttpRequest) -> HttpResponse:
    """DES-012 (US-011, FR-DOC-001, AC-032 – AC-034): read-only, own appointments only."""
    state = demo_state(request, frozenset({"empty", "loading", "error"}))
    day = mock.doctor_day()
    appointments = day.appointments if state == "default" else ()
    return render(
        request,
        "staff_portal/doctor_day.html",
        {"state": state, "day": day, "appointments": appointments},
    )
