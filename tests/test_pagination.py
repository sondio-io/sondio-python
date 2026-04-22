from __future__ import annotations

import httpx
import pytest
import respx

from sondio.client import fetch, MAX_AUTO_PAGES


def _env(items, has_more):
    return {"items": items, "pagination": {"page": 1, "limit": len(items), "hasMore": has_more}}


@respx.mock
def test_default_returns_first_page_only():
    route = respx.get("https://api.test.local/api/v1/data/earthquakes").mock(
        return_value=httpx.Response(200, json=_env([{"id": "a"}], has_more=True))
    )
    with pytest.warns(UserWarning, match="truncated"):
        df = fetch("data/earthquakes")
    assert len(df) == 1
    assert route.calls.call_count == 1


@respx.mock
def test_explicit_page_suppresses_warning():
    respx.get("https://api.test.local/api/v1/data/earthquakes").mock(
        return_value=httpx.Response(200, json=_env([{"id": "a"}], has_more=True))
    )
    import warnings
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        df = fetch("data/earthquakes", params={"page": 2})
    assert len(df) == 1


@respx.mock
def test_all_pages_iterates_until_has_more_false():
    responses = [
        httpx.Response(200, json=_env([{"id": "a"}], has_more=True)),
        httpx.Response(200, json=_env([{"id": "b"}], has_more=True)),
        httpx.Response(200, json=_env([{"id": "c"}], has_more=False)),
    ]
    route = respx.get("https://api.test.local/api/v1/data/earthquakes").mock(side_effect=responses)
    df = fetch("data/earthquakes", all_pages=True)
    assert list(df["id"]) == ["a", "b", "c"]
    assert route.calls.call_count == 3


@respx.mock
def test_all_pages_respects_hard_cap():
    # Always-more response; cap should kick in and warn
    respx.get("https://api.test.local/api/v1/data/earthquakes").mock(
        return_value=httpx.Response(200, json=_env([{"id": "x"}], has_more=True))
    )
    with pytest.warns(UserWarning, match="seatbelt"):
        df = fetch("data/earthquakes", all_pages=True)
    assert len(df) == MAX_AUTO_PAGES
