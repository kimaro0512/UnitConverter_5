"""Unit registration string parser (FR-06)."""

from __future__ import annotations

import re

from unit_converter.domain.exceptions import ParseError
from unit_converter.domain.models import UnitDefinition

_REGISTRATION_PATTERN = re.compile(
    r"^\s*1\s+(\w+)\s*=\s*([\d.]+)\s+(\w+)\s*$",
    re.IGNORECASE,
)


def parse_unit_registration(
    raw: str,
    expected_base_unit: str = "meter",
) -> UnitDefinition:
    """FR-06: Parse ``1 cubit = 0.4572 meter`` into a UnitDefinition."""
    match = _REGISTRATION_PATTERN.match(raw.strip())
    if not match:
        raise ParseError(f"Invalid registration format: {raw!r}")
    unit_name, ratio_str, base_unit = match.groups()
    if base_unit.lower() != expected_base_unit.lower():
        raise ParseError(f"Base unit must be {expected_base_unit}: {raw!r}")
    try:
        ratio = float(ratio_str)
    except ValueError as exc:
        raise ParseError(f"Invalid ratio: {ratio_str!r}") from exc
    return UnitDefinition(name=unit_name.lower(), ratio_to_base=ratio)
