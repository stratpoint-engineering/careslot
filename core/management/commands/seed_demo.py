"""Idempotent demo data for local development: `uv run python manage.py seed_demo`.

Safe to run any number of times (get_or_create). Names are made up. Users get unusable passwords:
Day 0 sign-in is mocked; Day 1 sets real passwords.
"""

from datetime import time
from typing import Any

from django.core.management.base import BaseCommand
from django.db import transaction

from accounts.models import Patient, User
from core.roles import Role
from scheduling.models import Clinic, Doctor, Weekday, WorkingHours

CLINICS = ["Clinic A", "Clinic B", "Clinic C"]
DOCTORS = [
    ("Dr. Ana Reyes", "Clinic A"),
    ("Dr. Ben Lim", "Clinic B"),
    ("Dr. Carla Tan", "Clinic C"),
]
WEEKDAY_HOURS = (time(8), time(12))
PATIENTS = [
    ("Maria Santos", "maria.santos@example.com", "0917 000 0000"),
    ("Jose Bautista", "", "0918 000 0000"),
    ("Liza Ramos", "liza.ramos@example.com", ""),
]
USERS = [
    ("patient@example.com", "Maria Santos", Role.PATIENT),
    ("desk@example.com", "Joy Mendoza", Role.FRONT_DESK),
    ("doctor@example.com", "Dr. Ana Reyes", Role.DOCTOR),
    ("admin@example.com", "Clinic Admin", Role.CLINIC_ADMIN),
]


class Command(BaseCommand):
    help = (
        "Create demo clinics, doctors, working hours, patients and one user per role (idempotent)."
    )

    @transaction.atomic
    def handle(self, *args: Any, **options: Any) -> None:
        clinics = {name: Clinic.objects.get_or_create(name=name)[0] for name in CLINICS}
        users = {}
        for email, full_name, role in USERS:
            user, created = User.objects.get_or_create(
                email=email, defaults={"full_name": full_name, "role": role}
            )
            if created:
                user.set_unusable_password()
                user.save(update_fields=["password"])
            users[role] = user
        for full_name, clinic_name in DOCTORS:
            doctor, _ = Doctor.objects.get_or_create(
                full_name=full_name, defaults={"clinic": clinics[clinic_name]}
            )
            if full_name == "Dr. Ana Reyes" and doctor.user is None:
                doctor.user = users[Role.DOCTOR]
                doctor.save(update_fields=["user"])
            for weekday in (Weekday.MONDAY, Weekday.TUESDAY, Weekday.THURSDAY, Weekday.FRIDAY):
                WorkingHours.objects.get_or_create(
                    doctor=doctor,
                    weekday=weekday,
                    defaults={"start_time": WEEKDAY_HOURS[0], "end_time": WEEKDAY_HOURS[1]},
                )
        for full_name, email, phone in PATIENTS:
            Patient.objects.get_or_create(
                full_name=full_name, defaults={"email": email, "phone": phone}
            )
        patient = Patient.objects.get(full_name="Maria Santos")
        if patient.user is None:
            patient.user = users[Role.PATIENT]
            patient.save(update_fields=["user"])
        self.stdout.write(self.style.SUCCESS("Demo data ready."))
