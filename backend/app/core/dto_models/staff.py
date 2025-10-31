# backend/core/dto_models/staff_dto.py
from uuid import uuid4
from pydantic import BaseModel, Field, conint
from datetime import datetime
from typing import Optional, List

# base DTO
class StaffBase(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()), description="Unique staff ID (UUID4)")
    date: datetime = Field(..., description="Duty date (YYYY-MM-DD)")
    name: str = Field(..., min_length=1, description="Staff full name")
    age: conint(ge=16, le=80)  # type: ignore[valid-type]
    position: str = Field(..., min_length=1, description="Job position title")

    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# CRUD DTOs — shared fields for all Staff models
# ---------------------------------------------------------------------------

class StaffCreate(StaffBase):
    """Payload for creating a new staff record."""
    pass


class StaffUpdate(StaffBase):
    """Partial update of existing staff record."""
    pass

class StaffRead(StaffBase):
    """Represents staff data returned by the API."""
    pass

class StaffDeleteResponse(BaseModel):
    """Response returned after successful deletion."""
    deleted: bool = True


# ---------------------------------------------------------------------------
# Aggregated Response DTOs
# ---------------------------------------------------------------------------
class StaffListResponse(BaseModel):
    """Response wrapper for staff listing endpoints."""
    total: int
    data: List[StaffRead]


class StaffCreateResponse(StaffRead):
    """Response returned after creation (identical to StaffRead)."""
    message: str = "Staff record created successfully"
