import logging

from django.db import DatabaseError, connection
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_GET

from core.roles import HOME_URL_NAME

logger = logging.getLogger(__name__)


@require_GET
@never_cache
def healthz(request: HttpRequest) -> JsonResponse:
    """ALB/ECS health check. The only JSON endpoint: 200 when the app and database answer."""
    try:
        connection.ensure_connection()
    except DatabaseError:
        logger.exception("health check: database unreachable")
        return JsonResponse({"status": "error", "database": "unreachable"}, status=503)
    return JsonResponse({"status": "ok", "database": "ok"})


@require_GET
def home(request: HttpRequest) -> HttpResponse:
    role = getattr(request, "mock_role", None)
    if role is None:
        return redirect("signin")
    return redirect(HOME_URL_NAME[role])
