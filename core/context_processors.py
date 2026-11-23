from typing import Any

from django.http import HttpRequest

from core.roles import Role
from core.viewmodels import NavLink

# Header links per role (designer's choice, 2026-11-23: logo, links, user, Sign out).
NAV: dict[Role, tuple[NavLink, ...]] = {
    Role.PATIENT: (
        NavLink("book_doctor", "Book"),
        NavLink("my_appointments", "My appointments"),
    ),
    Role.FRONT_DESK: (
        NavLink("desk_day", "Day view"),
        NavLink("desk_book", "Book for patient"),
    ),
    Role.DOCTOR: (NavLink("doctor_day", "My day"),),
    Role.CLINIC_ADMIN: (
        NavLink("staff_accounts", "Staff accounts"),
        NavLink("working_hours", "Working hours"),
    ),
}


def shell(request: HttpRequest) -> dict[str, Any]:
    """What the header needs on every page: the signed-in role and its links."""
    role: Role | None = getattr(request, "mock_role", None)
    return {
        "current_role": role,
        "current_role_label": role.label if role else "",
        "nav_links": NAV.get(role, ()) if role else (),
    }
