from dataclasses import dataclass


@dataclass
class DutySchedule:
    # Store ISO date string (YYYY-MM-DD) for simplicity
    date: str
    staff_id: int

