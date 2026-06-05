"""Boundary formatter tests (FR-07, FR-11)."""

from __future__ import annotations

from unit_converter.output.csv_formatter import CsvFormatter
from unit_converter.output.formatter_factory import get_formatter, registered_format_names
from unit_converter.output.json_formatter import JsonFormatter
from unit_converter.output.table_formatter import TableFormatter
from unit_converter.output.text_formatter import TextFormatter


def test_boundary_FR07_json_format(sample_conversion_result) -> None:
    """FR-07: JsonFormatter output mentions feet."""
    # Given / When
    output = JsonFormatter().format(sample_conversion_result)
    # Then
    assert "feet" in output


def test_boundary_FR07_csv_format(sample_conversion_result) -> None:
    """FR-07: CsvFormatter produces comma-separated output."""
    # Given / When
    output = CsvFormatter().format(sample_conversion_result)
    # Then
    assert "," in output


def test_boundary_FR07_table_format(sample_conversion_result) -> None:
    """FR-07: TableFormatter produces header and rows."""
    # Given / When
    output = TableFormatter().format(sample_conversion_result)
    # Then
    assert "unit" in output.lower()
    assert "feet" in output


def test_boundary_FR07_factory_all_formats() -> None:
    """FR-07: formatter factory exposes text, json, csv, table."""
    # Given / When
    names = registered_format_names()
    # Then
    assert set(names) == {"text", "json", "csv", "table"}
    get_formatter("text")
    get_formatter("json")
    get_formatter("csv")
    get_formatter("table")


def test_boundary_FR11_text_output_one_decimal(sample_conversion_result) -> None:
    """FR-11: TextFormatter shows README one-decimal example."""
    # Given / When
    output = TextFormatter().format(sample_conversion_result)
    # Then
    assert "8.2" in output
    assert "2.7" in output
