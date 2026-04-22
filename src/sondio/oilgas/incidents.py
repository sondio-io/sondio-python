from __future__ import annotations

from typing import Optional

import pandas as pd

from .._coerce import make_coercer
from ..client import fetch

_coerce = make_coercer(
    numeric=("latitude", "longitude"),
    datetime=("incident_date", "reported_date"),
)


def incidents(
    *,
    country: Optional[str] = None,
    state: Optional[str] = None,
    county: Optional[str] = None,
    operator: Optional[str] = None,
    incident_type: Optional[str] = None,
    search: Optional[str] = None,
    sort: Optional[str] = None,
    order: Optional[str] = None,
    limit: Optional[int] = None,
    page: Optional[int] = None,
    all_pages: bool = False,
) -> pd.DataFrame:
    """Oil & gas incidents (spills, leaks, releases).

    Maps to `/api/v1/data/oilgas-incidents`.
    """
    return fetch(
        "data/oilgas-incidents",
        params={
            "country": country,
            "state": state,
            "county": county,
            "operator": operator,
            "incident_type": incident_type,
            "search": search,
            "sort": sort,
            "order": order,
            "limit": limit,
            "page": page,
        },
        all_pages=all_pages,
        coerce=_coerce,
    )
