from typing import List

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field, conint

from backend.models.staff import StaffCreate, StaffRead





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

