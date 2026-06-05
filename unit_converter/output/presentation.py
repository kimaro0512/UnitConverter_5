"""Output presentation helpers — export vs text display (FR-07, FR-11)."""

from __future__ import annotations

from unit_converter.domain.models import ConversionResult, ConvertedValue
from unit_converter.output.rounding import round_for_display


def all_converted_values(result: ConversionResult) -> list[ConvertedValue]:
    """Export formats: all units at full precision (includes source)."""
    return list(result.values)


def text_display_lines(result: ConversionResult) -> list[str]:
    """Text format: non-source units with one-decimal display rounding."""
    lines: list[str] = []
    for item in all_converted_values(result):
        if item.unit == result.source.unit:
            continue
        rounded = round_for_display(item.value)
        lines.append(
            f"{result.source.value} {result.source.unit} = {rounded} {item.unit}"
        )
    return lines
