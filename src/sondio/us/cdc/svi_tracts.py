"""CDC Social Vulnerability Index at the census-tract level."""
from __future__ import annotations

from typing import Optional

import pandas as pd

from ..._coerce import make_coercer
from ...client import fetch

# Every percent and RPL (ranked percentile) field ships as a string. Coerce
# the full set so downstream analysis is just math.
_PCT_FIELDS = (
    "pct_poverty",
    "pct_unemployed",
    "pct_housing_cost_burden",
    "pct_no_hs_diploma",
    "pct_uninsured",
    "pct_age_65_plus",
    "pct_age_17_and_under",
    "pct_disabled",
    "pct_single_parent",
    "pct_limited_english",
    "pct_minority",
    "pct_multi_unit",
    "pct_mobile_home",
    "pct_crowded_housing",
    "pct_no_vehicle",
    "pct_group_quarters",
)
_RPL_FIELDS = (
    "rpl_theme1_socioeconomic",
    "rpl_theme2_household",
    "rpl_theme3_minority",
    "rpl_theme4_housing",
    "rpl_themes_overall",
)

_coerce = make_coercer(
    numeric=(
        "data_year",
        "total_population",
        "housing_units",
        "households",
        "area_sq_mi",
        *_PCT_FIELDS,
        *_RPL_FIELDS,
    ),
)


def svi_tracts(
    *,
    state: Optional[str] = None,
    state_fips: Optional[str] = None,
    county_fips: Optional[str] = None,
    county_name: Optional[str] = None,
    tract_fips: Optional[str] = None,
    data_year: Optional[int] = None,
    min_rpl: Optional[float] = None,
    max_rpl: Optional[float] = None,
    min_population: Optional[int] = None,
    max_population: Optional[int] = None,
    sort: Optional[str] = None,
    order: Optional[str] = None,
    limit: Optional[int] = None,
    page: Optional[int] = None,
    all_pages: bool = False,
) -> pd.DataFrame:
    """CDC Social Vulnerability Index (SVI) tract-level scores.

    Maps to ``/api/v1/data/us-svi-tracts``. ``min_rpl``/``max_rpl`` filter
    on ``rpl_themes_overall`` (0 = least vulnerable, 1 = most).
    """
    return fetch(
        "data/us-svi-tracts",
        params={
            "subdivision_code": state,
            "state_fips": state_fips,
            "county_fips": county_fips,
            "county_name": county_name,
            "tract_fips": tract_fips,
            "data_year": data_year,
            "min_rpl_themes_overall": min_rpl,
            "max_rpl_themes_overall": max_rpl,
            "min_total_population": min_population,
            "max_total_population": max_population,
            "sort": sort,
            "order": order,
            "limit": limit,
            "page": page,
        },
        all_pages=all_pages,
        coerce=_coerce,
    )
