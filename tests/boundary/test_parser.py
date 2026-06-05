"""Boundary parser tests (FR-01, FR-09)."""

from __future__ import annotations

import pytest

from unit_converter.domain.exceptions import ParseError
from unit_converter.input.parser import parse_unit_value


def test_boundary_FR01_parse_valid_unit_value() -> None:
    """FR-01: parse meter:2.5 into Quantity."""
    # Given
    raw = "meter:2.5"
    # When
    quantity = parse_unit_value(raw)
    # Then
    assert quantity.unit == "meter"
    assert quantity.value == 2.5


def test_boundary_FR01_parse_trims_whitespace() -> None:
    """FR-01: trim whitespace around unit:value."""
    # Given
    raw = " meter:2.5 "
    # When
    quantity = parse_unit_value(raw)
    # Then
    assert quantity.unit == "meter"
    assert quantity.value == 2.5


def test_boundary_FR09_reject_missing_colon() -> None:
    """FR-09: reject meter2.5 without colon."""
    # Given
    raw = "meter2.5"
    # When / Then
    with pytest.raises(ParseError):
        parse_unit_value(raw)


def test_boundary_FR09_reject_non_numeric() -> None:
    """FR-09: reject non-numeric value."""
    # Given
    raw = "meter:abc"
    # When / Then
    with pytest.raises(ParseError):
        parse_unit_value(raw)


def test_boundary_FR09_reject_bare_unit() -> None:
    """FR-09: reject bare unit string."""
    # Given
    raw = "meter"
    # When / Then
    with pytest.raises(ParseError):
        parse_unit_value(raw)


def test_boundary_FR09_reject_bare_non_unit() -> None:
    """FR-09: reject bare non-unit string."""
    # Given
    raw = "abc"
    # When / Then
    with pytest.raises(ParseError):
        parse_unit_value(raw)


def test_boundary_FR09_reject_extra_colon() -> None:
    """FR-09: reject extra colon in input."""
    # Given
    raw = "meter:2.5:extra"
    # When / Then
    with pytest.raises(ParseError):
        parse_unit_value(raw)
