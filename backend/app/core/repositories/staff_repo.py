from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional

from sqlalchemy import select, func, delete
from sqlalchemy.orm import Session

from ..models import Staff
from ..db_models.staff import StaffORM


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

    @abstractmethod
    def delete_all(self) -> None:
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

    def delete_all(self) -> None:
        self._items = []
        self._next_id = 1


class SQLAlchemyStaffRepository(StaffRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, staff: Staff) -> Staff:
        # Enforce unique by name (case-insensitive) similar to InMemory repo
        if self.exists_by_name(staff.name):
            raise ValueError("Staff with this name already exists")

        row = StaffORM(name=staff.name, age=staff.age, position=staff.position)
        self.session.add(row)
        self.session.commit()
        self.session.refresh(row)
        return Staff(id=row.id, name=row.name, age=row.age, position=row.position)

    def delete(self, staff_id: int) -> None:
        obj = self.session.get(StaffORM, staff_id)
        if obj is None:
            return
        self.session.delete(obj)
        self.session.commit()

    def list(self) -> List[Staff]:
        rows = self.session.execute(select(StaffORM)).scalars().all()
        return [Staff(id=r.id, name=r.name, age=r.age, position=r.position) for r in rows]

    def get(self, staff_id: int) -> Optional[Staff]:
        r = self.session.get(StaffORM, staff_id)
        if not r:
            return None
        return Staff(id=r.id, name=r.name, age=r.age, position=r.position)

    def exists_by_name(self, name: str) -> bool:
        needle = name.strip().lower()
        stmt = select(StaffORM.id).where(func.lower(StaffORM.name) == needle).limit(1)
        return self.session.execute(stmt).first() is not None

    def delete_all(self) -> None:
        self.session.execute(delete(StaffORM))
        self.session.commit()
