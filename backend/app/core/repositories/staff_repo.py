from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional

from ..models import Staff


class StaffRepository(ABC):
    @abstractmethod
    def add(self, staff: Staff) -> Staff:
        raise NotImplementedError

    @abstractmethod
    def delete(self, staff_id: int) -> None:
        raise NotImplementedError

    @abstractmethod
    def list(self) -> List[Staff]:
        raise NotImplementedError

    @abstractmethod
    def get(self, staff_id: int) -> Optional[Staff]:
        raise NotImplementedError

    @abstractmethod
    def exists_by_name(self, name: str) -> bool:
        raise NotImplementedError


class InMemoryStaffRepository(StaffRepository):
    def __init__(self) -> None:
        self._items: List[Staff] = []
        self._next_id: int = 1

    def add(self, staff: Staff) -> Staff:
        # Enforce name uniqueness (case-insensitive)
        if self.exists_by_name(staff.name):
            raise ValueError("Staff with this name already exists")

        # Assign ID if 0 or negative
        if staff.id <= 0:
            staff = Staff(id=self._next_id, name=staff.name, age=staff.age, position=staff.position)
        self._next_id = max(self._next_id, staff.id + 1)

        self._items.append(staff)
        return staff

    def delete(self, staff_id: int) -> None:
        self._items = [s for s in self._items if s.id != staff_id]

    def list(self) -> List[Staff]:
        return list(self._items)

    def get(self, staff_id: int) -> Optional[Staff]:
        for s in self._items:
            if s.id == staff_id:
                return s
        return None

    def exists_by_name(self, name: str) -> bool:
        needle = name.strip().lower()
        return any(s.name.strip().lower() == needle for s in self._items)

