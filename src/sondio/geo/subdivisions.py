"""Country subdivisions (states, provinces).

Non-geometric by default — adding `with_geometry=True` returns a
GeoDataFrame of state polygons from `/api/v1/geo/boundaries/subdivisions`.
"""
from __future__ import annotations

from typing import Optional

import pandas as pd

from ..client import fetch, fetch_geojson


def subdivisions(
    *,
    country: Optional[str] = None,
    type: Optional[str] = None,
    limit: Optional[int] = None,
    page: Optional[int] = None,
    all_pages: bool = False,
    with_geometry: bool = False,
    bbox: Optional[tuple] = None,
    zoom: Optional[int] = None,
):
    """List country subdivisions as a DataFrame.

    `with_geometry=True` fetches simplified polygons from the boundaries
    endpoint and returns a GeoDataFrame (requires the `sondio[geo]` extra).
    `bbox=(west, south, east, north)` and `zoom` apply only when
    `with_geometry=True`.
    """
    if with_geometry:
        return _boundaries(country=country, bbox=bbox, zoom=zoom)
    return fetch(
        "geo/subdivisions",
        params={"country": country, "type": type, "limit": limit, "page": page},
        all_pages=all_pages,
    )


def _boundaries(
    *,
    country: Optional[str],
    bbox: Optional[tuple],
    zoom: Optional[int],
):
    try:
        import geopandas as gpd
        from shapely.geometry import shape
    except ImportError as exc:  # pragma: no cover
        raise ImportError(
            "Geometry requires the `geo` extra: pip install 'sondio[geo]'"
        ) from exc

    params = {
        "country_code": country,
        "zoom": zoom,
        "bbox": ",".join(str(v) for v in bbox) if bbox else None,
    }
    body = fetch_geojson("geo/boundaries/subdivisions", params=params)
    features = body.get("features") or []
    if not features:
        return gpd.GeoDataFrame(geometry=[], crs="EPSG:4326")
    rows = []
    geoms = []
    for f in features:
        geom = f.get("geometry")
        geoms.append(shape(geom) if geom else None)
        rows.append(f.get("properties") or {})
    return gpd.GeoDataFrame(rows, geometry=geoms, crs="EPSG:4326")
