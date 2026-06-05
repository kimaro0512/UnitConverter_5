"""Conversion protocols (NFR-01)."""

from __future__ import annotations

from typing import Protocol

from unit_converter.domain.models import UnitDefinition


class UnitRegistryPort(Protocol):
    """Read-only registry surface used by ConversionEngine."""

    @property
    def base_unit(self) -> str: ...

    def unit_names(self) -> list[str]: ...

    def get_definition(self, name: str) -> UnitDefinition: ...

    def has_unit(self, name: str) -> bool: ...
