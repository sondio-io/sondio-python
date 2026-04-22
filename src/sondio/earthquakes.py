"""Earthquakes — vertical-rule global dataset (top-level)."""
from __future__ import annotations

from typing import Optional

import pandas as pd

from ._coerce import make_coercer
from .client import fetch

_coerce = make_coercer(
    numeric=("magnitude", "depth_km", "latitude", "longitude", "felt_reports", "significance"),
    datetime=("event_time",),
)


def earthquakes(
    *,
    state: Optional[str] = None,
    min_mag: Optional[float] = None,
    max_mag: Optional[float] = None,
    days: Optional[int] = None,
    sort: Optional[str] = None,
    order: Optional[str] = None,
    limit: Optional[int] = None,
    page: Optional[int] = None,
    all_pages: bool = False,
) -> pd.DataFrame:
    """Earthquakes (USGS) as a DataFrame.

    Maps to `/api/v1/data/earthquakes`.
    """
    return fetch(
        "data/earthquakes",
        params={
            "state": state,
            "min_mag": min_mag,
            "max_mag": max_mag,
            "days": days,
            "sort": sort,
            "order": order,
            "limit": limit,
            "page": page,
        },
        all_pages=all_pages,
        coerce=_coerce,
    )
