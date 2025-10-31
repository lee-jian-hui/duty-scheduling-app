from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

from sqlalchemy import select
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
        # Ensure only one assignment per date
        if any(item.date == schedule.date for item in self._items):
            raise ValueError("A duty is already assigned for this date")
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
            # Keep message consistent with InMemory repo to preserve handlers
            raise ValueError("A duty is already assigned for this date")
        return DutySchedule(date=row.date, staff_id=row.staff_id)

    def list(self) -> List[DutySchedule]:
        rows = self.session.execute(select(DutyScheduleORM)).scalars().all()
        return [DutySchedule(date=r.date, staff_id=r.staff_id) for r in rows]

    def delete_by_date(self, date_str: str) -> None:
        obj = self.session.get(DutyScheduleORM, date_str)
        if obj is None:
            return
        self.session.delete(obj)
        self.session.commit()
