"""Entity registry tests (FR-06)."""

from __future__ import annotations

from unit_converter.conversion.engine import ConversionEngine
from unit_converter.domain.models import Quantity, UnitDefinition


def test_entity_FR06_registry_stores_cubit(empty_registry) -> None:
    """FR-06: registry stores cubit after registration."""
    # Given
    cubit = UnitDefinition(name="cubit", ratio_to_base=0.4572)
    # When
    registry = empty_registry.register(cubit)
    # Then
    assert registry.has_unit("cubit")


def test_entity_FR06_cubit_in_conversion_output(empty_registry) -> None:
    """FR-06: cubit appears in conversion output after registration."""
    # Given
    meter = UnitDefinition(name="meter", ratio_to_base=1.0)
    cubit = UnitDefinition(name="cubit", ratio_to_base=0.4572)
    registry = empty_registry.register_many([meter, cubit])
    engine = ConversionEngine(registry)
    # When
    result = engine.convert(Quantity(unit="meter", value=1.0))
    units = {item.unit for item in result.values}
    # Then
    assert "cubit" in units
