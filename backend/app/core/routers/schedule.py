from typing import List

from fastapi import APIRouter, HTTPException, Depends

from ..dto_models.schedule import ScheduleCreate, ScheduleRead, ScheduleDeleteResponse
from ..services import ScheduleService
from app.deps import get_schedule_service

router = APIRouter(prefix="/api/schedule", tags=["schedule"])


@router.get("", response_model=List[ScheduleRead])
def list_schedule(svc: ScheduleService = Depends(get_schedule_service)) -> List[ScheduleRead]:
    return svc.list_schedule()


@router.post("", response_model=ScheduleRead, status_code=201)
def assign_duty(payload: ScheduleCreate, svc: ScheduleService = Depends(get_schedule_service)) -> ScheduleRead:
    try:
        return svc.assign(payload)
    except ValueError as e:
        if str(e) == "staff_not_found":
            raise HTTPException(status_code=400, detail="Staff not found")
        # Repo may raise error if date already assigned
        if str(e).startswith("A duty is already assigned"):
            raise HTTPException(status_code=409, detail="Duty already assigned for date")
        raise


@router.delete("/{date}", response_model=ScheduleDeleteResponse)
def delete_duty(date: str, svc: ScheduleService = Depends(get_schedule_service)) -> ScheduleDeleteResponse:
    # Expecting date in YYYY-MM-DD format
    try:
        svc.delete_by_date(date)
    except Exception:
        # For now, ignore missing entry and respond deleted True to keep idempotency
        pass
    return ScheduleDeleteResponse(deleted=True)
