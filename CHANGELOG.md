# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.2] - 2026-04-22

### Added

- Platform-aware API key resolution. `sondio.api_key` now resolves from
  (in order) explicit attribute → Colab Secrets (`google.colab.userdata`)
  → Kaggle Secrets (`kaggle_secrets.UserSecretsClient`) → `SONDIO_API_KEY`
  env var → `~/.sondio/config`. Notebook users on Colab and Kaggle no
  longer need platform-specific boilerplate in every setup cell.
- `py.typed` marker for PEP 561 — IDEs and type checkers now recognize
  the package as typed and surface the type hints that shipped since 0.1.0.
- `CHANGELOG.md`, `CONTRIBUTING.md`, and GitHub Actions CI running pytest
  on Python 3.10–3.13.

## [0.1.1] - 2026-04-22

### Added

- `sondio.oilgas.production(well_id)` — per-well monthly production history.
- `sondio.wind_turbines(...)` — USWTDB fleet (75k turbines).
- `sondio.rail_lines(...)` — BTS NTAD (302k segments, tri-national).
- `sondio.us.cdc.svi_tracts(...)` — CDC Social Vulnerability Index tracts.
- `records_key` parameter on `fetch()` for endpoints that use a non-standard
  response envelope.

## [0.1.0] - 2026-04-22

### Added

- Initial real release. Replaces the 0.0.2 placeholder on PyPI.
- 11 endpoint wrappers across `sondio.oilgas.*`, `sondio.earthquakes`,
  `sondio.geo.subdivisions`, `sondio.us.epa.*`, `sondio.us.ghg.*`,
  `sondio.us.npdes.*`, `sondio.us.phmsa.*`.
- Bearer authentication, opt-in pagination (`all_pages=True`), retries on
  429/5xx with `Retry-After` honoring, typed coercion of numeric/datetime
  columns, `geopandas.GeoDataFrame` support for geometry-returning
  endpoints.
- `SondioError` / `SondioAPIError` exceptions.

## [0.0.2] - 2026-04-21

### Added

- Placeholder release to reserve the PyPI name. Printed "coming soon" on
  any call. Superseded by 0.1.0.

## [0.0.1] - 2026-04-20

### Yanked

- Initial placeholder. Yanked due to a typo in `LICENSE`; see 0.0.2.
