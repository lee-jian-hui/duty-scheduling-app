from __future__ import annotations

from typing import Dict, List

from ..repositories import ScheduleRepository
from ..dto_models.statistics import StatisticRead


class StatisticsService:
    def __init__(self, schedule_repo: ScheduleRepository) -> None:
        self.schedule_repo = schedule_repo

    def duty_counts(self) -> List[StatisticRead]:
        items = self.schedule_repo.list()
        counts: Dict[int, int] = {}
        for it in items:
            counts[it.staff_id] = counts.get(it.staff_id, 0) + 1
        return [StatisticRead(staff_id=sid, count=cnt) for sid, cnt in counts.items()]

