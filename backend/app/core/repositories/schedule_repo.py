from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ..models import DutySchedule
from ..db_models.schedule import DutyScheduleORM


class ScheduleRepository(ABC):
    @abstractmethod
    def add(self, schedule: DutySchedule) -> DutySchedule:
        raise NotImplementedError

    @abstractmethod
    def list(self) -> List[DutySchedule]:
        raise NotImplementedError

    @abstractmethod
    def delete_by_date(self, date_str: str) -> None:
        raise NotImplementedError


class InMemoryScheduleRepository(ScheduleRepository):
    def __init__(self) -> None:
        self._items: List[DutySchedule] = []

    def add(self, schedule: DutySchedule) -> DutySchedule:
        # Enforce single assignment per date globally
        if any(item.date == schedule.date for item in self._items):
            raise ValueError("duplicate_assignment")
        self._items.append(schedule)
        return schedule

    def list(self) -> List[DutySchedule]:
        return list(self._items)

    def delete_by_date(self, date_str: str) -> None:
        self._items = [item for item in self._items if item.date != date_str]


class SQLAlchemyScheduleRepository(ScheduleRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, schedule: DutySchedule) -> DutySchedule:
        row = DutyScheduleORM(date=schedule.date, staff_id=schedule.staff_id)
        self.session.add(row)
        try:
            self.session.commit()
        except IntegrityError:
            self.session.rollback()
            # Duplicate assignment for the same (date, staff_id)
            raise ValueError("duplicate_assignment")
        return DutySchedule(date=row.date, staff_id=row.staff_id)

    def list(self) -> List[DutySchedule]:
        rows = self.session.execute(select(DutyScheduleORM)).scalars().all()
        return [DutySchedule(date=r.date, staff_id=r.staff_id) for r in rows]

    def delete_by_date(self, date_str: str) -> None:
        # Delete all assignments on the given date
        self.session.execute(delete(DutyScheduleORM).where(DutyScheduleORM.date == date_str))
        self.session.commit()
