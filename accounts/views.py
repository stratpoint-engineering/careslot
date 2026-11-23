"""E001 Accounts & Access screens: DES-001 Register, DES-002 Sign in, DES-003 Staff accounts."""

from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_http_methods, require_POST

from accounts import mock
from accounts.forms import MockSignInForm
from core.auth import clear_mock_role, role_required, set_mock_role
from core.demo import demo_state, mock_submit
from core.roles import HOME_URL_NAME, Role
from core.viewmodels import Option


@require_http_methods(["GET", "POST"])
def register(request: HttpRequest) -> HttpResponse:
    """DES-001 (US-001, FR-AUTH-001). Saving the account is Day 1."""
    if request.method == "POST":  # Day 0: nothing saved; Day 1 creates the account (FR-AUTH-001)
        return mock_submit("signin")
    state = demo_state(request, frozenset({"error", "disabled"}))
    return render(request, "accounts/register.html", {"state": state})


@require_http_methods(["GET", "POST"])
def signin(request: HttpRequest) -> HttpResponse:
    """DES-002 (US-002). Day 0 mock: any credentials; the chosen role is stored in a signed cookie."""
    state = demo_state(request, frozenset({"error", "locked", "idle", "disabled"}))
    form = MockSignInForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        role = Role(form.cleaned_data["role"])
        target = request.GET.get("next", "")
        if not url_has_allowed_host_and_scheme(
            target, allowed_hosts={request.get_host()}, require_https=request.is_secure()
        ):
            target = ""
        response = redirect(target or HOME_URL_NAME[role])
        set_mock_role(response, role)
        return response
    role_options = [
        Option(r.value, r.label, selected=(form["role"].value() == r.value)) for r in Role
    ]
    return render(
        request,
        "accounts/signin.html",
        {"state": state, "form": form, "role_options": role_options},
    )


@require_POST
def signout(request: HttpRequest) -> HttpResponse:
    response = redirect("signin")
    clear_mock_role(response)
    return response


@require_http_methods(["GET", "POST"])
@role_required(Role.CLINIC_ADMIN)
def staff_accounts(request: HttpRequest) -> HttpResponse:
    """DES-003 (US-012, FR-ADMIN-001). Creating and disabling accounts is Day 1."""
    if request.method == "POST":  # Day 0: nothing saved
        if "disable" in request.POST:  # first click asks to confirm (designer's choice)
            return mock_submit("staff_accounts", "disabled")
        return mock_submit("staff_accounts")
    state = demo_state(request, frozenset({"empty", "loading", "error", "disabled"}))
    accounts = [] if state in {"empty", "loading"} else mock.staff_accounts()
    return render(
        request,
        "accounts/staff_accounts.html",
        {
            "state": state,
            "accounts": accounts,
            "role_options": mock.staff_role_options(),
            "clinic_options": mock.clinic_options(),
        },
    )
