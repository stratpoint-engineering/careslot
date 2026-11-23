from dataclasses import dataclass
from datetime import date, datetime


@dataclass(frozen=True)
class AppointmentVM:
    """An appointment as patients and staff see it (DES-007, DES-008, DES-011, DES-013)."""

    id: int
    starts_at: datetime
    doctor_name: str
    clinic_name: str
    patient_name: str = ""
    reason: str = ""
    can_cancel_online: bool = True  # False within 2 hours of the start (BR-006)


@dataclass(frozen=True)
class SlotVM:
    """A 20-minute time on a doctor's day (DES-006, DES-009, DES-011)."""

    starts_at: datetime
    appointment: AppointmentVM | None = None

    @property
    def is_free(self) -> bool:
        return self.appointment is None


@dataclass(frozen=True)
class BookingChoiceVM:
    """The doctor and date chosen in steps 1–2 of online booking."""

    doctor_id: int
    doctor_name: str
    clinic_name: str
    day: date
    earliest_day: date
    latest_day: date  # today + 30 days (BR-002)
