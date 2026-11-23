import re
import uuid
from collections.abc import Callable

from django.http import HttpRequest, HttpResponse

from core.auth import read_mock_role
from core.logging import request_id_var

_SAFE_ID = re.compile(r"^[A-Za-z0-9._=;-]{1,128}$")


class RequestIdMiddleware:
    """Gives every request an id, puts it on every log line and on the response."""

    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        incoming = request.headers.get("X-Request-ID", "")
        request_id = incoming if _SAFE_ID.match(incoming) else uuid.uuid4().hex
        token = request_id_var.set(request_id)
        try:
            response = self.get_response(request)
        finally:
            request_id_var.reset(token)
        response["X-Request-ID"] = request_id
        return response


class MockRoleMiddleware:
    """Day 0: reads the signed mock-role cookie into `request.mock_role` (None when signed out)."""

    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        request.mock_role = read_mock_role(request)  # type: ignore[attr-defined]
        return self.get_response(request)
