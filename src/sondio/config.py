"""Configuration resolution.

Priority: explicit module attribute > env var > ~/.sondio/config.
"""
from __future__ import annotations

import configparser
import os
from pathlib import Path
from typing import Optional

DEFAULT_BASE_URL = "https://api.sondio.io/api/v1"


def resolve_api_key(explicit: Optional[str]) -> Optional[str]:
    if explicit:
        return explicit
    env = os.environ.get("SONDIO_API_KEY")
    if env:
        return env
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


def resolve_base_url(explicit: Optional[str]) -> str:
    if explicit:
        return explicit
    return os.environ.get("SONDIO_BASE_URL", DEFAULT_BASE_URL)
