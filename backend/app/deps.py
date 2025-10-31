from __future__ import annotations

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db import get_db
from app.core.services import StaffService, ScheduleService
from app.core.repositories import (
    SQLAlchemyStaffRepository,
    SQLAlchemyScheduleRepository,
)


def get_staff_service(db: Session = Depends(get_db)) -> StaffService:
    staff_repo = SQLAlchemyStaffRepository(db)
    schedule_repo = SQLAlchemyScheduleRepository(db)
    return StaffService(staff_repo, schedule_repo)


def get_schedule_service(db: Session = Depends(get_db)) -> ScheduleService:
    schedule_repo = SQLAlchemyScheduleRepository(db)
    staff_repo = SQLAlchemyStaffRepository(db)
    return ScheduleService(schedule_repo, staff_repo)
