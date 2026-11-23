from dataclasses import dataclass
from datetime import time


@dataclass(frozen=True)
class WorkingDayVM:
    """One weekday row of DES-004 Working hours. start/end None = not working that day."""

    weekday: int
    label: str
    start: time | None = None
    end: time | None = None
    error: str = ""
