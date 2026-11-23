import re
from datetime import datetime
from pathlib import Path

from django.conf import settings
from django.utils import timezone

from notifications.emails import render_reminder
from patient_portal.viewmodels import AppointmentVM


def test_reminder_email_has_the_appointment_details() -> None:
    """DES-013 / AC-018: date, time, clinic and doctor; English only."""
    appt = AppointmentVM(
        1, timezone.make_aware(datetime(2027, 10, 12, 9, 0)), "Dr. Ana Reyes", "Clinic A"
    )
    email = render_reminder(appt, "Maria", "https://careslot.example/me/appointments")
    assert email.subject == "Reminder: your appointment tomorrow at 09:00"
    for part in (email.text, email.html):
        assert "Tue 12 Oct 2027, 09:00" in part
        assert "Dr. Ana Reyes" in part
        assert "Clinic A" in part


def test_email_colours_are_token_values() -> None:
    """Email clients can't read tokens.css, so the email repeats values; they must be tokens."""
    root = Path(settings.BASE_DIR)
    tokens = set(re.findall(r"hsl\([^)]*\)", (root / "static/css/tokens.css").read_text()))
    email = (root / "templates/notifications/email/reminder.html").read_text()
    used = set(re.findall(r"hsl\([^)]*\)", email))
    assert used
    assert used <= tokens
