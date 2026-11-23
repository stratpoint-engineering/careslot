"""Day 0 sample data for E004 screens (names and dates made up)."""

from datetime import date

from patient_portal.mock import SAMPLE_DAY, at
from patient_portal.viewmodels import AppointmentVM, SlotVM
from staff_portal.viewmodels import DoctorDayVM, PatientVM


def _booked(
    appt_id: int, day: date, h: int, m: int, patient: str, reason: str, doctor: str, clinic: str
) -> SlotVM:
    starts = at(day, h, m)
    return SlotVM(
        starts, AppointmentVM(appt_id, starts, doctor, clinic, patient_name=patient, reason=reason)
    )


def desk_day() -> list[DoctorDayVM]:
    d = SAMPLE_DAY
    return [
        DoctorDayVM(
            1,
            "Dr. Ana Reyes",
            "Clinic A",
            d,
            (
                _booked(
                    1, d, 8, 0, "Maria Santos", "Cough for two weeks", "Dr. Ana Reyes", "Clinic A"
                ),
                SlotVM(at(d, 8, 20)),
                _booked(
                    2,
                    d,
                    8,
                    40,
                    "Jose Bautista (walk-in)",
                    "Blood pressure check",
                    "Dr. Ana Reyes",
                    "Clinic A",
                ),
                SlotVM(at(d, 9, 0)),
            ),
        ),
        DoctorDayVM(
            2,
            "Dr. Ben Lim",
            "Clinic B",
            d,
            (
                SlotVM(at(d, 8, 0)),
                _booked(3, d, 8, 20, "Liza Ramos", "Follow-up", "Dr. Ben Lim", "Clinic B"),
                SlotVM(at(d, 8, 40)),
            ),
        ),
        DoctorDayVM(3, "Dr. Carla Tan", "Clinic C", d, working=False),
    ]


def doctor_day() -> DoctorDayVM:
    d = SAMPLE_DAY
    doctor, clinic = "Dr. Ana Reyes", "Clinic A"
    return DoctorDayVM(
        1,
        doctor,
        clinic,
        d,
        (
            _booked(1, d, 8, 0, "Maria Santos", "Cough for two weeks", doctor, clinic),
            _booked(2, d, 8, 40, "Jose Bautista", "Blood pressure check", doctor, clinic),
            _booked(4, d, 10, 20, "Ana Cruz", "Follow-up on lab results", doctor, clinic),
        ),
    )


def patient_search_results() -> list[PatientVM]:
    return [PatientVM(1, "Maria Santos", "maria.santos@example.com", "0917 000 0000")]


def appointment(appointment_id: int) -> AppointmentVM | None:
    for day in desk_day():
        for appt in day.appointments:
            if appt.id == appointment_id:
                return appt
    return None


def move_slots() -> list[SlotVM]:
    d = date(2027, 10, 13)
    return [SlotVM(at(d, 8, 20)), SlotVM(at(d, 9, 40)), SlotVM(at(d, 10, 0))]
