"""Day 0 mock authentication: a signed cookie holding the user's role.

No credentials are checked. Day 1 replaces this with Django auth + django-axes
(ADR-CARESLOT-E001-002); the `role_required` contract stays the same.
"""

from collections.abc import Callable
from functools import wraps
from typing import Any
from urllib.parse import urlencode

from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, resolve_url

from core.roles import Role

COOKIE_SALT = "careslot.mock-role"

View = Callable[..., HttpResponse]


def read_mock_role(request: HttpRequest) -> Role | None:
    raw = request.get_signed_cookie(
        settings.MOCK_ROLE_COOKIE,
        default=None,
        salt=COOKIE_SALT,
        max_age=settings.MOCK_ROLE_MAX_AGE,
    )
    return Role(raw) if raw in Role.values else None


def set_mock_role(response: HttpResponse, role: Role) -> None:
    response.set_signed_cookie(
        settings.MOCK_ROLE_COOKIE,
        role.value,
        salt=COOKIE_SALT,
        max_age=settings.MOCK_ROLE_MAX_AGE,
        httponly=True,
        samesite="Lax",
        secure=settings.SESSION_COOKIE_SECURE,
    )


def clear_mock_role(response: HttpResponse) -> None:
    response.delete_cookie(settings.MOCK_ROLE_COOKIE, samesite="Lax")


def role_required(*roles: Role) -> Callable[[View], View]:
    """Server-side guard (team pattern): not signed in → sign-in page; wrong role → 403."""

    def decorator(view: View) -> View:
        @wraps(view)
        def wrapped(request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
            role = getattr(request, "mock_role", None)
            if role is None:
                return redirect(
                    f"{resolve_url(settings.LOGIN_URL)}?{urlencode({'next': request.path})}"
                )
            if role not in roles:
                raise PermissionDenied
            return view(request, *args, **kwargs)

        wrapped.required_roles = roles  # type: ignore[attr-defined]
        return wrapped

    return decorator
