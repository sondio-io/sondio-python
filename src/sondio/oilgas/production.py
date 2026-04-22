"""Per-well oil & gas production history."""
from __future__ import annotations

from typing import Optional

import pandas as pd

from .._coerce import make_coercer
from ..client import fetch

_coerce = make_coercer(
    numeric=("oil_bbl", "gas_mcf", "water_bbl", "condensate_bbl", "casinghead_gas_mcf", "days_producing"),
    datetime=("production_date", "reported_date", "date"),
)


def production(
    well_id: str,
    *,
    months: Optional[int] = None,
    as_of: Optional[str] = None,
    include_revisions: bool = False,
) -> pd.DataFrame:
    """Monthly production history for a single well.

    Maps to ``/api/v1/data/oilgas-wells/{well_id}/production``. ``well_id``
    accepts either the Sondio UUID or the source ``external_id``.

    ``months`` defaults to 24 server-side (max 360). Volumes resolve at
    well-level where the source reports them, else fall back to lease-level
    (``level`` in the response metadata).

    ``as_of`` / ``include_revisions`` are Pro+ features that expose the
    full reported-date revision history of each month.
    """
    params: dict[str, object] = {}
    if months is not None:
        params["months"] = months
    if as_of is not None:
        params["as_of"] = as_of
    if include_revisions:
        params["include_revisions"] = "true"
    return fetch(
        f"data/oilgas-wells/{well_id}/production",
        params=params,
        coerce=_coerce,
        records_key="records",
    )
