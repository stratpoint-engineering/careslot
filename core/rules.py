"""Business numbers, each next to the rule it implements. Change a number only with a change request.

These are constants, not settings: they are the same in every environment.
"""

from datetime import time, timedelta

SLOT_LENGTH = timedelta(minutes=20)  # BR-005, FR-BOOK-003
ONLINE_BOOKING_WINDOW = timedelta(days=30)  # BR-002, FR-BOOK-002
MAX_FUTURE_APPOINTMENTS = 2  # BR-003, FR-BOOK-006 (every channel, no override)
ONLINE_CANCEL_CUTOFF = timedelta(hours=2)  # BR-006, FR-APPT-002
REMINDER_SEND_TIME = time(18, 0)  # BR-008, FR-NOTIF-001: 18:00 on the day before
LOCKOUT_FAILURE_LIMIT = 5  # BR-017, NFR-SEC-002
LOCKOUT_DURATION = timedelta(minutes=15)  # BR-017, NFR-SEC-002
IDLE_SIGN_OUT = timedelta(minutes=30)  # BR-018, NFR-SEC-003
AUDIT_LOG_RETENTION_YEARS = 5  # BR-015, NFR-SEC-004
