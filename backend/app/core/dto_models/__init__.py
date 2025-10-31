from .staff import router as staff_dto
from .schedule import router as schedule_dto
from .statistics import router as statistics_dto

__all__ = [
    "staff_dto",
    "schedule_dto",
    "statistics_dto",
]

