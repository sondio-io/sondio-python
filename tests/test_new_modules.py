from __future__ import annotations

import httpx
import pandas as pd
import respx

import sondio


def _envelope(items, has_more=False):
    return {"items": items, "pagination": {"page": 1, "limit": len(items), "hasMore": has_more}}


@respx.mock
def test_wind_turbines_maps_params_and_coerces():
    route = respx.get("https://api.test.local/api/v1/data/wind-turbines").mock(
        return_value=httpx.Response(
            200,
            json=_envelope(
                [{"id": "a", "t_state": "TX", "t_cap": "4500.00", "p_cap": "301.50", "p_year": 2025, "latitude": 26.5, "longitude": -97.6}]
            ),
        )
    )
    df = sondio.wind_turbines(state="TX", manufacturer="Nordex", min_capacity_kw=1500, bbox=(-100.0, 25.0, -95.0, 30.0))
    q = dict(route.calls.last.request.url.params)
    assert q["t_state"] == "TX"
    assert q["t_manu"] == "Nordex"
    assert q["min_t_cap"] == "1500"
    assert q["west"] == "-100.0" and q["east"] == "-95.0"
    assert df["t_cap"].iloc[0] == 4500.0
    assert df["p_year"].iloc[0] == 2025


@respx.mock
def test_rail_lines_passenger_bool_becomes_string_and_coerces_miles():
    route = respx.get("https://api.test.local/api/v1/data/rail-lines").mock(
        return_value=httpx.Response(
            200, json=_envelope([{"id": "r1", "miles": "965.67", "tracks": 1, "country_code": "US"}])
        )
    )
    df = sondio.rail_lines(country="US", state="AK", passenger=False)
    q = dict(route.calls.last.request.url.params)
    assert q["country_code"] == "US"
    assert q["subdivision_code"] == "AK"
    assert q["passenger"] == "false"
    assert df["miles"].iloc[0] == 965.67


@respx.mock
def test_svi_tracts_percent_coerced_and_rpl_filter_mapped():
    route = respx.get("https://api.test.local/api/v1/data/us-svi-tracts").mock(
        return_value=httpx.Response(
            200,
            json=_envelope(
                [{"id": "t1", "rpl_themes_overall": "0.8734", "pct_poverty": "22.4", "total_population": 2500}]
            ),
        )
    )
    df = sondio.us.cdc.svi_tracts(state="LA", min_rpl=0.75, min_population=1000)
    q = dict(route.calls.last.request.url.params)
    assert q["subdivision_code"] == "LA"
    assert q["min_rpl_themes_overall"] == "0.75"
    assert q["min_total_population"] == "1000"
    assert df["rpl_themes_overall"].iloc[0] == 0.8734
    assert df["pct_poverty"].iloc[0] == 22.4


@respx.mock
def test_production_uses_records_envelope_and_coerces_numerics():
    respx.get("https://api.test.local/api/v1/data/oilgas-wells/abc-123/production").mock(
        return_value=httpx.Response(
            200,
            json={
                "level": "well",
                "lease_well_count": 1,
                "records": [
                    {"production_date": "2025-01-01", "oil_bbl": "12500.5", "gas_mcf": "34000", "water_bbl": "800", "days_producing": 31},
                    {"production_date": "2024-12-01", "oil_bbl": "11000.0", "gas_mcf": "32000", "water_bbl": "700", "days_producing": 31},
                ],
                "tier": "pro",
            },
        )
    )
    df = sondio.oilgas.production("abc-123", months=12)
    assert len(df) == 2
    assert df["oil_bbl"].iloc[0] == 12500.5
    assert pd.api.types.is_datetime64_any_dtype(df["production_date"])


@respx.mock
def test_production_empty_records_returns_empty_frame():
    respx.get("https://api.test.local/api/v1/data/oilgas-wells/none/production").mock(
        return_value=httpx.Response(200, json={"level": "none", "lease_well_count": 0, "records": [], "tier": "free"})
    )
    df = sondio.oilgas.production("none")
    assert df.empty
