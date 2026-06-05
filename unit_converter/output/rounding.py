"""Display rounding policy (FR-11)."""

from __future__ import annotations

DEFAULT_DECIMAL_PLACES = 1


def round_for_display(value: float, places: int | None = None) -> float:
    """FR-11: Round for human-readable output (README one-decimal example)."""
    decimal_places = DEFAULT_DECIMAL_PLACES if places is None else places
    return round(value, decimal_places)
