import pandas as pd

class Step:
    volume: int | None = None

    def __init__(self, date: pd.Timestamp, current_distance: float, street: str):
        self.date = date
        self.current_distance = current_distance
        self.street = street