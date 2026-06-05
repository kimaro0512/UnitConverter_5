"""Structured error codes for boundary/golden output (FR-08, FR-09, FR-10)."""

from __future__ import annotations

from enum import Enum


class ErrorCode(Enum):
    """E00x + NAME — golden master and CLI error taxonomy."""

    NEGATIVE_VALUE = ("E008", "NEGATIVE_VALUE")
    PARSE_ERROR = ("E009", "PARSE_ERROR")
    UNKNOWN_UNIT = ("E010", "UNKNOWN_UNIT")

    @property
    def code(self) -> str:
        return self.value[0]

    @property
    def name_label(self) -> str:
        return self.value[1]
