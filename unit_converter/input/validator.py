"""Input validator — business rules for quantities (FR-08, FR-10)."""

from __future__ import annotations

from unit_converter.conversion.protocols import UnitRegistryPort
from unit_converter.domain.exceptions import UnknownUnitError, ValidationError
from unit_converter.domain.models import Quantity


class InputValidator:
    """Validates parsed quantities against registry and value rules."""

    def __init__(self, registry: UnitRegistryPort) -> None:
        self._registry = registry

    def validate(self, quantity: Quantity) -> None:
        """FR-08, FR-10: Reject negative values and unknown units."""
        if quantity.value < 0:
            raise ValidationError(f"Negative value not allowed: {quantity.value}")
        if not self._registry.has_unit(quantity.unit):
            raise UnknownUnitError(f"Unknown unit: {quantity.unit}")
