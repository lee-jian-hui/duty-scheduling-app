from typing import List

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import StreamingResponse
import io

from ..dto_models.schedule import (
    ScheduleCreate,
    ScheduleDeleteResponse,
    ScheduleRead,
    ScheduleUpdateRequest,
    IntelligentScheduleRequest,
    ScheduleWipeResponse,
)
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


@router.put("/{date}", response_model=ScheduleRead)
def replace_duty(date: str, payload: ScheduleUpdateRequest, svc: ScheduleService = Depends(get_schedule_service)) -> ScheduleRead:
    try:
        return svc.replace_for_date(date, payload.staff_id)
    except ValueError as e:
        if str(e) == "staff_not_found":
            raise HTTPException(status_code=400, detail="Staff not found")
        raise


@router.get("/export")
def export_schedule(svc: ScheduleService = Depends(get_schedule_service)) -> StreamingResponse:
    data = svc.export_csv()
    return StreamingResponse(
        io.BytesIO(data),
        media_type="text/csv",
        headers={
            "Content-Disposition": 'attachment; filename="schedule.csv"'
        },
    )


@router.post("/intelligent-schedule", response_model=List[ScheduleRead])
def intelligent_schedule(payload: IntelligentScheduleRequest, svc: ScheduleService = Depends(get_schedule_service)) -> List[ScheduleRead]:
    try:
        start = payload.start_date.date()
        end = payload.end_date.date()
        return svc.generate_round_robin(start, end)
    except ValueError as e:
        if str(e) == "invalid_range":
            raise HTTPException(status_code=400, detail="Invalid date range")
        if str(e) == "no_staff":
            raise HTTPException(status_code=400, detail="No staff available")
        raise


@router.delete("", response_model=ScheduleWipeResponse)
def wipe_all(svc: ScheduleService = Depends(get_schedule_service)) -> ScheduleWipeResponse:
    svc.wipe_all()
    return ScheduleWipeResponse(deleted=True)
