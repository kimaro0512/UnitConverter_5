"""Boundary unit registration parser tests (FR-06)."""

from __future__ import annotations

import pytest

from unit_converter.input.unit_registration_parser import parse_unit_registration


def test_boundary_FR06_parse_register_cubit() -> None:
    """FR-06: parse cubit registration string."""
    # Given
    raw = "1 cubit = 0.4572 meter"
    # When
    definition = parse_unit_registration(raw)
    # Then
    assert definition.name == "cubit"
    assert definition.ratio_to_base == pytest.approx(0.4572)
