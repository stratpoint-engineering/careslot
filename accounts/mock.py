"""Day 0 sample data for E001 screens. Day 1 replaces these functions with real queries
returning the same view-models. All names are made up."""

from accounts.viewmodels import StaffAccountVM
from core.roles import Role
from core.viewmodels import Option


def staff_accounts() -> list[StaffAccountVM]:
    return [
        StaffAccountVM(1, "Joy Mendoza", "joy@clinic.example", Role.FRONT_DESK),
        StaffAccountVM(2, "Dr. Ana Reyes", "ana.reyes@clinic.example", Role.DOCTOR, "Clinic A"),
        StaffAccountVM(3, "Carlo Dizon", "carlo@clinic.example", Role.FRONT_DESK, is_active=False),
    ]


def staff_role_options() -> list[Option]:
    return [
        Option(r.value, str(r.label)) for r in (Role.FRONT_DESK, Role.DOCTOR, Role.CLINIC_ADMIN)
    ]


def clinic_options() -> list[Option]:
    return [Option("1", "Clinic A"), Option("2", "Clinic B"), Option("3", "Clinic C")]
