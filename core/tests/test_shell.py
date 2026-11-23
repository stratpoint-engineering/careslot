"""Day 0 shell: every guarded page, every design state, the mock auth guard, health and headers."""

import json
import logging

import pytest
from django.test import Client
from django.urls import URLPattern, URLResolver, get_resolver, reverse

from core.auth import COOKIE_SALT
from core.logging import RequestIdFilter
from core.roles import Role

PUBLIC = {"home", "signin", "signout", "register", "healthz"}

# url name → (role allowed, kwargs, design states from the DES frame)
PAGES: dict[str, tuple[Role, dict[str, int], list[str]]] = {
    "staff_accounts": (Role.CLINIC_ADMIN, {}, ["empty", "loading", "error", "disabled"]),
    "working_hours": (Role.CLINIC_ADMIN, {}, ["empty", "loading", "error", "disabled"]),
    "book_doctor": (Role.PATIENT, {}, ["loading", "error", "disabled"]),
    "book_time": (Role.PATIENT, {}, ["empty", "loading", "error"]),
    "book_confirm": (Role.PATIENT, {}, ["error", "taken", "limit", "disabled"]),
    "my_appointments": (
        Role.PATIENT,
        {},
        ["booked", "empty", "loading", "error", "disabled", "confirm"],
    ),
    "desk_day": (Role.FRONT_DESK, {}, ["empty", "loading", "error"]),
    "desk_book": (Role.FRONT_DESK, {}, ["empty", "error", "taken", "limit", "disabled"]),
    "desk_appointment": (
        Role.FRONT_DESK,
        {"appointment_id": 1},
        ["confirm", "error", "loading", "disabled"],
    ),
    "doctor_day": (Role.DOCTOR, {}, ["empty", "loading", "error"]),
}


def signed_in(role: Role) -> Client:
    client = Client()
    client.cookies.load({"mock-role": ""})
    response = client.post(
        reverse("signin"), {"email": "x@example.com", "password": "anything", "role": role.value}
    )
    assert response.status_code == 302
    return client


def all_url_names() -> set[str]:
    names: set[str] = set()

    def walk(patterns: list[URLPattern | URLResolver]) -> None:
        for p in patterns:
            if isinstance(p, URLResolver):
                walk(p.url_patterns)
            elif p.name:
                names.add(p.name)

    walk(get_resolver().url_patterns)
    return names


def test_every_route_is_either_public_or_listed_and_guarded() -> None:
    assert all_url_names() == PUBLIC | set(PAGES)


@pytest.mark.parametrize("name", sorted(PAGES))
def test_signed_out_is_redirected_to_signin(name: str) -> None:
    _, kwargs, _ = PAGES[name]
    url = reverse(name, kwargs=kwargs)
    response = Client().get(url)
    assert response.status_code == 302
    assert response["Location"].startswith(reverse("signin"))


@pytest.mark.parametrize("name", sorted(PAGES))
def test_wrong_role_gets_403(name: str) -> None:
    allowed, kwargs, _ = PAGES[name]
    other = next(r for r in Role if r != allowed)
    response = signed_in(other).get(reverse(name, kwargs=kwargs))
    assert response.status_code == 403
    assert b"No access" in response.content


@pytest.mark.parametrize(
    ("name", "state"),
    [(n, s) for n, (_, _, states) in sorted(PAGES.items()) for s in ["default", *states]],
)
def test_every_page_renders_every_design_state(name: str, state: str) -> None:
    role, kwargs, _ = PAGES[name]
    response = signed_in(role).get(reverse(name, kwargs=kwargs), {"state": state})
    assert response.status_code == 200
    assert b'<main id="main">' in response.content


@pytest.mark.parametrize("state", ["default", "error", "locked", "idle", "disabled"])
def test_signin_states_render(state: str) -> None:
    assert Client().get(reverse("signin"), {"state": state}).status_code == 200


@pytest.mark.parametrize("state", ["default", "error", "disabled"])
def test_register_states_render(state: str) -> None:
    assert Client().get(reverse("register"), {"state": state}).status_code == 200


@pytest.mark.parametrize("role", list(Role))
def test_signin_sends_each_role_home(role: Role) -> None:
    response = Client().post(
        reverse("signin"), {"email": "a@example.com", "password": "x", "role": role.value}
    )
    expected = {
        Role.PATIENT: "my_appointments",
        Role.FRONT_DESK: "desk_day",
        Role.DOCTOR: "doctor_day",
        Role.CLINIC_ADMIN: "staff_accounts",
    }[role]
    assert response["Location"] == reverse(expected)


