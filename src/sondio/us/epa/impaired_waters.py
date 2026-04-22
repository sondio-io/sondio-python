from __future__ import annotations

from typing import Optional

import pandas as pd

from ..._coerce import make_coercer
from ...client import fetch

_coerce = make_coercer(numeric=("latitude", "longitude"))


def impaired_waters(
    *,
    state: Optional[str] = None,
    pollutant: Optional[str] = None,
    search: Optional[str] = None,
    sort: Optional[str] = None,
    order: Optional[str] = None,
    limit: Optional[int] = None,
    page: Optional[int] = None,
    all_pages: bool = False,
) -> pd.DataFrame:
    """EPA Clean Water Act 303(d) impaired waters.

    Maps to `/api/v1/data/us-epa-impaired-waters`.
    """
    return fetch(
        "data/us-epa-impaired-waters",
        params={
            "state": state,
            "pollutant": pollutant,
            "search": search,
            "sort": sort,
            "order": order,
            "limit": limit,
            "page": page,
        },
        all_pages=all_pages,
        coerce=_coerce,
    )
