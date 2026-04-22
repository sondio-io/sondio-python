"""Oil & gas — vertical-rule datasets.

Country is a parameter (e.g. `country="US"`), not a URL prefix.
"""
from __future__ import annotations

from .incidents import incidents
from .permits import permits
from .wells import wells

__all__ = ["incidents", "permits", "wells"]
