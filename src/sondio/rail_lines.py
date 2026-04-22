"""Rail lines — vertical-rule global dataset (top-level).

Source: BTS NTAD North American Rail Lines. Multi-country (US, CA, MX)
— country is a row-level attribute.
"""
from __future__ import annotations

from typing import Optional

import pandas as pd

from ._coerce import make_coercer
from .client import fetch

_coerce = make_coercer(
    numeric=("miles", "tracks"),
)


def rail_lines(
    *,
    country: Optional[str] = None,
    state: Optional[str] = None,
    owner: Optional[str] = None,
    rail_subdivision: Optional[str] = None,
    passenger: Optional[bool] = None,
    min_miles: Optional[float] = None,
    max_miles: Optional[float] = None,
    min_tracks: Optional[int] = None,
    max_tracks: Optional[int] = None,
    bbox: Optional[tuple[float, float, float, float]] = None,
    sort: Optional[str] = None,
    order: Optional[str] = None,
    limit: Optional[int] = None,
    page: Optional[int] = None,
    all_pages: bool = False,
) -> pd.DataFrame:
    """North American rail lines (BTS NTAD) as a DataFrame.

    Maps to ``/api/v1/data/rail-lines``. ``country`` accepts ISO-3166-1
    alpha-2 (``US``, ``CA``, ``MX``); ``state`` accepts ISO-3166-2 local
    codes (``TX``, ``AB``, ``ON``, …). ``rail_subdivision`` is the
    operating-subdivision name (e.g. ``BRAZEAU``, ``KINGSTON``) —
    distinct from the ISO political subdivision.

    ``bbox`` is ``(west, south, east, north)`` in EPSG:4326.
    """
    params: dict[str, object] = {
        "country_code": country,
        "subdivision_code": state,
        "owner": owner,
        "rail_subdivision": rail_subdivision,
        "min_miles": min_miles,
        "max_miles": max_miles,
        "min_tracks": min_tracks,
        "max_tracks": max_tracks,
        "sort": sort,
        "order": order,
        "limit": limit,
        "page": page,
    }
    if passenger is not None:
        params["passenger"] = "true" if passenger else "false"
    if bbox is not None:
        west, south, east, north = bbox
        params["west"] = west
        params["south"] = south
        params["east"] = east
        params["north"] = north
    return fetch("data/rail-lines", params=params, all_pages=all_pages, coerce=_coerce)
