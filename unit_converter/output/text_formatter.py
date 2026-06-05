"""Text output formatter (FR-07, FR-11)."""

from __future__ import annotations

from unit_converter.domain.models import ConversionResult
from unit_converter.output.presentation import text_display_lines


class TextFormatter:
    """Default line-oriented output with one-decimal display rounding."""

    def format(self, result: ConversionResult) -> str:
        """FR-11: Format each conversion line per README example."""
        return "\n".join(text_display_lines(result))
