import pandas as pd

from typing import List
from step import Step

class Route:
    def total_steps_distance(self) -> float: 
        return self.steps[-1].current_distance
    def total_steps_time(self) -> pd.Timedelta:
        return self.steps[-1].date - self.pickup_date
    # def total_volume(self):
    #     return ???
    def total_real_time(self) -> pd.Timedelta:
        return self.dropoff_date - self.pickup_date

    def __init__(self, pickup_date: pd.Timestamp, dropoff_date: pd.Timestamp, total_cost: float, total_distance: float, steps: List[Step]):
        self.pickup_date = pickup_date
        self.dropoff_date = dropoff_date
        self.total_cost = total_cost
        self.total_real_distance = total_distance
        self.steps = steps