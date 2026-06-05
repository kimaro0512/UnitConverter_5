"""Boundary unit registration parser tests (FR-06)."""

from __future__ import annotations

import pytest


def test_boundary_FR06_parse_register_cubit() -> None:
    """FR-06: parse cubit registration string."""
    # Given
    raw = "1 cubit = 0.4572 meter"
    # When
    try:
        from unit_converter.input.unit_registration_parser import parse_unit_registration

        parse_unit_registration(raw)
    except (ModuleNotFoundError, NotImplementedError):
        pass
    # Then
    pytest.fail("Red skeleton: UnitDefinition(cubit, 0.4572)")
