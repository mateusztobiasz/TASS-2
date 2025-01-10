from typing import Iterator, Tuple

import pandas as pd
import pickle as pkl
import time

from src.api_requester import send_request
from src.utils import TAXIS_CHOSEN_PICKLE, TAXIS_STEPS_PICKLE


def get_taxis_coordinates() -> Iterator:
    chosen_taxis = pd.read_pickle(TAXIS_CHOSEN_PICKLE)
    pickup_coordinates = zip(
        chosen_taxis["Pickup_longitude"], chosen_taxis["Pickup_latitude"]
    )
    dropoffs_coordinates = zip(
        chosen_taxis["Dropoff_longitude"], chosen_taxis["Dropoff_latitude"]
    )

    return zip(pickup_coordinates, dropoffs_coordinates)


def extract_taxi_path(taxi_coordinate: Tuple[Tuple[float]], index: int) -> list:
    response = send_request(taxi_coordinate, steps="true", tidy="true", waypoints="0;1")
    json_response = response.json()

    if response.status_code != 200:
        print(f'HTTP ERROR: Request nr {index} for taxi route coordinates: {taxi_coordinate} has ended with error code {response.status_code}')

        if "message" in json_response:
            print(f'\tmessage: {json_response["message"]}')
        
        return list()

    if "matchings" not in json_response:
        print(f'ERROR: Request nr {index} for taxi route coordinates: {taxi_coordinate} has returned no matchings')

        if "message" in json_response:
            print(f'\tmessage: {json_response["message"]}')
        
        return list()

    if len(json_response["matchings"]) == 0 or "legs" not in json_response["matchings"][0] or len(json_response["matchings"][0]["legs"]) == 0:
        return list()

    return json_response["matchings"][0]["legs"][0]["steps"]


if __name__ == "__main__":
    # taxis_coordinates = get_taxis_coordinates()

    # i = 0
    # taxis_steps = []
    # for coordinates in taxis_coordinates:
    #     taxis_steps.append(extract_taxi_path(coordinates, i))
    #     i = i + 1
    #     if i == 300: # API is limited to 300 request per minute
    #         i = 0
    #         print('waiting...')
    #         time.sleep(61)

    # with open(TAXIS_STEPS_PICKLE, 'wb') as f:
    #     pkl.dump(taxis_steps, f)

    with open(TAXIS_STEPS_PICKLE, 'rb') as f:
        taxis_steps = pkl.load(f)

    