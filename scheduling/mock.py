"""Day 0 sample data for E002 screens (names made up). Day 1 returns the same view-models from
WorkingHours rows."""

from datetime import time

from core.viewmodels import Option
from scheduling.models import Weekday
from scheduling.viewmodels import WorkingDayVM

_SAMPLE = {
    Weekday.MONDAY: (time(8), time(12)),
    Weekday.TUESDAY: (time(8), time(12)),
    Weekday.WEDNESDAY: (time(13), time(17)),
    Weekday.THURSDAY: (time(8), time(12)),
    Weekday.FRIDAY: (time(8), time(12)),
}


def working_week(*, blank: bool = False, error_on: int | None = None) -> list[WorkingDayVM]:
    days = []
    for day in Weekday:
        start, end = (None, None) if blank else _SAMPLE.get(day, (None, None))
        error = ""
        if day == error_on:
            start, end, error = time(12), time(10), "End time must be after start time."
        days.append(WorkingDayVM(day.value, day.label, start, end, error))
    return days


def doctor_options() -> list[Option]:
    return [Option("1", "Dr. Ana Reyes — Clinic A", True), Option("2", "Dr. Ben Lim — Clinic B")]
