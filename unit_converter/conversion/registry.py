"""Unit registry — register and lookup units (FR-03, FR-06, NFR-01)."""

from __future__ import annotations

from unit_converter.domain.exceptions import UnknownUnitError
from unit_converter.domain.models import UnitDefinition


class UnitRegistry:
    """Stores unit definitions keyed by name; ratios are relative to base_unit."""

    def __init__(self, base_unit: str = "meter") -> None:
        self._base_unit = base_unit
        self._units: dict[str, UnitDefinition] = {}

    @property
    def base_unit(self) -> str:
        return self._base_unit

    def register(self, definition: UnitDefinition) -> None:
        """FR-06: Add or replace a unit definition."""
        self._units[definition.name] = definition

    def register_many(self, definitions: list[UnitDefinition]) -> None:
        """FR-03: Bulk-register unit definitions (e.g. default meter/feet/yard)."""
        for definition in definitions:
            self.register(definition)

    def has_unit(self, name: str) -> bool:
        return name in self._units

    def unit_names(self) -> list[str]:
        return sorted(self._units.keys())

    def get_definition(self, name: str) -> UnitDefinition:
        if name not in self._units:
            raise UnknownUnitError(f"Unknown unit: {name}")
        return self._units[name]
