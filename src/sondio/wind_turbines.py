"""Wind turbines — vertical-rule global dataset (top-level).

Source: US Wind Turbine Database (USWTDB). US-only today; the API
surface is vertical-rule so additional countries can land as rows.
"""
from __future__ import annotations

from typing import Optional

import pandas as pd

from ._coerce import make_coercer
from .client import fetch

_coerce = make_coercer(
    numeric=(
        "p_year",
        "p_cap",
        "t_cap",
        "t_hh",
        "t_rd",
        "latitude",
        "longitude",
    ),
)


def wind_turbines(
    *,
    state: Optional[str] = None,
    county: Optional[str] = None,
    project_name: Optional[str] = None,
    manufacturer: Optional[str] = None,
    year: Optional[int] = None,
    min_year: Optional[int] = None,
    max_year: Optional[int] = None,
    min_capacity_kw: Optional[float] = None,
    max_capacity_kw: Optional[float] = None,
    bbox: Optional[tuple[float, float, float, float]] = None,
    sort: Optional[str] = None,
    order: Optional[str] = None,
    limit: Optional[int] = None,
    page: Optional[int] = None,
    all_pages: bool = False,
) -> pd.DataFrame:
    """Wind turbines (USWTDB) as a DataFrame.

    Maps to ``/api/v1/data/wind-turbines``. Field prefixes: ``t_*`` = turbine
    (state, county, capacity kW, hub height m, rotor diameter m), ``p_*`` =
    project (name, year online, total project MW).

    ``bbox`` is ``(west, south, east, north)`` in EPSG:4326.
    """
    params: dict[str, object] = {
        "t_state": state,
        "t_county": county,
        "p_name": project_name,
        "t_manu": manufacturer,
        "p_year": year,
        "min_p_year": min_year,
        "max_p_year": max_year,
        "min_t_cap": min_capacity_kw,
        "max_t_cap": max_capacity_kw,
        "sort": sort,
        "order": order,
        "limit": limit,
        "page": page,
    }
    if bbox is not None:
        west, south, east, north = bbox
        params["west"] = west
        params["south"] = south
        params["east"] = east
        params["north"] = north
    return fetch("data/wind-turbines", params=params, all_pages=all_pages, coerce=_coerce)
