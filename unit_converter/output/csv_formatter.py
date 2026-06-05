"""CSV output formatter (FR-07)."""

from __future__ import annotations

from unit_converter.domain.models import ConversionResult


class CsvFormatter:
    """Comma-separated unit/value rows."""

    def format(self, result: ConversionResult) -> str:
        lines = ["unit,value"]
        for item in result.values:
            lines.append(f"{item.unit},{item.value}")
        return "\n".join(lines)
