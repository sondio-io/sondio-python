"""Geographic reference data — subdivisions, basins, boundaries.

Endpoints that return geometry produce a GeoDataFrame; install the
`sondio[geo]` extra for geopandas support.
"""
from __future__ import annotations

from .subdivisions import subdivisions

__all__ = ["subdivisions"]
