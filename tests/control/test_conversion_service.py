"""Control conversion service tests (FR-02, FR-06, FR-07, FR-09)."""

from __future__ import annotations

import pytest


def test_control_FR02_service_convert_input(conversion_service) -> None:
    """FR-02: convert_input parses and converts meter:2.5."""
    # Given
    raw = "meter:2.5"
    # When
    try:
        if conversion_service is not None:
            conversion_service.convert_input(raw)
    except (ModuleNotFoundError, NotImplementedError):
        pass
    # Then
    pytest.fail("Red skeleton: ConversionResult with source.value=2.5")


def test_control_FR02_service_returns_all_unit_values(conversion_service) -> None:
    """FR-02: convert_input returns feet, yard, and meter."""
    # Given
    raw = "meter:1.0"
    # When
    try:
        if conversion_service is not None:
            conversion_service.convert_input(raw)
    except (ModuleNotFoundError, NotImplementedError):
        pass
    # Then
    pytest.fail("Red skeleton: result includes feet, yard, meter")


def test_control_FR06_service_register_and_convert(conversion_service) -> None:
    """FR-06: service registers cubit and converts."""
    # Given
    raw = "meter:1.0"
    registration = "1 cubit = 0.4572 meter"
    _ = registration
    # When
    try:
        if conversion_service is not None:
            conversion_service.convert_input(raw)
    except (ModuleNotFoundError, NotImplementedError):
        pass
    # Then
    pytest.fail("Red skeleton: conversion output includes cubit")


def test_control_FR07_service_format_json(
    conversion_service,
    sample_conversion_result,
) -> None:
    """FR-07: format_result produces valid JSON."""
    # Given
    # When
    try:
        from unit_converter.output.json_formatter import JsonFormatter

        if conversion_service is not None and sample_conversion_result is not None:
            formatter = JsonFormatter()
            conversion_service.format_result(sample_conversion_result, formatter)
    except (ModuleNotFoundError, NotImplementedError):
        pass
    # Then
    pytest.fail("Red skeleton: format_result returns valid JSON string")


def test_control_FR09_service_invalid_format(conversion_service) -> None:
    """FR-09: convert_input rejects invalid format."""
    # Given
    raw = "invalid"
    # When
    try:
        if conversion_service is not None:
            conversion_service.convert_input(raw)
    except (ModuleNotFoundError, NotImplementedError):
        pass
    # Then
    pytest.fail("Red skeleton: ParseError or ValidationError for invalid input")
