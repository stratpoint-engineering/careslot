"""Schema guarantees from ARCH-CARESLOT-v1 §5 that hold no matter which code writes the row."""

from datetime import datetime, time

import pytest
from django.db import IntegrityError, transaction
from django.utils import timezone

from accounts.models import Patient
from scheduling.models import (
    Appointment,
    AppointmentStatus,
    Channel,
    Clinic,
    Doctor,
    Weekday,
    WorkingHours,
)

pytestmark = pytest.mark.django_db


@pytest.fixture
def doctor() -> Doctor:
    return Doctor.objects.create(full_name="Dr. Test", clinic=Clinic.objects.create(name="C"))


@pytest.fixture
def patient() -> Patient:
    return Patient.objects.create(full_name="P One")


START = timezone.make_aware(datetime(2027, 10, 12, 9, 0))


def book(doctor: Doctor, patient: Patient, **extra: object) -> Appointment:
    return Appointment.objects.create(
        doctor=doctor,
        patient=patient,
        start=START,
        reason="Check-up",
        channel=Channel.ONLINE,
        **extra,
    )


def test_a_slot_holds_one_booked_appointment(doctor: Doctor, patient: Patient) -> None:
    """BR-004 / FR-BOOK-005, enforced by the database on every channel."""
    book(doctor, patient)
    other = Patient.objects.create(full_name="P Two")
    with pytest.raises(IntegrityError), transaction.atomic():
        Appointment.objects.create(
            doctor=doctor, patient=other, start=START, reason="X", channel=Channel.FRONT_DESK
        )


def test_a_cancelled_slot_can_be_booked_again(doctor: Doctor, patient: Patient) -> None:
    book(doctor, patient, status=AppointmentStatus.CANCELLED)
    book(doctor, patient)
    assert Appointment.objects.filter(status=AppointmentStatus.BOOKED).count() == 1


def test_reason_is_required(doctor: Doctor, patient: Patient) -> None:
    """FR-BOOK-004."""
    with pytest.raises(IntegrityError), transaction.atomic():
        Appointment.objects.create(
            doctor=doctor, patient=patient, start=START, reason="", channel=Channel.ONLINE
        )


def test_working_hours_end_after_start(doctor: Doctor) -> None:
    with pytest.raises(IntegrityError), transaction.atomic():
        WorkingHours.objects.create(
            doctor=doctor, weekday=Weekday.MONDAY, start_time=time(12), end_time=time(10)
        )
