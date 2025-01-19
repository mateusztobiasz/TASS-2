import pickle as pkl

import pandas as pd

from src.paths_extractor import normalize_street
from src.utils import TAXIS_STEPS_PICKLE, TRAFFICS_PICKLE

if __name__ == "__main__":
    with open(TAXIS_STEPS_PICKLE, "rb") as f:
        taxis_steps = pkl.load(f)

    taxis_streets = []
    for route in taxis_steps:
        for element in route:
            if "name" in element and element["name"] != "":
                taxis_streets.append(element["name"])
    taxis_streets = [normalize_street(s) for s in taxis_streets]

    traffic = pd.read_pickle(TRAFFICS_PICKLE)
    traffic_streets = set(
        [normalize_street(s) for s in traffic.groupby(["street"]).groups.keys()]
    )

    # Count how many entries from taxis are covered by traffic dataset
    i = 0
    for s in taxis_streets:
        if s in traffic_streets:
            i = i + 1
    print(i / len(taxis_streets))

    # Compare different streets of both datasets
    tax = set(taxis_streets)
    print(tax - traffic_streets)
    print("-------------------------------------------------------------------------")
    print(traffic_streets - tax)
