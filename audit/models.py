"""Append-only access log (ADR-CARESLOT-E006-001; epic E006).

Every view or change of a patient's data writes one row: who, which patient, what, when.
The application's database role has INSERT and SELECT only; rows older than 5 years are deleted
by a separate scheduled job (NFR-SEC-004). Never update or delete rows from application code.
"""

from typing import ClassVar

from django.conf import settings
from django.db import models


class AuditAction(models.TextChoices):
    VIEW = "view", "View"
    CREATE = "create", "Create"
    UPDATE = "update", "Update"
    CANCEL = "cancel", "Cancel"


class AuditLog(models.Model):
    actor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="+")
    patient = models.ForeignKey("accounts.Patient", on_delete=models.PROTECT, related_name="+")
    action = models.CharField(max_length=10, choices=AuditAction.choices)
    object_type = models.CharField(max_length=50)
    object_id = models.CharField(max_length=50, blank=True)
    at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes: ClassVar = [models.Index(fields=["patient", "at"])]

    def __str__(self) -> str:
        return f"{self.at:%Y-%m-%d %H:%M} {self.actor_id} {self.action} patient {self.patient_id}"
