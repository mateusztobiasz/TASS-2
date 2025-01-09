import pandas as pd

from src.utils import TAXIS_CSV, TAXIS_PICKLE, TRAFFICS_CSV, TRAFFICS_PICKLE


def preprocess_traffics() -> None:
    traffic = pd.read_csv(TRAFFICS_CSV)
    traffic = traffic[traffic["Yr"] == 2015]

    df = pd.DataFrame(
        {
            "year": traffic["Yr"],
            "month": traffic["M"],
            "day": traffic["D"],
            "hour": traffic["HH"],
            "minute": traffic["MM"],
        }
    )

    traffic["date"] = pd.to_datetime(df)
    traffic = traffic.drop(
        columns=["SegmentID", "Vol", "Boro", "RequestID", "Yr", "M", "D", "HH", "MM"]
    )

    traffic.to_pickle(TRAFFICS_PICKLE)


def preprocess_taxis() -> None:
    taxis = pd.read_csv(TAXIS_CSV)

    taxis["pickup_date"] = pd.to_datetime(
        taxis["pickup_datetime"], format="%m/%d/%Y %I:%M:%S %p"
    )
    taxis["dropoff_date"] = pd.to_datetime(
        taxis["dropoff_datetime"], format="%m/%d/%Y %I:%M:%S %p"
    )

    taxis["Total_cost"] = taxis["Total_amount"] - taxis["Tip_amount"]

    taxis = taxis.drop(
        columns=[
            "vendorid",
            "Store_and_fwd_flag",
            "pickup_datetime",
            "dropoff_datetime",
            "rate_code",
            "Passenger_count",
            "Fare_amount",
            "Extra",
            "MTA_tax",
            "Tolls_amount",
            "Tip_amount",
            "Total_amount",
            "Ehail_fee",
            "Improvement_surcharge",
            "Payment_type",
            "Trip_type",
        ]
    )
    taxis.to_pickle(TAXIS_PICKLE)


if __name__ == "__main__":
    preprocess_traffics()
    preprocess_taxis()
