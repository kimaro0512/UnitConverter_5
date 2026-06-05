"""Table output formatter (FR-07)."""

from __future__ import annotations

from unit_converter.domain.models import ConversionResult
from unit_converter.output.presentation import all_converted_values


class TableFormatter:
    """Simple fixed-width table of conversion values (full precision export)."""

    def format(self, result: ConversionResult) -> str:
        header = "unit    | value"
        separator = "--------+--------"
        rows = [
            f"{item.unit:<7} | {item.value}"
            for item in all_converted_values(result)
        ]
        return "\n".join([header, separator, *rows])
