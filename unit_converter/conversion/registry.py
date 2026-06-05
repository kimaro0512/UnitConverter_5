"""Unit registry — register and lookup units (FR-03, FR-06, NFR-01)."""

from __future__ import annotations

from unit_converter.domain.exceptions import RegistryKeyError
from unit_converter.domain.models import UnitDefinition


class UnitRegistry:
    """Immutable-style registry: register returns a new instance (FR-06, R2)."""

    def __init__(
        self,
        base_unit: str = "meter",
        units: dict[str, UnitDefinition] | None = None,
    ) -> None:
        self._base_unit = base_unit
        self._units = dict(units) if units is not None else {}

    @property
    def base_unit(self) -> str:
        return self._base_unit

    def register(self, definition: UnitDefinition) -> UnitRegistry:
        """FR-06: Return a new registry including the unit definition."""
        new_units = {**self._units, definition.name: definition}
        return UnitRegistry(self._base_unit, new_units)

    def register_many(self, definitions: list[UnitDefinition]) -> UnitRegistry:
        """FR-03: Return a new registry with all definitions applied."""
        registry = self
        for definition in definitions:
            registry = registry.register(definition)
        return registry

    def has_unit(self, name: str) -> bool:
        return name in self._units

    def unit_names(self) -> list[str]:
        return sorted(self._units.keys())

    def get_definition(self, name: str) -> UnitDefinition:
        if name not in self._units:
            raise RegistryKeyError(f"Unit not in registry: {name}")
        return self._units[name]
