"""Entity registry tests (FR-06)."""

from __future__ import annotations

import pytest


def test_entity_FR06_registry_stores_cubit(empty_registry) -> None:
    """FR-06: registry stores cubit after registration."""
    # Given
    # When
    try:
        from unit_converter.domain.models import UnitDefinition

        if empty_registry is not None:
            cubit = UnitDefinition(name="cubit", ratio_to_base=0.4572)
            empty_registry.register(cubit)
    except (ModuleNotFoundError, NotImplementedError):
        pass
    # Then
    pytest.fail("Red skeleton: has_unit('cubit') is True")


def test_entity_FR06_cubit_in_conversion_output(empty_registry) -> None:
    """FR-06: cubit appears in conversion output after registration."""
    # Given
    # When
    try:
        from unit_converter.conversion.engine import ConversionEngine
        from unit_converter.domain.models import Quantity

        if empty_registry is not None:
            engine = ConversionEngine(empty_registry)
            engine.convert(Quantity(unit="meter", value=1.0))
    except (ModuleNotFoundError, NotImplementedError):
        pass
    # Then
    pytest.fail("Red skeleton: conversion values include cubit")
