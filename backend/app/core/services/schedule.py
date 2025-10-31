from __future__ import annotations

from typing import List
from datetime import datetime

from ..models import DutySchedule
from ..repositories import ScheduleRepository, StaffRepository
from ..dto_models.schedule import (
    ScheduleCreate,
    ScheduleRead,
)


class ScheduleService:
    def __init__(self, schedule_repo: ScheduleRepository, staff_repo: StaffRepository) -> None:
        self.schedule_repo = schedule_repo
        self.staff_repo = staff_repo

    def list_schedule(self) -> List[ScheduleRead]:
        items = self.schedule_repo.list()
        # Map domain model (date str) to DTO (datetime)
        result: List[ScheduleRead] = []
        for it in items:
            dt = datetime.fromisoformat(it.date)
            # Provide a transient UUID for read if missing; routers don't require it strictly
            result.append(ScheduleRead(id="", date=dt, staff_id=it.staff_id))
        return result

    def assign(self, payload: ScheduleCreate) -> ScheduleRead:
        # Validate staff exists
        staff = self.staff_repo.get(payload.staff_id)
        if not staff:
            raise ValueError("staff_not_found")

        # Convert date to YYYY-MM-DD string
        date_str = payload.date.date().isoformat()

        entity = DutySchedule(date=date_str, staff_id=payload.staff_id)
        saved = self.schedule_repo.add(entity)
        return ScheduleRead(id=payload.id, date=payload.date, staff_id=saved.staff_id)

    def delete_by_date(self, date_str: str) -> None:
        self.schedule_repo.delete_by_date(date_str)
