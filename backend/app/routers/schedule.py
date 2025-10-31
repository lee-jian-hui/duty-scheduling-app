from typing import List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field


class ScheduleCreate(BaseModel):
    date: str = Field(..., regex=r"^\d{4}-\d{2}-\d{2}$")
    staff_id: int


class ScheduleRead(ScheduleCreate):
    pass


router = APIRouter(prefix="/api/schedule", tags=["schedule"])


@router.get("", response_model=List[ScheduleRead])
def list_schedule() -> List[ScheduleRead]:
    # Skeleton: to be implemented by service layer
    return []


@router.post("", response_model=ScheduleRead, status_code=201)
def assign_duty(payload: ScheduleCreate) -> ScheduleRead:
    # Skeleton: to be implemented by service layer
    raise HTTPException(status_code=501, detail="Not implemented: assign_duty service binding")


