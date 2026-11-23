from dataclasses import dataclass
from datetime import date

from patient_portal.viewmodels import AppointmentVM, SlotVM


@dataclass(frozen=True)
class DoctorDayVM:
    """One doctor's card on the front-desk day view (DES-009) or the doctor's own list (DES-012)."""

    doctor_id: int
    doctor_name: str
    clinic_name: str
    day: date
    slots: tuple[SlotVM, ...] = ()
    working: bool = True

    @property
    def appointments(self) -> tuple[AppointmentVM, ...]:
        return tuple(s.appointment for s in self.slots if s.appointment is not None)


@dataclass(frozen=True)
class PatientVM:
    """A patient record as the front desk sees it (DES-010)."""

    id: int
    full_name: str
    email: str = ""
    phone: str = ""
