from dataclasses import dataclass

from core.roles import Role


@dataclass(frozen=True)
class StaffAccountVM:
    """One row of DES-003 Staff accounts."""

    id: int
    full_name: str
    email: str
    role: Role
    clinic_name: str = ""  # doctors only
    is_active: bool = True

    @property
    def role_label(self) -> str:
        return self.role.label
