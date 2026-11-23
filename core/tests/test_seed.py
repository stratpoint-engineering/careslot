import pytest
from django.core.management import call_command

from accounts.models import Patient, User
from scheduling.models import Clinic, Doctor, WorkingHours

pytestmark = pytest.mark.django_db


def counts() -> tuple[int, ...]:
    return (
        Clinic.objects.count(),
        Doctor.objects.count(),
        WorkingHours.objects.count(),
        Patient.objects.count(),
        User.objects.count(),
    )


def test_seed_is_idempotent() -> None:
    call_command("seed_demo")
    first = counts()
    call_command("seed_demo")
    assert counts() == first == (3, 3, 12, 3, 4)
    assert not User.objects.get(email="desk@example.com").has_usable_password()
