from __future__ import annotations

import pytest

import sondio


@pytest.fixture(autouse=True)
def _reset_config():
    """Isolate module-level config across tests."""
    prev_key = sondio.api_key
    prev_url = sondio.base_url
    sondio.api_key = "sk_sondio_test"
    sondio.base_url = "https://api.test.local/api/v1"
    yield
    sondio.api_key = prev_key
    sondio.base_url = prev_url
