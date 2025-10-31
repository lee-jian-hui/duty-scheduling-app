from __future__ import annotations

from typing import List

from ..utils.logger import get_logger

from ..models import Staff
from ..repositories import StaffRepository, ScheduleRepository
from ..dto_models.staff import StaffCreate, StaffRead


logger = get_logger(__name__)

class StaffService:
    def __init__(self, staff_repo: StaffRepository, schedule_repo: ScheduleRepository) -> None:
        self.staff_repo = staff_repo
        self.schedule_repo = schedule_repo

    def list_staff(self) -> List[StaffRead]:
        items = self.staff_repo.list()
        return [StaffRead(id=s.id, name=s.name, age=s.age, position=s.position) for s in items]

    def add_staff(self, payload: StaffCreate) -> StaffRead:
        # Enforce unique name via repository
        if self.staff_repo.exists_by_name(payload.name):
            raise ValueError("duplicate_name")

        entity = Staff(id=0, name=payload.name, age=payload.age, position=payload.position)
        saved = self.staff_repo.add(entity)
        return StaffRead(id=saved.id, name=saved.name, age=saved.age, position=saved.position)

    def delete_staff(self, staff_id: int, *, force: bool = False) -> None:
        # Prevent deletion if staff has scheduled duties unless force is requested
        schedules = self.schedule_repo.list()
        if any(s.staff_id == staff_id for s in schedules):
            if not force:
                raise ValueError("has_duties")
            # Cascade: remove all duties for this staff first
            self.schedule_repo.delete_by_staff_id(staff_id)
        self.staff_repo.delete(staff_id)
