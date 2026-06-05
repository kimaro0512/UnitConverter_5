"""Boundary formatter tests (FR-07, FR-11)."""

from __future__ import annotations

import pytest


def test_boundary_FR07_json_format(sample_conversion_result) -> None:
    """FR-07: JsonFormatter output mentions feet."""
    # Given
    # When
    try:
        from unit_converter.output.json_formatter import JsonFormatter

        if sample_conversion_result is not None:
            JsonFormatter().format(sample_conversion_result)
    except (ModuleNotFoundError, NotImplementedError):
        pass
    # Then
    pytest.fail("Red skeleton: 'feet' in JSON output")


def test_boundary_FR07_csv_format(sample_conversion_result) -> None:
    """FR-07: CsvFormatter produces comma-separated output."""
    # Given
    # When
    try:
        from unit_converter.output.csv_formatter import CsvFormatter

        if sample_conversion_result is not None:
            CsvFormatter().format(sample_conversion_result)
    except (ModuleNotFoundError, NotImplementedError):
        pass
    # Then
    pytest.fail("Red skeleton: comma-separated CSV output")


def test_boundary_FR07_table_format(sample_conversion_result) -> None:
    """FR-07: TableFormatter produces header and rows."""
    # Given
    # When
    try:
        from unit_converter.output.table_formatter import TableFormatter

        if sample_conversion_result is not None:
            TableFormatter().format(sample_conversion_result)
    except (ModuleNotFoundError, NotImplementedError):
        pass
    # Then
    pytest.fail("Red skeleton: table header and rows in output")


def test_boundary_FR07_factory_all_formats() -> None:
    """FR-07: formatter factory exposes text, json, csv, table."""
    # Given
    # When
    try:
        from unit_converter.output.formatter_factory import (
            get_formatter,
            registered_format_names,
        )

        registered_format_names()
        get_formatter("text")
    except (ModuleNotFoundError, NotImplementedError, ValueError):
        pass
    # Then
    pytest.fail("Red skeleton: factory supports text/json/csv/table")


def test_boundary_FR11_text_output_one_decimal(sample_conversion_result) -> None:
    """FR-11: TextFormatter shows README one-decimal example."""
    # Given
    # When
    try:
        from unit_converter.output.text_formatter import TextFormatter

        if sample_conversion_result is not None:
            TextFormatter().format(sample_conversion_result)
    except (ModuleNotFoundError, NotImplementedError):
        pass
    # Then
    pytest.fail("Red skeleton: output contains '8.2' and '2.7'")
