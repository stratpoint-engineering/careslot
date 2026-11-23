"""Users and patients (ARCH-CARESLOT-v1 §5; epic E001)."""

from typing import Any, ClassVar

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone

from core.roles import Role


class UserManager(BaseUserManager["User"]):
    use_in_migrations = True

    def create_user(self, email: str, password: str | None = None, **extra: Any) -> "User":
        if not email:
            raise ValueError("Email is required")
        user = self.model(email=self.normalize_email(email).lower(), **extra)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email: str, password: str | None = None, **extra: Any) -> "User":
        extra.update(is_staff=True, is_superuser=True, role=Role.CLINIC_ADMIN)
        return self.create_user(email, password, **extra)


class User(AbstractBaseUser, PermissionsMixin):
    """Anyone who signs in: patient, front desk, doctor or clinic admin (FR-AUTH-001, FR-AUTH-005)."""

    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=200)
    role = models.CharField(max_length=20, choices=Role.choices)
    is_active = models.BooleanField(default=True)  # FR-ADMIN-001: disabled accounts can't sign in
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects: ClassVar[UserManager] = UserManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS: ClassVar[list[str]] = ["full_name"]

    def __str__(self) -> str:
        return self.email


class Patient(models.Model):
    """A patient record. Front desk can create one without an online account (FR-DESK-002),
    so `user` is optional. Linking a later self-registration is open (PRD Open Question 3)."""

    full_name = models.CharField(max_length=200)
    email = models.EmailField(blank=True)  # needed for the reminder email (FR-NOTIF-001)
    phone = models.CharField(max_length=40, blank=True)
    user = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.PROTECT, related_name="patient"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes: ClassVar = [models.Index(fields=["email"]), models.Index(fields=["full_name"])]

    def __str__(self) -> str:
        return self.full_name
