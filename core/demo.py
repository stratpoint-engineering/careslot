"""Dev-only switch to view a screen's design states (empty / loading / error / disabled …) with mock data.

Only active when settings.CARESLOT_DEMO_STATES is True (dev and test). In production every page
renders its real state, decided by real data from Day 1 on.
"""

from django.conf import settings
from django.http import HttpRequest

DEFAULT = "default"


def demo_state(request: HttpRequest, allowed: frozenset[str]) -> str:
    requested = request.GET.get("state", DEFAULT)
    if settings.CARESLOT_DEMO_STATES and requested in allowed:
        return requested
    return DEFAULT
