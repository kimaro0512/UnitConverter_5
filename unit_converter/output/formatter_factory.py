"""Formatter factory (FR-07, OCP)."""

from __future__ import annotations

from unit_converter.output.csv_formatter import CsvFormatter
from unit_converter.output.json_formatter import JsonFormatter
from unit_converter.output.protocols import OutputFormatter
from unit_converter.output.table_formatter import TableFormatter
from unit_converter.output.text_formatter import TextFormatter

_FORMATTERS: dict[str, type[OutputFormatter]] = {
    "text": TextFormatter,
    "json": JsonFormatter,
    "csv": CsvFormatter,
    "table": TableFormatter,
}


def registered_format_names() -> list[str]:
    """Return all supported output format names."""
    return sorted(_FORMATTERS.keys())


def get_formatter(name: str) -> OutputFormatter:
    """FR-07: Resolve a formatter by name."""
    formatter_cls = _FORMATTERS.get(name)
    if formatter_cls is None:
        raise ValueError(f"Unknown format: {name}")
    return formatter_cls()
