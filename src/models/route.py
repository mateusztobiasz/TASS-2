from functools import reduce
from typing import List

import pandas as pd

from src.models.step import Step


class Route:
    def __init__(
        self,
        pickup_date: pd.Timestamp,
        dropoff_date: pd.Timestamp,
        total_cost: float,
        total_distance: float,
        steps: List[Step],
    ):
        self.pickup_date = pickup_date
        self.dropoff_date = dropoff_date
        self.total_cost = (total_cost,)
        self.total_real_distance = total_distance
        self.steps = steps

    def total_steps_distance(self) -> float:
        return self.steps[-1].current_distance

    def total_steps_time(self) -> pd.Timedelta:
        return self.steps[-1].date - self.pickup_date

    def total_volume(self) -> float:
        return reduce(
            lambda acc, cur: acc + cur.volume if cur.volume is not None else acc,
            self.steps,
            0,
        )

    def total_real_time(self) -> pd.Timedelta:
        return self.dropoff_date - self.pickup_date
