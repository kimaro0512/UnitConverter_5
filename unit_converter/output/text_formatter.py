"""Text output formatter (FR-07, FR-11)."""

from __future__ import annotations

from unit_converter.domain.models import ConversionResult


class TextFormatter:
    """Default line-oriented output with one-decimal display rounding."""

    def format(self, result: ConversionResult) -> str:
        """FR-11: Format each conversion line per README example."""
        lines = []
        for item in result.values:
            if item.unit == result.source.unit:
                continue
            rounded = result.rounded_value(item.value)
            lines.append(
                f"{result.source.value} {result.source.unit} = {rounded} {item.unit}"
            )
        return "\n".join(lines)
