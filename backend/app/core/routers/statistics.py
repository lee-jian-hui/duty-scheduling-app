from typing import List

from fastapi import APIRouter
from ..dto_models.statistics import StatisticRead


router = APIRouter(prefix="/api/statistics", tags=["statistics"])


@router.get("", response_model=List[StatisticRead])
def duty_counts() -> List[StatisticRead]:
    # Skeleton: to be implemented by service layer
    return []
