import pandas as pd

from src.utils import (
    MINUTES_THRESHOLD,
    N_TAXIS,
    TAXIS_CHOSEN_PICKLE,
    TAXIS_PICKLE,
    TRAFFIC_COUNT,
    TRAFFICS_CHOSEN_PICKLE,
    TRAFFICS_PICKLE,
)


def choose_traffic_days() -> None:
    traffic = pd.read_pickle(TRAFFICS_PICKLE)

    traffic_hours_count = traffic.groupby(["date"])
    counts = traffic_hours_count.count()
    chosen_traffics = counts[counts["street"] > TRAFFIC_COUNT]

    chosen_traffics.to_pickle(TRAFFICS_CHOSEN_PICKLE)


def extract_matched_taxis() -> None:
    chosen_traffics = pd.read_pickle(TRAFFICS_CHOSEN_PICKLE)
    taxis = pd.read_pickle(TAXIS_PICKLE)

    time_bias = pd.Timedelta(minutes=MINUTES_THRESHOLD)
    taxi_pickups = taxis["pickup_date"][0:N_TAXIS]
    indices = pd.Series([False] * len(taxi_pickups))
    for traffic_timestamp in chosen_traffics.index:
        indices = indices | ((traffic_timestamp - taxi_pickups).abs() < time_bias)

    chosen_taxis = taxis[0:N_TAXIS][indices]
    chosen_taxis.to_pickle(TAXIS_CHOSEN_PICKLE)


if __name__ == "__main__":
    choose_traffic_days()
    extract_matched_taxis()
