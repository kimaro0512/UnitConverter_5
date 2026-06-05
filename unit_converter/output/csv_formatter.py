"""CSV output formatter (FR-07)."""

from __future__ import annotations

from unit_converter.domain.models import ConversionResult
from unit_converter.output.presentation import all_converted_values


class CsvFormatter:
    """Comma-separated unit/value rows (full precision export)."""

    def format(self, result: ConversionResult) -> str:
        lines = ["unit,value"]
        for item in all_converted_values(result):
            lines.append(f"{item.unit},{item.value}")
        return "\n".join(lines)
