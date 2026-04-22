from __future__ import annotations

from typing import Optional

import pandas as pd

from ..._coerce import make_coercer
from ...client import fetch

_coerce = make_coercer(
    numeric=("total_co2e", "year", "latitude", "longitude"),
)


def facilities(
    *,
    state: Optional[str] = None,
    industry_type: Optional[str] = None,
    year: Optional[int] = None,
    search: Optional[str] = None,
    sort: Optional[str] = None,
    order: Optional[str] = None,
    limit: Optional[int] = None,
    page: Optional[int] = None,
    all_pages: bool = False,
) -> pd.DataFrame:
    """GHG Reporting Program (GHGRP) facility emissions.

    Maps to `/api/v1/data/us-ghg-facilities`.
    """
    return fetch(
        "data/us-ghg-facilities",
        params={
            "state": state,
            "industry_type": industry_type,
            "year": year,
            "search": search,
            "sort": sort,
            "order": order,
            "limit": limit,
            "page": page,
        },
        all_pages=all_pages,
        coerce=_coerce,
    )
