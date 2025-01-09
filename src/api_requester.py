import os
from typing import List, Tuple

import requests
from dotenv import load_dotenv

from src.utils import BASE_URL


def get_public_token() -> str:
    load_dotenv()

    return os.getenv("PUBLIC_TOKEN")


def build_url(coordinates: List[Tuple[str]]) -> str:
    coordinates_params = ";".join([f"{lng},{lat}" for lng, lat in coordinates])

    return f"{BASE_URL}/{coordinates_params}"


def send_request(coordinates: Tuple[Tuple[float]], **kwargs) -> requests.Response:
    url = build_url(coordinates)

    kwargs["access_token"] = get_public_token()
    response = requests.get(url, params=kwargs)

    return response


# if __name__ == "__main__":
#     coordinates = [(34.596, -23.46), (34.597, -23.46)]
#     response = send_request(
#         coordinates=coordinates, steps="true", access_token=get_public_token()
#     )
