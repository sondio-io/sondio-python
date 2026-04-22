from __future__ import annotations

from typing import Optional

import pandas as pd

from ..._coerce import make_coercer
from ...client import fetch

_coerce = make_coercer(numeric=("depth_ft", "latitude", "longitude"))


def aquifer_exemptions(
    *,
    state: Optional[str] = None,
    well_class: Optional[str] = None,
    search: Optional[str] = None,
    sort: Optional[str] = None,
    order: Optional[str] = None,
    limit: Optional[int] = None,
    page: Optional[int] = None,
    all_pages: bool = False,
) -> pd.DataFrame:
    """EPA UIC aquifer exemptions.

    Maps to `/api/v1/data/us-epa-aquifer-exemptions`.
    """
    return fetch(
        "data/us-epa-aquifer-exemptions",
        params={
            "state": state,
            "well_class": well_class,
            "search": search,
            "sort": sort,
            "order": order,
            "limit": limit,
            "page": page,
        },
        all_pages=all_pages,
        coerce=_coerce,
    )
