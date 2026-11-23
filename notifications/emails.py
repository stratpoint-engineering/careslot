"""DES-013 Reminder email — Epic E005 — serves US-006, FR-NOTIF-001, AC-018.

Rendering only. Sending (Celery outbox job + Amazon SES, ADR-CARESLOT-E005-001/002) is Day 1.
English only (NFR-005).
"""

from dataclasses import dataclass

from django.template.loader import render_to_string

from patient_portal.viewmodels import AppointmentVM


@dataclass(frozen=True)
class RenderedEmail:
    subject: str
    text: str
    html: str


def render_reminder(
    appointment: AppointmentVM, patient_first_name: str, appointments_url: str
) -> RenderedEmail:
    context = {
        "appointment": appointment,
        "first_name": patient_first_name,
        "appointments_url": appointments_url,
    }
    return RenderedEmail(
        subject=f"Reminder: your appointment tomorrow at {appointment.starts_at:%H:%M}",
        text=render_to_string("notifications/email/reminder.txt", context),
        html=render_to_string("notifications/email/reminder.html", context),
    )
