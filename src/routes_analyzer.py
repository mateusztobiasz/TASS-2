import pickle as pkl
from typing import List, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src.models.route import Route
from src.utils import ROUTES_PICKLE


def load_routes(str_path: str) -> List[Route]:
    with open(str_path, "rb") as f:
        return pkl.load(f)


def get_routes_with_most_traffic(routes: List[Route], threshold: float) -> List[Route]:
    coefficients = [
        (
            sum([1 if s.volume != None else 0 for s in r.steps]) / len(r.steps)
            if any(r.steps)
            else 0
        )
        for r in routes
    ]

    return [
        r
        for c, r in zip(coefficients, routes)
        if c >= threshold and r.total_real_distance != 0
    ]


def map_costs(routes_filtered: List[Route]) -> None:

    for r in routes_filtered:
        r.total_cost = r.total_cost[0]


def get_routes_info(routes: List[Route]) -> pd.DataFrame:
    df = pd.DataFrame(
        (
            {
                "real_dist [m]": round(r.total_real_distance, 2),
                "steps_dist [m]": round(r.total_steps_distance(), 2),
                "diff_dist [m]": round(
                    r.total_real_distance - r.total_steps_distance(), 2
                ),
                "real_time [min]": round(r.total_real_time().total_seconds() / 60, 2),
                "steps_time [min]": round(r.total_steps_time().total_seconds() / 60, 2),
                "diff_time [min]": round(
                    (r.total_real_time() - r.total_steps_time()).total_seconds() / 60
                ),
                "min_per_km [min / km]": round(
                    (r.total_real_time().total_seconds() / 60)
                    / (r.total_real_distance / 1000),
                    2,
                ),
                "real_cost [$]": r.total_cost,
                "cost_per_km [$ / km]": round(
                    r.total_cost / (r.total_real_distance / 1000), 2
                ),
                "cost_per_minute [$ / min]": round(
                    r.total_cost / (r.total_real_time().total_seconds() / 60), 2
                ),
                "total_traffic": round(r.total_volume(), 2),
            }
            for r in routes
        )
    )

    return df[df["real_time [min]"] > 1]


def check_dist_diffs(routes_info: pd.DataFrame) -> Tuple[pd.DataFrame, pd.DataFrame]:
    big_diffs = routes_info[routes_info["diff_dist [m]"] > 300]
    small_diffs = routes_info[routes_info["diff_dist [m]"] <= 300]

    return big_diffs, small_diffs


def bin_by_traffic(routes: pd.DataFrame) -> pd.DataFrame:
    routes_cp = routes.copy()

    bins = np.around(np.linspace(0, 2000, 10), decimals=2)
    routes_cp["traffic_bin"] = pd.cut(
        routes_cp["total_traffic"], bins=bins, include_lowest=True
    )
    grouped_routes = routes_cp.groupby("traffic_bin", observed=True).count()

    return grouped_routes


def plot(series: pd.Series) -> None:
    plt.figure(figsize=(10, 6))
    series.plot(kind="bar", color="skyblue", edgecolor="black")

    plt.xlabel("Traffic Bins")
    plt.ylabel("Counts")
    plt.title("Counts of Traffic in Bins")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    plt.show()


if __name__ == "__main__":
    routes = load_routes(ROUTES_PICKLE)

    routes_filtered = get_routes_with_most_traffic(routes, 0.4)
    map_costs(routes_filtered)
    routes_info = get_routes_info(routes_filtered)

    print("[HIPOTEZA 1]: Czy kierowcy omijają korki?")
    print(
        "-----------------------------------------------------------------------------------------------------"
    )
    big_diffs, small_diffs = check_dist_diffs(routes_info)
    print(
        f"""Kierowcy, którzy przejechali dłuższą drogą niż najkrótsza: {len(big_diffs)} [{round(len(big_diffs) / len(routes_info), 3) * 100}%]. 
Ci, którzy wybrali najkrótszą: {len(small_diffs)} [{round(len(small_diffs) / len(routes_info), 3) * 100}%]. \n"""
    )
    big_diffs_traffic_count = bin_by_traffic(big_diffs)
    small_diffs_traffic_count = bin_by_traffic(small_diffs)
    print(
        f"Zgrupowane wartości natężenia dla kierowców, którzy przejechali dłuższą drogę: \n{big_diffs_traffic_count['total_traffic']}. \n"
    )
    print(
        f"Zgrupowane wartości natężenia dla kierowców, którzy przejechali najkrótszą drogę: \n{small_diffs_traffic_count['total_traffic']}. \n"
    )

    plot(big_diffs_traffic_count["total_traffic"])
    plot(small_diffs_traffic_count["total_traffic"])
