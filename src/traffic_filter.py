import pandas as pd

from functools import reduce
from src.utils import DATA_DIR, TRAFFIC_CSV


def read_csv(file_path: str) -> pd.DataFrame:
    df = pd.read_csv(file_path, skipinitialspace=True)

    return df


def filter_dataset(df: pd.DataFrame, **kwargs) -> pd.DataFrame:
    return df[
        reduce(
            lambda cur, key: cur & (df[key] == kwargs[key]),
            kwargs.keys(),
            pd.Series(True, index=df.index),
        )
    ]


def save_to_csv(df: pd.DataFrame, file_path: str) -> None:
    df.to_csv(file_path, index=False)


if __name__ == "__main__":
    df = read_csv(TRAFFIC_CSV)
    filtered_df = filter_dataset(df, Yr=2015)
    save_to_csv(filtered_df, f"{DATA_DIR}/traffic_205.csv")
