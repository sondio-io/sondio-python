"""Sondio — Python SDK for energy and environmental data.

Thin wrapper over the Sondio REST API. Every call returns a pandas
DataFrame (or GeoDataFrame for geographic results).

Quickstart:

    import sondio
    sondio.api_key = "sk_sondio_..."  # or set SONDIO_API_KEY

    # Vertical-rule datasets (country as a parameter)
    wells  = sondio.oilgas.wells(country="US", state="TX")
    quakes = sondio.earthquakes(state="TX", min_mag=3.0, days=30)

    # Agency-rule datasets live under sondio.<country>.<agency>.<resource>
    ae     = sondio.us.epa.aquifer_exemptions(state="TX")
    ghg    = sondio.us.ghg.facilities(state="TX")
    pl     = sondio.us.phmsa.pipeline_incidents(state="TX")

    # Geographic reference data (requires `sondio[geo]`)
    states = sondio.geo.subdivisions(country="US")

Pagination is opt-in. A call without `all_pages=True` returns the first
page and warns if more exist. See README.md for details.
"""
from __future__ import annotations

api_key: str | None = None
"""Your Sondio API key. Set via sondio.api_key = ... or SONDIO_API_KEY env var."""

base_url: str | None = None
"""Override the API base URL. Defaults to https://api.sondio.io/api/v1."""

from ._version import __version__
from . import geo, oilgas, us
from .client import SondioAPIError, SondioError
from .earthquakes import earthquakes
from .rail_lines import rail_lines
from .wind_turbines import wind_turbines

__all__ = [
    "__version__",
    "api_key",
    "base_url",
    "earthquakes",
    "geo",
    "oilgas",
    "rail_lines",
    "us",
    "wind_turbines",
    "SondioAPIError",
    "SondioError",
]
