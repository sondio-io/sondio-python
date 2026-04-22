"""Configuration resolution.

Priority for api_key: explicit attribute > Colab Secrets > Kaggle Secrets >
env var > ~/.sondio/config.

Colab and Kaggle don't inject secrets as env vars — they ship bespoke client
APIs. We try each import inside try/except so the SDK works identically on
Deepnote, Hex, SageMaker, Paperspace, local Jupyter, and CI (all of which
use env-var injection and fall through to step 4).
"""
from __future__ import annotations

import configparser
import os
from pathlib import Path
from typing import Optional

DEFAULT_BASE_URL = "https://api.sondio.io/api/v1"
_ENV_VAR = "SONDIO_API_KEY"


def _try_colab() -> Optional[str]:
    try:
        from google.colab import userdata  # type: ignore[import-not-found]
    except ImportError:
        return None
    try:
        key = userdata.get(_ENV_VAR)
    except Exception:
        return None
    return key or None


def _try_kaggle() -> Optional[str]:
    try:
        from kaggle_secrets import UserSecretsClient  # type: ignore[import-not-found]
    except ImportError:
        return None
    try:
        key = UserSecretsClient().get_secret(_ENV_VAR)
    except Exception:
        return None
    return key or None


def _try_config_file() -> Optional[str]:
    cfg_path = Path.home() / ".sondio" / "config"
    if not cfg_path.exists():
        return None
    parser = configparser.ConfigParser()
    try:
        parser.read(cfg_path)
    except configparser.Error:
        return None
    if parser.has_option("default", "api_key"):
        return parser.get("default", "api_key").strip() or None
    return None


def resolve_api_key(explicit: Optional[str]) -> Optional[str]:
    if explicit:
        return explicit
    for resolver in (_try_colab, _try_kaggle):
        key = resolver()
        if key:
            return key
    env = os.environ.get(_ENV_VAR)
    if env:
        return env
    return _try_config_file()


def resolve_base_url(explicit: Optional[str]) -> str:
    if explicit:
        return explicit
    return os.environ.get("SONDIO_BASE_URL", DEFAULT_BASE_URL)
