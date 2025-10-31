from typing import List

from fastapi import APIRouter, Depends
from ..dto_models.statistics import StatisticRead
from ..services import StatisticsService
from app.deps import get_statistics_service


router = APIRouter(prefix="/api/statistics", tags=["statistics"])


@router.get("", response_model=List[StatisticRead])
def duty_counts(svc: StatisticsService = Depends(get_statistics_service)) -> List[StatisticRead]:
    return svc.duty_counts()
