from django.db import models


class Role(models.TextChoices):
    """The four user roles (PRD personas; FR-AUTH-005)."""

    PATIENT = "patient", "Patient"
    FRONT_DESK = "front_desk", "Front desk"
    DOCTOR = "doctor", "Doctor"
    CLINIC_ADMIN = "clinic_admin", "Clinic admin"


# Where each role lands after sign-in (DES-002 notes).
HOME_URL_NAME: dict[str, str] = {
    Role.PATIENT: "my_appointments",
    Role.FRONT_DESK: "desk_day",
    Role.DOCTOR: "doctor_day",
    Role.CLINIC_ADMIN: "staff_accounts",
}
