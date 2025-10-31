from pydantic import BaseModel, Field


class StaffCreate(BaseModel):
    name: str = Field(..., min_length=1)
    age: conint(ge=16, le=80)  # type: ignore[valid-type]
    position: str = Field(..., min_length=1)


class StaffRead(StaffCreate):
    id: int