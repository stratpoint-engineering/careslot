"""Dev-only switch to view a screen's design states (empty / loading / error / disabled …) with mock data.

Only active when settings.CARESLOT_DEMO_STATES is True (dev and test). In production every page
renders its real state, decided by real data from Day 1 on.
"""

from urllib.parse import urlencode

from django.conf import settings
from django.http import HttpRequest, HttpResponseRedirect
from django.urls import reverse

DEFAULT = "default"


def mock_submit(url_name: str, state: str = "", **kwargs: object) -> HttpResponseRedirect:
    """Day 0 form submit: saves nothing, goes to the next screen of the flow (POST → redirect → GET).

    Day 1 replaces each call with the real service call, keeping the same redirect target.
    """
    url = reverse(url_name, kwargs=kwargs or None)
    return HttpResponseRedirect(f"{url}?{urlencode({'state': state})}" if state else url)


def demo_state(request: HttpRequest, allowed: frozenset[str]) -> str:
    requested = request.GET.get("state", DEFAULT)
    if settings.CARESLOT_DEMO_STATES and requested in allowed:
        return requested
    return DEFAULT
