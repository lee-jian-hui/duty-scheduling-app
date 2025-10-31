from .staff import router as staff_router
from .schedule import router as schedule_router
from .statistics import router as statistics_router

__all__ = [
    "staff_router",
    "schedule_router",
    "statistics_router",
]

