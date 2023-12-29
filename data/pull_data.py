import os
from typing import List

import pandas as pd
import yfinance as yf

import numpy as np

def pull_fdr_data(ticker: str) -> pd.DataFrame:
    return (
        pd.read_csv(os.path.join("data", "fdr", f"{ticker}.csv"), parse_dates=[0])
        .rename(columns={"Date": "date", "Close": "close"})
        .set_index("date")
        .replace(0.0, np.nan) # 0.0의 값을 np.nan으로 대체
    )

def _fill_blanks(data: pd.DataFrame):
    return data[
        data["close"].first_valid_index() : data["close"].last_valid_index() # 첫번째 유효한 값부터 마지막 유효한 값까지 추출
    ].fillna(
        method="ffill"
    )  # .interpolate()


def pull_fdr_data_multiple(
    tickers: List[str], fill_missing_dates=False
) -> pd.DataFrame:
    data = pd.concat(
        [pull_fdr_data(ticker).assign(ticker=ticker).copy() for ticker in tickers] # 행 기준 병합
    )

    if not fill_missing_dates:
        return data.dropna().copy()

    dates = data.reset_index()[["date"]].drop_duplicates().sort_values("date")
    data = data.reset_index().set_index("ticker")

    return (
        pd.concat(
            [
                _fill_blanks(
                    dates.merge(data.loc[t], on="date", how="left").assign(ticker=t)
                )
                for t in tickers
            ]
        )
        .reset_index()
        .set_index("date")
        .drop(columns="index")
        .copy()
    )
