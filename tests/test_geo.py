from __future__ import annotations

import httpx
import respx

import sondio

pytest_plugins = ()


def _env(items):
    return {"items": items, "pagination": {"page": 1, "limit": len(items), "hasMore": False}}


@respx.mock
def test_subdivisions_without_geometry_returns_dataframe():
    respx.get("https://api.test.local/api/v1/geo/subdivisions").mock(
        return_value=httpx.Response(200, json=_env([
            {"id": "1", "country_code": "US", "code": "US-TX", "local_code": "TX", "name": "Texas"},
        ]))
    )
    df = sondio.geo.subdivisions(country="US", page=1)
    assert "geometry" not in df.columns
    assert df["local_code"].iloc[0] == "TX"


@respx.mock
def test_subdivisions_with_geometry_returns_geodataframe():
    pytest = __import__("pytest")
    gpd = pytest.importorskip("geopandas")

    feature_collection = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {"type": "Polygon", "coordinates": [[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]]},
                "properties": {"id": "1", "code": "US-TX", "local_code": "TX", "name": "Texas"},
            },
        ],
    }
    respx.get("https://api.test.local/api/v1/geo/boundaries/subdivisions").mock(
        return_value=httpx.Response(200, json=feature_collection)
    )
    gdf = sondio.geo.subdivisions(country="US", with_geometry=True)
    assert isinstance(gdf, gpd.GeoDataFrame)
    assert gdf.crs == "EPSG:4326"
    assert gdf["local_code"].iloc[0] == "TX"
    assert gdf.geometry.iloc[0].geom_type == "Polygon"


@respx.mock
def test_subdivisions_with_geometry_empty_returns_empty_geodataframe():
    pytest = __import__("pytest")
    gpd = pytest.importorskip("geopandas")

    respx.get("https://api.test.local/api/v1/geo/boundaries/subdivisions").mock(
        return_value=httpx.Response(200, json={"type": "FeatureCollection", "features": []})
    )
    gdf = sondio.geo.subdivisions(country="XX", with_geometry=True)
    assert isinstance(gdf, gpd.GeoDataFrame)
    assert len(gdf) == 0
