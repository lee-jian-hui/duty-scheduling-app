from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List

from ..models import DutySchedule


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

