"""Clinics, doctors, working hours and appointments (ARCH-CARESLOT-v1 §5; epic E002).

Slots are NOT stored: they are generated from WorkingHours in 20-minute steps (FR-BOOK-003).
"""

from typing import ClassVar

from django.conf import settings
from django.db import models
from django.db.models import F, Q


class Clinic(models.Model):
    name = models.CharField(max_length=200, unique=True)

    def __str__(self) -> str:
        return self.name


class Doctor(models.Model):
    """Each doctor works at exactly one clinic (PO, 2026-11-23)."""

    full_name = models.CharField(max_length=200)
    clinic = models.ForeignKey(Clinic, on_delete=models.PROTECT, related_name="doctors")
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="doctor",
    )

    def __str__(self) -> str:
        return self.full_name


class Weekday(models.IntegerChoices):
    MONDAY = 0, "Monday"
    TUESDAY = 1, "Tuesday"
    WEDNESDAY = 2, "Wednesday"
    THURSDAY = 3, "Thursday"
    FRIDAY = 4, "Friday"
    SATURDAY = 5, "Saturday"
    SUNDAY = 6, "Sunday"


class WorkingHours(models.Model):
    """One working period per doctor and weekday (FR-ADMIN-002, DES-004). No row = not working."""

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name="working_hours")
    weekday = models.PositiveSmallIntegerField(choices=Weekday.choices)
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        constraints: ClassVar = [
            models.UniqueConstraint(fields=["doctor", "weekday"], name="one_period_per_doctor_day"),
            models.CheckConstraint(
                condition=Q(end_time__gt=F("start_time")), name="hours_end_after_start"
            ),
        ]

    def __str__(self) -> str:
        return f"{self.doctor} {self.get_weekday_display()} {self.start_time}-{self.end_time}"


class AppointmentStatus(models.TextChoices):
    BOOKED = "booked", "Booked"
    CANCELLED = "cancelled", "Cancelled"


class Channel(models.TextChoices):
    """Where a booking came from; feeds the online-share metric (BRD goal G2)."""

    ONLINE = "online", "Online"
    FRONT_DESK = "front_desk", "Front desk"


class Appointment(models.Model):
    """Only scheduling.services may create, move or cancel these (ADR-CARESLOT-E002-001)."""

    doctor = models.ForeignKey(Doctor, on_delete=models.PROTECT, related_name="appointments")
    patient = models.ForeignKey(
        "accounts.Patient", on_delete=models.PROTECT, related_name="appointments"
    )
    start = models.DateTimeField()
    status = models.CharField(
        max_length=20, choices=AppointmentStatus.choices, default=AppointmentStatus.BOOKED
    )
    reason = models.TextField()  # required free text (FR-BOOK-004)
    channel = models.CharField(max_length=20, choices=Channel.choices)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL,
        related_name="appointments_created",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    cancelled_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        constraints: ClassVar = [
            # BR-004 / FR-BOOK-005: a slot holds at most one booked appointment, on every channel.
            models.UniqueConstraint(
                fields=["doctor", "start"],
                condition=Q(status="booked"),
                name="one_booked_appointment_per_slot",
            ),
            models.CheckConstraint(condition=~Q(reason=""), name="appointment_reason_required"),
        ]
        indexes: ClassVar = [
            models.Index(fields=["doctor", "start"]),
            models.Index(fields=["patient", "start"]),
        ]

    def __str__(self) -> str:
        return f"{self.start:%Y-%m-%d %H:%M} {self.doctor} / {self.patient}"
