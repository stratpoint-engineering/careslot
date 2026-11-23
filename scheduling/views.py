"""E002 Scheduling Core screen: DES-004 Working hours.

Booking rules (slot free, max 2, reason required) will live in scheduling/services.py from Day 1;
every channel calls it (ADR-CARESLOT-E002-001). No service code on Day 0.
"""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET

from core.auth import role_required
from core.demo import demo_state
from core.roles import Role
from scheduling import mock
from scheduling.models import Weekday


@require_GET
@role_required(Role.CLINIC_ADMIN)
def working_hours(request: HttpRequest) -> HttpResponse:
    """DES-004 (US-013, FR-ADMIN-002, FR-BOOK-003). Saving hours is Day 1."""
    state = demo_state(request, frozenset({"empty", "loading", "error", "disabled"}))
    days = mock.working_week(
        blank=state == "empty", error_on=Weekday.TUESDAY if state == "error" else None
    )
    return render(
        request,
        "scheduling/working_hours.html",
        {"state": state, "days": days, "doctor_options": mock.doctor_options()},
    )
