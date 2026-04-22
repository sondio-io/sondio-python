from __future__ import annotations

from typing import Optional

import pandas as pd

from ..._coerce import make_coercer
from ...client import fetch

_coerce = make_coercer(numeric=("latitude", "longitude"))


def permits(
    *,
    state: Optional[str] = None,
    status: Optional[str] = None,
    facility_type: Optional[str] = None,
    search: Optional[str] = None,
    sort: Optional[str] = None,
    order: Optional[str] = None,
    limit: Optional[int] = None,
    page: Optional[int] = None,
    all_pages: bool = False,
) -> pd.DataFrame:
    """NPDES-authorized wastewater discharge permits.

    Maps to `/api/v1/data/us-npdes-permits`.
    """
    return fetch(
        "data/us-npdes-permits",
        params={
            "state": state,
            "status": status,
            "facility_type": facility_type,
            "search": search,
            "sort": sort,
            "order": order,
            "limit": limit,
            "page": page,
        },
        all_pages=all_pages,
        coerce=_coerce,
    )
