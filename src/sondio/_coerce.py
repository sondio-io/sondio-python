"""Per-endpoint column-type coercion.

Server returns numeric-looking columns as strings in several places
(`magnitude`, `depth_km`, `depth_ft`, etc.). Each endpoint module passes
its known numeric/datetime columns in and the helpers here coerce only
those — unknown columns pass through untouched.
"""
from __future__ import annotations

from typing import Iterable

import pandas as pd


def coerce_numeric(df: pd.DataFrame, cols: Iterable[str]) -> pd.DataFrame:
    for c in cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    return df


def coerce_datetime(df: pd.DataFrame, cols: Iterable[str], utc: bool = True) -> pd.DataFrame:
    for c in cols:
        if c in df.columns:
            df[c] = pd.to_datetime(df[c], errors="coerce", utc=utc)
    return df


def make_coercer(
    *,
    numeric: Iterable[str] = (),
    datetime: Iterable[str] = (),
):
    numeric_cols = tuple(numeric)
    datetime_cols = tuple(datetime)

    def _coerce(df: pd.DataFrame) -> pd.DataFrame:
        df = coerce_numeric(df, numeric_cols)
        df = coerce_datetime(df, datetime_cols)
        return df

    return _coerce
