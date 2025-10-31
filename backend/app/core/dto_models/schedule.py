from uuid import uuid4
from pydantic import BaseModel, Field
from datetime import datetime
from typing import List


# Base DTO
class ScheduleBase(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()), description="Unique schedule ID (UUID4)")
    date: datetime = Field(..., description="Duty date (YYYY-MM-DD)")
    staff_id: int = Field(..., description="Assigned staff ID")

    # Enable attribute-based validation for future ORM compatibility
    model_config = {"from_attributes": True}


# CRUD DTOs — shared fields for all Schedule models
class ScheduleCreate(ScheduleBase):
    """Payload for creating a new schedule record."""
    pass


class ScheduleUpdate(ScheduleBase):
    """Payload for updating an existing schedule record."""
    pass


class ScheduleRead(ScheduleBase):
    """Represents schedule data returned by the API."""
    pass


class ScheduleDeleteResponse(BaseModel):
    """Response returned after successful deletion."""
    deleted: bool = True


# Aggregated Response DTOs
class ScheduleListResponse(BaseModel):
    """Response wrapper for schedule listing endpoints."""
    total: int
    data: List[ScheduleRead]


class ScheduleCreateResponse(ScheduleRead):
    """Response returned after creation (identical to ScheduleRead)."""
    message: str = "Schedule record created successfully"
