from pydantic import BaseModel, Field


class ScheduleCreate(BaseModel):
    date: str = Field(..., regex=r"^\d{4}-\d{2}-\d{2}$")
    # date: str = Field(..., regex=r"^\d{4}-\d{2}-\d{2}$")
    staff_id: int


class ScheduleRead(ScheduleCreate):
    pass
