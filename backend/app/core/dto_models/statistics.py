from pydantic import BaseModel


class StatisticRead(BaseModel):
    staff_id: int
    count: int
