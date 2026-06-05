"""Entity conversion engine tests (FR-02, FR-03, FR-04)."""

from __future__ import annotations

import pytest


def test_entity_FR02_convert_to_all_registered_units(engine) -> None:
    """FR-02: meter 2.5 converts to all registered units."""
    from unit_converter.domain.models import Quantity

    # Given
    quantity = Quantity(unit="meter", value=2.5)
    # When
    result = engine.convert(quantity)
    feet = next(item.value for item in result.values if item.unit == "feet")
    yard = next(item.value for item in result.values if item.unit == "yard")
    # Then
    assert feet == pytest.approx(8.2021)
    assert yard == pytest.approx(2.7340, abs=1e-3)


def test_entity_FR02_feet_input_converts_to_meter(engine) -> None:
    """FR-02: feet input converts back to meter."""
    from unit_converter.domain.models import Quantity

    # Given
    quantity = Quantity(unit="feet", value=8.2021)
    # When
    result = engine.convert(quantity)
    meter = next(item.value for item in result.values if item.unit == "meter")
    # Then
    assert meter == pytest.approx(2.5)


def test_entity_FR03_default_units_in_registry(default_registry) -> None:
    """FR-03: default registry lists meter, feet, yard."""
    # Given — default_registry loaded from config/units.json
    # When
    names = default_registry.unit_names()
    # Then
    assert set(names) == {"meter", "feet", "yard"}


def test_entity_FR04_meter_hub_converts_to_feet_and_yard(engine) -> None:
    """FR-04: meter hub converts 1.0 m to feet and yard."""
    from unit_converter.domain.models import Quantity

    # Given
    quantity = Quantity(unit="meter", value=1.0)
    # When
    result = engine.convert(quantity)
    feet = next(item.value for item in result.values if item.unit == "feet")
    yard = next(item.value for item in result.values if item.unit == "yard")
    # Then
    assert feet == pytest.approx(3.28084)
    assert yard == pytest.approx(1.09361)


def test_entity_FR04_feet_yard_cross_consistent(engine) -> None:
    """FR-04: feet and yard stay consistent via meter hub."""
    from unit_converter.domain.models import Quantity

    # Given
    quantity = Quantity(unit="feet", value=3.28084)
    # When
    result = engine.convert(quantity)
    feet = next(item.value for item in result.values if item.unit == "feet")
    yard = next(item.value for item in result.values if item.unit == "yard")
    # Then
    assert yard / feet == pytest.approx(1.09361 / 3.28084)
