"""Entity conversion engine tests (FR-02, FR-03, FR-04)."""

from __future__ import annotations

import pytest


def test_entity_FR02_convert_to_all_registered_units(engine) -> None:
    """FR-02: meter 2.5 converts to all registered units."""
    # Given
    # When
    try:
        from unit_converter.domain.models import Quantity

        if engine is not None:
            quantity = Quantity(unit="meter", value=2.5)
            engine.convert(quantity)
    except (ModuleNotFoundError, NotImplementedError):
        pass
    # Then
    pytest.fail("Red skeleton: feet≈8.2021, yard≈2.7340")


def test_entity_FR02_feet_input_converts_to_meter(engine) -> None:
    """FR-02: feet input converts back to meter."""
    # Given
    # When
    try:
        from unit_converter.domain.models import Quantity

        if engine is not None:
            quantity = Quantity(unit="feet", value=8.2021)
            engine.convert(quantity)
    except (ModuleNotFoundError, NotImplementedError):
        pass
    # Then
    pytest.fail("Red skeleton: meter≈2.5")


def test_entity_FR03_default_units_in_registry(default_registry) -> None:
    """FR-03: default registry lists meter, feet, yard."""
    # Given
    # When
    try:
        if default_registry is not None:
            default_registry.unit_names()
    except (ModuleNotFoundError, NotImplementedError):
        pass
    # Then
    pytest.fail("Red skeleton: unit_names() == {meter, feet, yard}")


def test_entity_FR04_meter_hub_converts_to_feet_and_yard(engine) -> None:
    """FR-04: meter hub converts 1.0 m to feet and yard."""
    # Given
    # When
    try:
        from unit_converter.domain.models import Quantity

        if engine is not None:
            quantity = Quantity(unit="meter", value=1.0)
            engine.convert(quantity)
    except (ModuleNotFoundError, NotImplementedError):
        pass
    # Then
    pytest.fail("Red skeleton: feet≈3.28084, yard≈1.09361")


def test_entity_FR04_feet_yard_cross_consistent(engine) -> None:
    """FR-04: feet and yard stay consistent via meter hub."""
    # Given
    # When
    try:
        from unit_converter.domain.models import Quantity

        if engine is not None:
            quantity = Quantity(unit="feet", value=3.28084)
            engine.convert(quantity)
    except (ModuleNotFoundError, NotImplementedError):
        pass
    # Then
    pytest.fail("Red skeleton: yard/feet ≈ 1.09361/3.28084")
