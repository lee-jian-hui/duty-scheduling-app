from __future__ import annotations

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class DutyScheduleORM(Base):
    __tablename__ = "duty_schedule"

    # Composite primary key: (date, staff_id)
    # date stored as ISO string YYYY-MM-DD to align with existing domain
    date: Mapped[str] = mapped_column(String(10), primary_key=True)
    staff_id: Mapped[int] = mapped_column(Integer, primary_key=True)
