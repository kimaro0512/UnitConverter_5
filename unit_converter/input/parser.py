"""Input parser — unit:value strings to Quantity (FR-01, FR-09)."""

from __future__ import annotations

from unit_converter.domain.exceptions import ParseError
from unit_converter.domain.models import Quantity


def parse_unit_value(raw: str) -> Quantity:
    """FR-01: Parse ``unit:value`` into a Quantity."""
    text = raw.strip()
    if ":" not in text:
        raise ParseError(f"Invalid format: {raw!r}")
    parts = text.split(":")
    if len(parts) != 2:
        raise ParseError(f"Invalid format: {raw!r}")
    unit, value_str = parts[0].strip(), parts[1].strip()
    if not unit:
        raise ParseError(f"Missing unit: {raw!r}")
    try:
        value = float(value_str)
    except ValueError as exc:
        raise ParseError(f"Invalid number: {value_str!r}") from exc
    return Quantity(unit=unit, value=value)
