from typing import List

from fastapi import APIRouter, HTTPException, Depends

from ..dto_models.staff import StaffCreate, StaffRead
from ..services import StaffService
from app.deps import get_staff_service





router = APIRouter(prefix="/api/staff", tags=["staff"])


@router.get("", response_model=List[StaffRead])
def list_staff(svc: StaffService = Depends(get_staff_service)) -> List[StaffRead]:
    return svc.list_staff()


@router.post("", response_model=StaffRead, status_code=201)
def add_staff(payload: StaffCreate, svc: StaffService = Depends(get_staff_service)) -> StaffRead:
    try:
        return svc.add_staff(payload)
    except ValueError as e:
        if str(e) == "duplicate_name":
            raise HTTPException(status_code=409, detail="Staff name already exists")
        raise


@router.delete("/{staff_id}")
def delete_staff(staff_id: int, svc: StaffService = Depends(get_staff_service)) -> dict:
    try:
        svc.delete_staff(staff_id)
        return {"deleted": True}
    except ValueError as e:
        if str(e) == "has_duties":
            raise HTTPException(status_code=409, detail="Cannot delete staff with assigned duties")
        raise
