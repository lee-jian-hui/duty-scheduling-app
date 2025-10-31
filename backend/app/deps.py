from __future__ import annotations

from app.core.services import StaffService, ScheduleService
from app.core.repositories import (
    InMemoryStaffRepository,
    InMemoryScheduleRepository,
)

# Shared in-memory repositories for the app lifecycle
_staff_repo = InMemoryStaffRepository()
_schedule_repo = InMemoryScheduleRepository()


def get_staff_service() -> StaffService:
    return StaffService(_staff_repo, _schedule_repo)


def get_schedule_service() -> ScheduleService:
    return ScheduleService(_schedule_repo, _staff_repo)
