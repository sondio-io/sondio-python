from __future__ import annotations

from typing import Optional

import pandas as pd

from .._coerce import make_coercer
from ..client import fetch

_coerce = make_coercer(
    numeric=("latitude", "longitude"),
    datetime=("permit_date", "approval_date"),
)


def permits(
    *,
    country: Optional[str] = None,
    state: Optional[str] = None,
    county: Optional[str] = None,
    operator: Optional[str] = None,
    status: Optional[str] = None,
    search: Optional[str] = None,
    sort: Optional[str] = None,
    order: Optional[str] = None,
    limit: Optional[int] = None,
    page: Optional[int] = None,
    all_pages: bool = False,
) -> pd.DataFrame:
    """Drilling permits.

    Maps to `/api/v1/data/oilgas-permits`.
    """
    return fetch(
        "data/oilgas-permits",
        params={
            "country": country,
            "state": state,
            "county": county,
            "operator": operator,
            "status": status,
            "search": search,
            "sort": sort,
            "order": order,
            "limit": limit,
            "page": page,
        },
        all_pages=all_pages,
        coerce=_coerce,
    )
