from __future__ import annotations

import builtins
import os
import sys
from types import ModuleType
from unittest.mock import patch

import pytest

from sondio import config


@pytest.fixture(autouse=True)
def _clear_env(monkeypatch):
    monkeypatch.delenv("SONDIO_API_KEY", raising=False)


def test_explicit_wins():
    assert config.resolve_api_key("explicit") == "explicit"


def test_env_var_when_no_explicit(monkeypatch):
    monkeypatch.setenv("SONDIO_API_KEY", "env-key")
    assert config.resolve_api_key(None) == "env-key"


def test_colab_userdata_when_present():
    fake_userdata = ModuleType("userdata")
    fake_userdata.get = lambda name: "colab-key" if name == "SONDIO_API_KEY" else None  # type: ignore[attr-defined]
    fake_colab = ModuleType("google.colab")
    fake_colab.userdata = fake_userdata  # type: ignore[attr-defined]
    fake_google = ModuleType("google")
    fake_google.colab = fake_colab  # type: ignore[attr-defined]
    with patch.dict(sys.modules, {"google": fake_google, "google.colab": fake_colab}):
        assert config.resolve_api_key(None) == "colab-key"


def test_colab_preempts_env(monkeypatch):
    monkeypatch.setenv("SONDIO_API_KEY", "env-key")
    fake_userdata = ModuleType("userdata")
    fake_userdata.get = lambda name: "colab-key"  # type: ignore[attr-defined]
    fake_colab = ModuleType("google.colab")
    fake_colab.userdata = fake_userdata  # type: ignore[attr-defined]
    fake_google = ModuleType("google")
    fake_google.colab = fake_colab  # type: ignore[attr-defined]
    with patch.dict(sys.modules, {"google": fake_google, "google.colab": fake_colab}):
        assert config.resolve_api_key(None) == "colab-key"


def test_colab_access_denied_falls_through(monkeypatch):
    monkeypatch.setenv("SONDIO_API_KEY", "env-key")

    def _raise(name):
        raise RuntimeError("SecretNotFoundError-equivalent")

    fake_userdata = ModuleType("userdata")
    fake_userdata.get = _raise  # type: ignore[attr-defined]
    fake_colab = ModuleType("google.colab")
    fake_colab.userdata = fake_userdata  # type: ignore[attr-defined]
    fake_google = ModuleType("google")
    fake_google.colab = fake_colab  # type: ignore[attr-defined]
    with patch.dict(sys.modules, {"google": fake_google, "google.colab": fake_colab}):
        assert config.resolve_api_key(None) == "env-key"


def test_kaggle_secrets_when_present():
    class FakeClient:
        def get_secret(self, name):
            return "kaggle-key" if name == "SONDIO_API_KEY" else None

    fake_mod = ModuleType("kaggle_secrets")
    fake_mod.UserSecretsClient = FakeClient  # type: ignore[attr-defined]
    with patch.dict(sys.modules, {"kaggle_secrets": fake_mod}):
        assert config.resolve_api_key(None) == "kaggle-key"


def test_non_notebook_env_returns_none_when_empty():
    assert config.resolve_api_key(None) is None
