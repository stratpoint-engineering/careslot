"""Reminder outbox (ADR-CARESLOT-E005-001; epic E005).

The booking service writes one Reminder per appointment in the same transaction. A Celery job
(Day 1) sends every due, unsent reminder every minute, with retries, so nothing is lost.
"""

from typing import ClassVar

from django.db import models


class ReminderStatus(models.TextChoices):
    PENDING = "pending", "Pending"
    SENT = "sent", "Sent"
    CANCELLED = "cancelled", "Cancelled"


class Reminder(models.Model):
    appointment = models.OneToOneField(
        "scheduling.Appointment", on_delete=models.CASCADE, related_name="reminder"
    )
    due_at = models.DateTimeField()  # 18:00 clinic time on the day before (FR-NOTIF-001)
    status = models.CharField(
        max_length=20, choices=ReminderStatus.choices, default=ReminderStatus.PENDING
    )
    sent_at = models.DateTimeField(null=True, blank=True)
    attempts = models.PositiveIntegerField(default=0)
    last_error = models.TextField(blank=True)

    class Meta:
        indexes: ClassVar = [models.Index(fields=["status", "due_at"])]

    def __str__(self) -> str:
        return f"Reminder for appointment {self.appointment_id} at {self.due_at:%Y-%m-%d %H:%M}"
