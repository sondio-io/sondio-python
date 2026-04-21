"""
Sondio -- The unified Python interface for energy and environmental data.

This package is under active development. Visit https://sondio.io/developers
for updates and early access.

Usage (coming soon):

    import sondio

    sondio.api_key = "sk_sondio_..."
    wells = sondio.wells(state="TX", basin="permian")
    quakes = sondio.earthquakes(min_magnitude=3.0)
"""

__version__ = "0.0.1"

api_key: str | None = None
"""Your Sondio API key. Set via sondio.api_key = "sk_sondio_..." or SONDIO_API_KEY env var."""


def _not_yet() -> None:
    raise NotImplementedError(
        "sondio SDK is not yet released. "
        "Visit https://sondio.io/developers for updates and early access."
    )


# Top-level convenience -- most common queries
def wells(**kwargs):  # noqa: D103
    _not_yet()

def well(api_number: str, **kwargs):  # noqa: D103
    _not_yet()

def production(api_number: str, **kwargs):  # noqa: D103
    _not_yet()

def permits(**kwargs):  # noqa: D103
    _not_yet()

def incidents(**kwargs):  # noqa: D103
    _not_yet()

def earthquakes(**kwargs):  # noqa: D103
    _not_yet()

def ghg_facilities(**kwargs):  # noqa: D103
    _not_yet()
