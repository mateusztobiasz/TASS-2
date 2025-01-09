from typing import Iterator, Tuple

import pandas as pd

from src.api_requester import send_request
from src.utils import TAXIS_CHOSEN_PICKLE


def get_taxis_coordinates() -> Iterator:
    chosen_taxis = pd.read_pickle(TAXIS_CHOSEN_PICKLE)
    pickup_coordinates = zip(
        chosen_taxis["Pickup_longitude"], chosen_taxis["Pickup_latitude"]
    )
    dropoffs_coordinates = zip(
        chosen_taxis["Dropoff_longitude"], chosen_taxis["Dropoff_latitude"]
    )

    return zip(pickup_coordinates, dropoffs_coordinates)


def extract_taxi_path(taxi_coordinate: Tuple[Tuple[float]]) -> list:
    response = send_request(taxi_coordinate, steps="true", tidy="true", waypoints="0;1")
    json_response = response.json()

    return json_response["matchings"][0]["legs"][0]["steps"]


if __name__ == "__main__":
    taxis_coordinates = get_taxis_coordinates()
    steps = extract_taxi_path(next(taxis_coordinates))
    print(steps)
