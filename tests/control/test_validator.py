"""Control validator tests (FR-08, FR-10)."""

from __future__ import annotations

import pytest


def test_control_FR08_reject_negative_value(default_registry) -> None:
    """FR-08: validator rejects negative meter value."""
    # Given
    # When
    try:
        from unit_converter.domain.models import Quantity
        from unit_converter.input.validator import InputValidator

        if default_registry is not None:
            validator = InputValidator(default_registry)
            validator.validate(Quantity(unit="meter", value=-1.0))
    except (ModuleNotFoundError, NotImplementedError):
        pass
    # Then
    pytest.fail("Red skeleton: ValidationError for meter:-1")


def test_control_FR08_zero_allowed(default_registry) -> None:
    """FR-08: validator allows zero."""
    # Given
    # When
    try:
        from unit_converter.domain.models import Quantity
        from unit_converter.input.validator import InputValidator

        if default_registry is not None:
            validator = InputValidator(default_registry)
            validator.validate(Quantity(unit="meter", value=0.0))
    except (ModuleNotFoundError, NotImplementedError):
        pass
    # Then
    pytest.fail("Red skeleton: no exception for meter:0")


def test_control_FR10_reject_unknown_unit(default_registry) -> None:
    """FR-10: validator rejects unknown unit mile."""
    # Given
    # When
    try:
        from unit_converter.domain.models import Quantity
        from unit_converter.input.validator import InputValidator

        if default_registry is not None:
            validator = InputValidator(default_registry)
            validator.validate(Quantity(unit="mile", value=1.0))
    except (ModuleNotFoundError, NotImplementedError):
        pass
    # Then
    pytest.fail("Red skeleton: UnknownUnitError for mile:1")


def test_control_FR10_reject_unregistered_cubit(default_registry) -> None:
    """FR-10: validator rejects unregistered cubit."""
    # Given
    # When
    try:
        from unit_converter.domain.models import Quantity
        from unit_converter.input.validator import InputValidator

        if default_registry is not None:
            validator = InputValidator(default_registry)
            validator.validate(Quantity(unit="cubit", value=1.0))
    except (ModuleNotFoundError, NotImplementedError):
        pass
    # Then
    pytest.fail("Red skeleton: UnknownUnitError for cubit:1")
