# backend/core/dto_models/staff_dto.py
from uuid import uuid4
from pydantic import BaseModel, Field, conint
from datetime import datetime
from typing import Optional, List

"""Pydantic DTOs for Staff entities.

Domain model (core/models/staff.py) has fields: id:int, name:str, age:int, position:str.
DTOs mirror that, with create/update excluding id and read including id.
"""


# base DTO (shared fields, no id)
class StaffBase(BaseModel):
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
    id: int

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
