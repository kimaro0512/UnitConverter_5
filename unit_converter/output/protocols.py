"""Output formatter protocols (FR-07, NFR-01)."""

from __future__ import annotations

from typing import Protocol

from unit_converter.domain.models import ConversionResult


class OutputFormatter(Protocol):
    """Format a ConversionResult as a string."""

    def format(self, result: ConversionResult) -> str: ...
