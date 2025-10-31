from typing import List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, conint


class StaffCreate(BaseModel):
    name: str = Field(..., min_length=1)
    age: conint(ge=16, le=80)  # type: ignore[valid-type]
    position: str = Field(..., min_length=1)


class StaffRead(StaffCreate):
    id: int


router = APIRouter(prefix="/api/staff", tags=["staff"])


@router.get("", response_model=List[StaffRead])
def list_staff() -> List[StaffRead]:
    # Skeleton: to be implemented by service layer
    return []


@router.post("", response_model=StaffRead, status_code=201)
def add_staff(payload: StaffCreate) -> StaffRead:
    # Skeleton: to be implemented by service layer
    raise HTTPException(status_code=501, detail="Not implemented: add_staff service binding")


@router.delete("/{staff_id}")
def delete_staff(staff_id: int) -> dict:
    # Skeleton: to be implemented by service layer
    raise HTTPException(status_code=501, detail="Not implemented: delete_staff service binding")

