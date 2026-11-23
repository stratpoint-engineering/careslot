"""Day 0 sample data for E003 screens (names and dates made up). Day 1 replaces these with
queries through scheduling.services that return the same view-models."""

from datetime import date, datetime, time, timedelta

from django.utils import timezone

from core.rules import ONLINE_BOOKING_WINDOW
from core.viewmodels import Option
from patient_portal.viewmodels import AppointmentVM, BookingChoiceVM, SlotVM

SAMPLE_DAY = date(2027, 10, 12)


def at(day: date, hour: int, minute: int = 0) -> datetime:
    return timezone.make_aware(datetime.combine(day, time(hour, minute)))


def clinic_options() -> list[Option]:
    return [Option("1", "Clinic A", True), Option("2", "Clinic B"), Option("3", "Clinic C")]


def doctor_options() -> list[Option]:
    return [
        Option("", "Choose a doctor", True),
        Option("1", "Dr. Ana Reyes"),
        Option("2", "Dr. Ben Lim"),
    ]


def booking_choice() -> BookingChoiceVM:
    today = SAMPLE_DAY - timedelta(days=5)
    return BookingChoiceVM(
        1, "Dr. Ana Reyes", "Clinic A", SAMPLE_DAY, today, today + ONLINE_BOOKING_WINDOW
    )


def free_slots() -> list[SlotVM]:
    times = [(8, 0), (8, 20), (9, 0), (9, 40), (10, 20), (11, 0), (11, 40)]
    return [SlotVM(at(SAMPLE_DAY, h, m)) for h, m in times]


def chosen_appointment() -> AppointmentVM:
    return AppointmentVM(
        0, at(SAMPLE_DAY, 9), "Dr. Ana Reyes", "Clinic A", reason="Cough for two weeks"
    )


def my_appointments(*, two_with_one_soon: bool = False) -> list[AppointmentVM]:
    if two_with_one_soon:
        soon = timezone.localtime() + timedelta(minutes=80)
        return [
            AppointmentVM(
                1,
                soon.replace(second=0, microsecond=0),
                "Dr. Ana Reyes",
                "Clinic A",
                can_cancel_online=False,
            ),
            AppointmentVM(2, at(SAMPLE_DAY, 9), "Dr. Ben Lim", "Clinic B"),
        ]
    return [AppointmentVM(1, at(SAMPLE_DAY, 9), "Dr. Ana Reyes", "Clinic A")]
