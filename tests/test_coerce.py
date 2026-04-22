from __future__ import annotations

import httpx
import pandas as pd
import respx

import sondio


def _env(items):
    return {"items": items, "pagination": {"page": 1, "limit": len(items), "hasMore": False}}


@respx.mock
def test_earthquakes_coerces_string_numerics():
    respx.get("https://api.test.local/api/v1/data/earthquakes").mock(
        return_value=httpx.Response(200, json=_env([
            {"id": "1", "magnitude": "2.3", "depth_km": "8.81", "event_time": "2026-01-21T22:52:32Z", "state": "TX"},
            {"id": "2", "magnitude": "4.1", "depth_km": "15.0", "event_time": "2026-01-22T01:00:00Z", "state": "CA"},
        ]))
    )
    df = sondio.earthquakes(page=1)
    assert df["magnitude"].dtype.kind == "f"
    assert df["depth_km"].dtype.kind == "f"
    assert pd.api.types.is_datetime64_any_dtype(df["event_time"])
    # Unknown columns are left untouched (not numerically coerced)
    assert df["state"].dtype.kind not in "fiu"


@respx.mock
def test_ghg_facilities_coerces_total_co2e():
    respx.get("https://api.test.local/api/v1/data/us-ghg-facilities").mock(
        return_value=httpx.Response(200, json=_env([
            {"id": "1", "year": 2024, "total_co2e": "12345.6", "state": "TX"},
        ]))
    )
    df = sondio.us.ghg.facilities(page=1)
    assert df["total_co2e"].dtype.kind == "f"


@respx.mock
def test_coercion_handles_empty_frame():
    respx.get("https://api.test.local/api/v1/data/earthquakes").mock(
        return_value=httpx.Response(200, json=_env([]))
    )
    df = sondio.earthquakes(page=1)
    assert df.empty
