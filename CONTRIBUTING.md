# Contributing to sondio

Thanks for taking the time to contribute.

## Development setup

```bash
git clone https://github.com/sondio-io/sondio-python
cd sondio-python
python -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
pytest
```

All 20+ tests should pass locally without a Sondio API key. The suite uses
`respx` to stub HTTP calls; nothing hits the network.

## Pull requests

- Keep each PR focused. One change per PR is easier to review and revert.
- Add or update tests for any behavior change.
- Add a `## [Unreleased]` entry to `CHANGELOG.md` for user-visible changes.
- Ensure `pytest` passes locally. CI runs against Python 3.10 through 3.13.
- Follow the existing module structure (see `docs/reference/dataset-naming.md`
  in the Sondio backend repo for the naming conventions that govern both
  API paths and SDK namespaces).

## Adding a new endpoint

1. Confirm the backend route exists and returns the canonical
   `{ items, pagination, meta? }` envelope.
2. Add a module under `src/sondio/` at the path that matches the dataset
   naming convention (vertical-rule datasets live at the top level or under
   `sondio.<vertical>`; agency-rule datasets live under
   `sondio.<country>.<agency>`).
3. Register any numeric or datetime columns with `make_coercer` so they
   come back as proper dtypes.
4. Add a test in `tests/` stubbing the endpoint with `respx`.
5. Update `README.md` if the module is part of the quickstart.

## Reporting issues

- Authentication / rate-limit issues: include the exact error message from
  `SondioAPIError` (includes the status code and truncated body).
- Data quality issues: please report these on the Sondio feedback page at
  <https://sondio.io/feedback> — those reach the data team directly.
- SDK bugs: open an issue on this repo with a minimal reproducer.

## Releasing (maintainers)

1. Bump `version` in `pyproject.toml` and `src/sondio/_version.py`.
2. Add a dated section to `CHANGELOG.md`.
3. `python -m build && twine upload dist/*`.
4. Tag and push: `git tag vX.Y.Z && git push origin vX.Y.Z`.
