"""Conversion engine — convert via base unit (FR-02, FR-04, NFR-01, NFR-06)."""

from __future__ import annotations

from unit_converter.conversion.protocols import UnitRegistryPort
from unit_converter.domain.models import ConversionResult, ConvertedValue, Quantity


class ConversionEngine:
    """Converts a quantity to all units in the registry using base-unit hub math."""

    def __init__(self, registry: UnitRegistryPort) -> None:
        self._registry = registry

    def convert(self, quantity: Quantity) -> ConversionResult:
        """FR-02, FR-04: Convert input to every registered unit via meter hub."""
        source = self._registry.get_definition(quantity.unit)
        base_value = quantity.value / source.ratio_to_base
        values = [
            ConvertedValue(
                unit=name,
                value=base_value * self._registry.get_definition(name).ratio_to_base,
            )
            for name in self._registry.unit_names()
        ]
        return ConversionResult(source=quantity, values=values)
