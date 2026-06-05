"""Control conversion service tests (FR-02, FR-06, FR-07, FR-09)."""

from __future__ import annotations

import json

import pytest

from unit_converter.domain.exceptions import ParseError, ValidationError


def test_control_FR02_service_convert_input(conversion_service) -> None:
    """FR-02: convert_input parses and converts meter:2.5."""
    # Given
    raw = "meter:2.5"
    # When
    result = conversion_service.convert_input(raw)
    # Then
    assert result.source.value == 2.5
    assert result.source.unit == "meter"


def test_control_FR02_service_returns_all_unit_values(conversion_service) -> None:
    """FR-02: convert_input returns feet, yard, and meter."""
    # Given
    raw = "meter:1.0"
    # When
    result = conversion_service.convert_input(raw)
    units = {item.unit for item in result.values}
    # Then
    assert units == {"meter", "feet", "yard"}


def test_control_FR06_service_register_and_convert(conversion_service) -> None:
    """FR-06: service registers cubit and converts."""
    # Given
    conversion_service.register_unit("1 cubit = 0.4572 meter")
    # When
    result = conversion_service.convert_input("meter:1.0")
    units = {item.unit for item in result.values}
    # Then
    assert "cubit" in units


def test_control_FR07_service_format_json(
    conversion_service,
    sample_conversion_result,
) -> None:
    """FR-07: format_result produces valid JSON."""
    from unit_converter.output.json_formatter import JsonFormatter

    # Given
    formatter = JsonFormatter()
    # When
    output = conversion_service.format_result(sample_conversion_result, formatter)
    # Then
    parsed = json.loads(output)
    assert "feet" in output
    assert parsed["source"]["unit"] == "meter"


def test_control_FR09_service_invalid_format(conversion_service) -> None:
    """FR-09: convert_input rejects invalid format."""
    # Given
    raw = "invalid"
    # When / Then
    with pytest.raises((ParseError, ValidationError)):
        conversion_service.convert_input(raw)
