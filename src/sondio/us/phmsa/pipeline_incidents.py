from __future__ import annotations

from typing import Optional

import pandas as pd

from ..._coerce import make_coercer
from ...client import fetch

_coerce = make_coercer(
    numeric=(
        "year",
        "fatalities",
        "injuries",
        "evacuated",
        "property_damage",
        "latitude",
        "longitude",
    ),
    datetime=("incident_date",),
)


def pipeline_incidents(
    *,
    state: Optional[str] = None,
    operator: Optional[str] = None,
    cause: Optional[str] = None,
    year: Optional[int] = None,
    search: Optional[str] = None,
    sort: Optional[str] = None,
    order: Optional[str] = None,
    limit: Optional[int] = None,
    page: Optional[int] = None,
    all_pages: bool = False,
) -> pd.DataFrame:
    """PHMSA pipeline incidents.

    Maps to `/api/v1/data/us-phmsa-pipeline-incidents`.
    """
    return fetch(
        "data/us-phmsa-pipeline-incidents",
        params={
            "state": state,
            "operator": operator,
            "cause": cause,
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
