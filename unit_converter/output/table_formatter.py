"""Table output formatter (FR-07)."""

from __future__ import annotations

from unit_converter.domain.models import ConversionResult


class TableFormatter:
    """Simple fixed-width table of conversion values."""

    def format(self, result: ConversionResult) -> str:
        header = "unit    | value"
        separator = "--------+--------"
        rows = [
            f"{item.unit:<7} | {item.value}"
            for item in result.values
        ]
        return "\n".join([header, separator, *rows])
