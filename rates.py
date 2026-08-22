# rates.py
from io import StringIO

import httpx
import polars as pl

FRED_URL = "https://fred.stlouisfed.org/graph/fredgraph.csv?id=MORTGAGE30US"


def get_current_30yr_rate() -> float:
    """
    Pulls the latest weekly 30-year fixed mortgage rate average
    (Freddie Mac PMMS, distributed via FRED). Returns as a decimal,
    e.g. 0.0665 for 6.65%.
    """
    response = httpx.get(FRED_URL, timeout=10)
    response.raise_for_status()

    df = pl.read_csv(StringIO(response.text))
    latest_row = df.tail(1)
    rate_str = latest_row["MORTGAGE30US"][0]

    return float(rate_str) / 100