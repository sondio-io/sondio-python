from __future__ import annotations

from typing import Optional

import pandas as pd

from .._coerce import make_coercer
from ..client import fetch

_coerce = make_coercer(
    numeric=("latitude", "longitude"),
    datetime=("spud_date", "completion_date", "permit_date"),
)


def wells(
    *,
    country: Optional[str] = None,
    state: Optional[str] = None,
    county: Optional[str] = None,
    basin: Optional[str] = None,
    operator: Optional[str] = None,
    status: Optional[str] = None,
    search: Optional[str] = None,
    producing: Optional[bool] = None,
    sort: Optional[str] = None,
    order: Optional[str] = None,
    limit: Optional[int] = None,
    page: Optional[int] = None,
    all_pages: bool = False,
) -> pd.DataFrame:
    """Oil & gas wells.

    Maps to `/api/v1/data/oilgas-wells`.
    """
    params: dict = {
        "country": country,
        "state": state,
        "county": county,
        "basin": basin,
        "operator": operator,
        "status": status,
        "search": search,
        "sort": sort,
        "order": order,
        "limit": limit,
        "page": page,
    }
    if producing is not None:
        params["producing"] = "true" if producing else "false"
    return fetch("data/oilgas-wells", params=params, all_pages=all_pages, coerce=_coerce)
