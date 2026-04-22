"""HTTP client: Bearer auth, opt-in pagination, typed coercion."""
from __future__ import annotations

import time
from typing import Any, Callable, Dict, List, Optional
import warnings

import httpx
import pandas as pd

from . import config as _config
from ._version import __version__

DEFAULT_TIMEOUT = 30.0
_RETRIABLE_STATUS = {429, 500, 502, 503, 504}

# Hard cap on auto-pagination so a misconfigured call can't spin forever.
# Above this, we return what we have and warn. Users who genuinely need
# every row should page manually.
MAX_AUTO_PAGES = 500

# Coercion function: receives the DataFrame and returns a coerced DataFrame.
# Endpoint modules register their own via `fetch(..., coerce=...)`.
Coercer = Callable[[pd.DataFrame], pd.DataFrame]


class SondioError(Exception):
    """Base exception for SDK-raised errors."""


class SondioAPIError(SondioError):
    """Non-2xx response from the API after retries."""

    def __init__(self, status_code: int, body: str):
        self.status_code = status_code
        self.body = body
        super().__init__(f"Sondio API error {status_code}: {body[:500]}")


def _headers(api_key: str) -> Dict[str, str]:
    return {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json",
        "User-Agent": f"sondio-python/{__version__}",
    }


def _clean(params: Dict[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in params.items() if v is not None}


def _request(
    client: httpx.Client,
    url: str,
    *,
    headers: Dict[str, str],
    params: Dict[str, Any],
) -> httpx.Response:
    try:
        resp = client.get(url, headers=headers, params=params)
    except httpx.RequestError:
        time.sleep(1.0)
        resp = client.get(url, headers=headers, params=params)
    if resp.status_code in _RETRIABLE_STATUS:
        retry_after = resp.headers.get("Retry-After")
        try:
            wait = float(retry_after) if retry_after else (30.0 if resp.status_code == 429 else 1.0)
        except ValueError:
            wait = 30.0 if resp.status_code == 429 else 1.0
        time.sleep(wait)
        resp = client.get(url, headers=headers, params=params)
    return resp


def _resolve_key() -> str:
    from . import api_key as attr_key  # type: ignore[attr-defined]

    key = _config.resolve_api_key(attr_key)
    if not key:
        raise SondioError(
            "Sondio API key not set. Assign sondio.api_key = \"sk_sondio_...\" "
            "or set the SONDIO_API_KEY environment variable."
        )
    return key


def _resolve_base_url() -> str:
    from . import base_url as attr_base  # type: ignore[attr-defined]

    return _config.resolve_base_url(attr_base)


def fetch_geojson(
    path: str,
    *,
    params: Optional[Dict[str, Any]] = None,
    timeout: float = DEFAULT_TIMEOUT,
) -> Dict[str, Any]:
    """GET `path` and return the raw GeoJSON FeatureCollection body.

    The boundaries endpoints return `{type: "FeatureCollection", features: [...]}`
    rather than the canonical `{items, pagination, meta}` envelope, so they
    need a separate code path.
    """
    api_key = _resolve_key()
    url = f"{_resolve_base_url().rstrip('/')}/{path.lstrip('/')}"
    headers = _headers(api_key)
    clean_params = _clean(dict(params or {}))
    with httpx.Client(timeout=timeout) as client:
        resp = _request(client, url, headers=headers, params=clean_params)
    if resp.status_code >= 400:
        raise SondioAPIError(resp.status_code, resp.text)
    return resp.json()


def fetch(
    path: str,
    *,
    params: Optional[Dict[str, Any]] = None,
    all_pages: bool = False,
    coerce: Optional[Coercer] = None,
    timeout: float = DEFAULT_TIMEOUT,
) -> pd.DataFrame:
    """GET `path` and return a pandas DataFrame.

    `all_pages=False` (default): one page per call. If the server indicates
    more pages, a UserWarning is emitted so the caller knows the result was
    truncated.

    `all_pages=True`: iterate until `pagination.hasMore` is false or
    MAX_AUTO_PAGES is reached. Hitting the cap emits a UserWarning.
    """
    api_key = _resolve_key()
    url = f"{_resolve_base_url().rstrip('/')}/{path.lstrip('/')}"
    headers = _headers(api_key)
    clean_params = _clean(dict(params or {}))
    explicit_page = clean_params.get("page") is not None

    page = int(clean_params.get("page") or 1)
    collected: List[Dict[str, Any]] = []
    hit_cap = False
    last_has_more = False

    with httpx.Client(timeout=timeout) as client:
        while True:
            resp = _request(client, url, headers=headers, params={**clean_params, "page": page})
            if resp.status_code >= 400:
                raise SondioAPIError(resp.status_code, resp.text)
            body = resp.json()
            items = body.get("items") or []
            collected.extend(items)

            last_has_more = bool((body.get("pagination") or {}).get("hasMore"))
            if explicit_page or not all_pages or not last_has_more:
                break
            page += 1
            if page > MAX_AUTO_PAGES:
                hit_cap = True
                break

    if not all_pages and not explicit_page and last_has_more:
        warnings.warn(
            f"Result truncated to the first page. Pass all_pages=True to iterate, "
            f"or set page= to a specific page.",
            UserWarning,
            stacklevel=3,
        )
    if hit_cap:
        warnings.warn(
            f"Auto-pagination hit the {MAX_AUTO_PAGES}-page seatbelt. "
            f"Narrow the query or use explicit page= to continue.",
            UserWarning,
            stacklevel=3,
        )

    df = pd.DataFrame(collected)
    if coerce is not None and not df.empty:
        df = coerce(df)
    return df
