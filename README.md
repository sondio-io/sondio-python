# sondio

Python SDK for the [Sondio](https://sondio.io) data platform. Energy and
environmental data as pandas DataFrames.

```bash
pip install sondio              # core
pip install 'sondio[geo]'       # adds geopandas for boundary polygons
```

## Quickstart

```python
import sondio

sondio.api_key = "sk_sondio_..."  # or set SONDIO_API_KEY

# Vertical-rule datasets — country is a parameter, not a prefix
wells  = sondio.oilgas.wells(country="US", state="TX", basin="permian")
quakes = sondio.earthquakes(state="TX", min_mag=3.0, days=30)

# Agency-rule datasets: sondio.<country>.<agency>.<resource>
ae     = sondio.us.epa.aquifer_exemptions(state="TX")
ghg    = sondio.us.ghg.facilities(state="TX")
pl     = sondio.us.phmsa.pipeline_incidents(state="TX")
npdes  = sondio.us.npdes.permits(state="TX")

# Geographic reference data
states = sondio.geo.subdivisions(country="US")
states_geo = sondio.geo.subdivisions(country="US", with_geometry=True)  # GeoDataFrame
```

Every call returns a `pandas.DataFrame` — or a `geopandas.GeoDataFrame` when
you ask for geometry.

## Configuration

```python
import sondio
sondio.api_key  = "sk_sondio_..."                   # explicit
sondio.base_url = "http://localhost:8791/api/v1"    # dev override
```

Resolution order: explicit attribute → `SONDIO_API_KEY` env var →
`~/.sondio/config` (`[default]` section, `api_key = ...`).

## Pagination

Opt-in to protect against unintentional 3M-row walks:

```python
# First page only (default). Emits a UserWarning if more pages exist.
wells = sondio.oilgas.wells(country="US", state="TX")

# Full iteration
wells = sondio.oilgas.wells(country="US", state="TX", all_pages=True)

# Specific page
wells = sondio.oilgas.wells(country="US", state="TX", page=3)
```

Auto-pagination is capped at 500 pages — hitting the cap raises a warning.

## Type coercion

Several API columns come back as strings (`magnitude`, `depth_ft`,
`total_co2e`). The SDK coerces known numeric/datetime columns per endpoint;
unknown columns pass through untouched.

## Errors

```python
from sondio import SondioError, SondioAPIError

try:
    sondio.earthquakes()
except SondioAPIError as e:
    print(e.status_code, e.body)
except SondioError as e:
    print("config problem:", e)
```

## Namespace shape

Matches the Sondio [dataset naming convention](https://github.com/sondio-io/sondio/blob/main/docs/reference/dataset-naming.md):

| Category                    | Shape                                               | Example                                  |
|-----------------------------|-----------------------------------------------------|------------------------------------------|
| Vertical-rule               | `sondio.<vertical>.<resource>(country=...)`          | `sondio.oilgas.wells(country="US")`      |
| Vertical-rule, global       | `sondio.<resource>(...)`                             | `sondio.earthquakes(...)`                |
| Agency-rule                 | `sondio.<country>.<agency>.<resource>(...)`          | `sondio.us.epa.aquifer_exemptions(...)`  |
| Geographic reference        | `sondio.geo.<resource>(...)`                         | `sondio.geo.subdivisions(...)`           |

## License

MIT — see [LICENSE](LICENSE).
