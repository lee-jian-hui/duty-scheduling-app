from __future__ import annotations

from typing import List
from datetime import datetime, date, timedelta
import csv
import io

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

    def replace_for_date(self, date_str: str, staff_id: int) -> ScheduleRead:
        # Validate staff exists
        staff = self.staff_repo.get(staff_id)
        if not staff:
            raise ValueError("staff_not_found")

        # Replace existing assignments for date with the new one
        self.schedule_repo.delete_by_date(date_str)
        entity = DutySchedule(date=date_str, staff_id=staff_id)
        saved = self.schedule_repo.add(entity)
        dt = datetime.fromisoformat(saved.date)
        return ScheduleRead(id="", date=dt, staff_id=saved.staff_id)

    def wipe_all(self) -> None:
        self.schedule_repo.delete_all()

    def generate_round_robin(self, start: date, end: date) -> List[ScheduleRead]:
        # Validate input range
        if end < start:
            raise ValueError("invalid_range")

        staff_list = self.staff_repo.list()
        if not staff_list:
            raise ValueError("no_staff")

        # Deterministic order by id, then name
        staff_list = sorted(staff_list, key=lambda s: (s.id, s.name))

        out: List[ScheduleRead] = []
        day = start
        idx = 0
        while day <= end:
            date_str = day.isoformat()
            # Replace any existing assignment for the date
            self.schedule_repo.delete_by_date(date_str)
            staff = staff_list[idx % len(staff_list)]
            saved = self.schedule_repo.add(DutySchedule(date=date_str, staff_id=staff.id))
            out.append(ScheduleRead(id="", date=datetime.fromisoformat(saved.date), staff_id=saved.staff_id))
            idx += 1
            day += timedelta(days=1)
        return out

    def export_csv(self) -> bytes:
        # Collect schedules ordered by date
        items = sorted(self.schedule_repo.list(), key=lambda x: x.date)
        buf = io.StringIO()
        writer = csv.writer(buf)
        writer.writerow(["date", "staff_id", "staff_name"])  # header
        for it in items:
            staff = self.staff_repo.get(it.staff_id)
            name = staff.name if staff else ""
            writer.writerow([it.date, it.staff_id, name])
        data = buf.getvalue().encode("utf-8")
        buf.close()
        return data