def test_signin_shows_inline_errors_without_toasts() -> None:
    response = Client().post(reverse("signin"), {"email": "", "password": "", "role": "patient"})
    assert response.status_code == 200
    assert b'class="err"' in response.content
    assert b"Enter your email." in response.content


def test_signin_ignores_offsite_next() -> None:
    response = Client().post(
        reverse("signin") + "?next=https://evil.example/",
        {"email": "a@example.com", "password": "x", "role": "patient"},
    )
    assert response["Location"] == reverse("my_appointments")


def test_tampered_cookie_is_signed_out() -> None:
    client = Client()
    client.cookies["mock-role"] = "clinic_admin"  # unsigned value
    assert client.get(reverse("staff_accounts")).status_code == 302
    assert COOKIE_SALT  # the salt is what makes a forged value fail


def test_signout_clears_role() -> None:
    client = signed_in(Role.PATIENT)
    client.post(reverse("signout"))
    assert client.get(reverse("my_appointments")).status_code == 302


def test_signout_requires_post() -> None:
    assert signed_in(Role.PATIENT).get(reverse("signout")).status_code == 405


@pytest.mark.django_db
def test_healthz_ok() -> None:
    response = Client().get(reverse("healthz"))
    assert response.status_code == 200
    assert json.loads(response.content) == {"status": "ok", "database": "ok"}


def test_security_headers_and_request_id() -> None:
    response = Client().get(reverse("signin"))
    assert response["X-Frame-Options"] == "DENY"
    assert response["X-Content-Type-Options"] == "nosniff"
    assert "default-src 'self'" in response["Content-Security-Policy"]
    assert "frame-ancestors 'none'" in response["Content-Security-Policy"]
    assert len(response["X-Request-ID"]) == 32


def test_404_page_uses_design() -> None:
    response = Client().get("/does-not-exist")
    assert response.status_code == 404
    assert b"Page not found" in response.content


def test_log_records_carry_request_id() -> None:
    record = logging.LogRecord("x", logging.INFO, __file__, 1, "msg", None, None)
    assert RequestIdFilter().filter(record)
    assert getattr(record, "request_id") == "-"  # noqa: B009


# Day 0 form submits: nothing is saved, every form moves to the next screen (never a bare 405).
# (role, url name, kwargs, POST data, expected redirect name, expected ?state=)
SUBMITS = [
    (Role.PATIENT, "book_confirm", {}, {"reason": "Cough"}, "my_appointments", "booked"),
    (Role.PATIENT, "my_appointments", {}, {"cancel": "1"}, "my_appointments", "confirm"),
    (Role.PATIENT, "my_appointments", {}, {"confirm_cancel": "1"}, "my_appointments", ""),
    (Role.FRONT_DESK, "desk_book", {}, {"reason": "Fever"}, "desk_day", ""),
    (
        Role.FRONT_DESK,
        "desk_appointment",
        {"appointment_id": 1},
        {"cancel": "1"},
        "desk_appointment",
        "confirm",
    ),
    (Role.FRONT_DESK, "desk_appointment", {"appointment_id": 1}, {"move_to": "x"}, "desk_day", ""),
    (Role.CLINIC_ADMIN, "staff_accounts", {}, {"disable": "1"}, "staff_accounts", "disabled"),
    (Role.CLINIC_ADMIN, "staff_accounts", {}, {"staff_email": "a@b.c"}, "staff_accounts", ""),
    (Role.CLINIC_ADMIN, "working_hours", {}, {"start-0": "08:00"}, "working_hours", ""),
]


@pytest.mark.parametrize(("role", "name", "kwargs", "data", "target", "state"), SUBMITS)
def test_day0_form_submits_go_to_the_next_screen(
    role: Role, name: str, kwargs: dict[str, int], data: dict[str, str], target: str, state: str
) -> None:
    response = signed_in(role).post(reverse(name, kwargs=kwargs or None), data)
    assert response.status_code == 302
    target_kwargs = kwargs if target == name else None
    expected = reverse(target, kwargs=target_kwargs or None) + (f"?state={state}" if state else "")
    assert response["Location"] == expected


def test_register_submit_goes_to_signin() -> None:
    response = Client().post(reverse("register"), {"email": "a@example.com"})
    assert response["Location"] == reverse("signin")


def test_unknown_appointment_post_is_404() -> None:
    response = signed_in(Role.FRONT_DESK).post(
        reverse("desk_appointment", kwargs={"appointment_id": 999}), {"cancel": "1"}
    )
    assert response.status_code == 404
