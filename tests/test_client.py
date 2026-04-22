from __future__ import annotations

import httpx
import pandas as pd
import pytest
import respx

import sondio
from sondio.client import fetch, SondioAPIError, SondioError


def _envelope(items, has_more=False):
    return {"items": items, "pagination": {"page": 1, "limit": len(items), "hasMore": has_more}}


@respx.mock
def test_fetch_returns_dataframe():
    respx.get("https://api.test.local/api/v1/data/earthquakes").mock(
        return_value=httpx.Response(200, json=_envelope([{"id": "1"}, {"id": "2"}]))
    )
    df = fetch("data/earthquakes")
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    assert list(df["id"]) == ["1", "2"]


@respx.mock
def test_auth_header_is_bearer_only():
    route = respx.get("https://api.test.local/api/v1/data/earthquakes").mock(
        return_value=httpx.Response(200, json=_envelope([]))
    )
    fetch("data/earthquakes")
    req = route.calls.last.request
    assert req.headers["authorization"] == "Bearer sk_sondio_test"
    assert "x-api-key" not in (k.lower() for k in req.headers.keys())


@respx.mock
def test_missing_api_key_raises():
    sondio.api_key = None
    import os
    prev = os.environ.pop("SONDIO_API_KEY", None)
    try:
        with pytest.raises(SondioError, match="API key"):
            fetch("data/earthquakes")
    finally:
        sondio.api_key = "sk_sondio_test"
        if prev is not None:
            os.environ["SONDIO_API_KEY"] = prev


@respx.mock
def test_api_error_raises_with_status():
    respx.get("https://api.test.local/api/v1/data/earthquakes").mock(
        return_value=httpx.Response(403, text="Forbidden")
    )
    with pytest.raises(SondioAPIError) as exc:
        fetch("data/earthquakes")
    assert exc.value.status_code == 403


@respx.mock
def test_none_params_are_dropped():
    route = respx.get("https://api.test.local/api/v1/data/earthquakes").mock(
        return_value=httpx.Response(200, json=_envelope([]))
    )
    fetch("data/earthquakes", params={"state": "TX", "min_mag": None, "days": 7})
    q = dict(route.calls.last.request.url.params)
    assert q == {"state": "TX", "days": "7", "page": "1"}
