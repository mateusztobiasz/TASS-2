import os
import pickle as pkl
import time
from typing import Iterator, List, Tuple

import pandas as pd

from src.api_requester import send_request
from src.models.route import Route
from src.models.step import Step
from src.utils import (
    MINUTES_THRESHOLD,
    ROUTES_PICKLE,
    TAXIS_CHOSEN_FULL_PICKLE,
    TAXIS_CHOSEN_PICKLE,
    TAXIS_STEPS_PICKLE,
    TRAFFICS_PICKLE,
)


def get_taxis_coordinates() -> Iterator:
    chosen_taxis = pd.read_pickle(TAXIS_CHOSEN_FULL_PICKLE)[:20000]
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
        print(
            f"HTTP ERROR: Request nr {index} for taxi route coordinates: {taxi_coordinate} has ended with error code {response.status_code}"
        )

        if "message" in json_response:
            print(f'\tmessage: {json_response["message"]}')

        return list()

    if "matchings" not in json_response:
        print(
            f"ERROR: Request nr {index} for taxi route coordinates: {taxi_coordinate} has returned no matchings"
        )

        if "message" in json_response:
            print(f'\tmessage: {json_response["message"]}')

        return list()

    if (
        len(json_response["matchings"]) == 0
        or "legs" not in json_response["matchings"][0]
        or len(json_response["matchings"][0]["legs"]) == 0
    ):
        return list()

    return json_response["matchings"][0]["legs"][0]["steps"]


def normalize_street(street: str) -> str:
    return (
        street.lower()
        .replace("1st", "1")
        .replace("2nd", "2")
        .replace("3rd", "3")
        .replace("1th", "1")
        .replace("2th", "2")
        .replace("3th", "3")
        .replace("4th", "4")
        .replace("5th", "5")
        .replace("6th", "6")
        .replace("7th", "7")
        .replace("8th", "8")
        .replace("9th", "9")
        .replace("0th", "0")
        .replace(" ", "")
    )


def extract_step_info(step: dict, distance: float, time: pd.Timestamp):
    if "duration" in step:
        time = time + pd.Timedelta(seconds=step["duration"])

    if "distance" in step:
        distance = distance + step["distance"]

    if "name" in step and step["name"] != "":
        street = step["name"]
        return Step(time, distance, normalize_street(street))
    else:
        return Step(time, distance, None)


def get_taxis_steps() -> None:
    taxis_coordinates = get_taxis_coordinates()

    i = 0
    taxis_steps = []
    for coordinates in taxis_coordinates:
        taxis_steps.append(extract_taxi_path(coordinates, i))
        i = i + 1
        # if i == 300:  # API is limited to 300 request per minute
        #     i = 0
        #     print("waiting...")
        #     time.sleep(61)

    with open(TAXIS_STEPS_PICKLE, "wb") as f:
        pkl.dump(taxis_steps, f)


def get_taxis_routes() -> None:
    with open(TAXIS_STEPS_PICKLE, "rb") as f:
        taxis_steps = pkl.load(f)

    taxis = pd.read_pickle(TAXIS_CHOSEN_FULL_PICKLE)[:20000]

    traffics = pd.read_pickle(TRAFFICS_PICKLE)

    taxis_routes: List[Route] = list()
    for taxi, route in zip(taxis.itertuples(), taxis_steps):
        steps_info = list()
        cur_time = taxi.pickup_date
        cur_distance = 0.0

        for step in route:
            step_info = extract_step_info(step, cur_distance, cur_time)
            cur_time = step_info.date
            cur_distance = step_info.current_distance
            steps_info.append(step_info)

        taxis_routes.append(
            Route(
                taxi.pickup_date,
                taxi.dropoff_date,
                taxi.Total_cost,
                taxi.Trip_distance * 1609.344,
                steps_info,
            )
        )

    assign_volumes(taxis_routes, traffics)


def assign_volumes(taxis_routes: List[Route], traffics: pd.DataFrame) -> None:
    streets = traffics["street"].apply(lambda s: normalize_street(s))

    for taxi_route in taxis_routes:
        for step in taxi_route.steps:
            if step.street == None:
                continue

            filtered = traffics[
                (
                    (traffics["date"] - step.date).abs()
                    < pd.Timedelta(minutes=MINUTES_THRESHOLD)
                )
                & (streets == step.street)
            ]
            if len(filtered) > 0:
                step.volume = filtered["Vol"].mean()

    with open(ROUTES_PICKLE, "wb") as f:
        pkl.dump(taxis_routes, f)


if __name__ == "__main__":
    if not os.path.isfile(TAXIS_STEPS_PICKLE):
        get_taxis_steps()

    get_taxis_routes()
