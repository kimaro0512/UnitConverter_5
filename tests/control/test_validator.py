"""Control validator tests (FR-08, FR-10)."""

from __future__ import annotations

import pytest

from unit_converter.domain.exceptions import UnknownUnitError, ValidationError
from unit_converter.domain.models import Quantity
from unit_converter.input.validator import InputValidator


def test_control_FR08_reject_negative_value(default_registry) -> None:
    """FR-08: validator rejects negative meter value."""
    # Given
    validator = InputValidator(default_registry)
    # When / Then
    with pytest.raises(ValidationError):
        validator.validate(Quantity(unit="meter", value=-1.0))


def test_control_FR08_zero_allowed(default_registry) -> None:
    """FR-08: validator allows zero."""
    # Given
    validator = InputValidator(default_registry)
    # When / Then — no exception
    validator.validate(Quantity(unit="meter", value=0.0))


def test_control_FR10_reject_unknown_unit(default_registry) -> None:
    """FR-10: validator rejects unknown unit mile."""
    # Given
    validator = InputValidator(default_registry)
    # When / Then
    with pytest.raises(UnknownUnitError):
        validator.validate(Quantity(unit="mile", value=1.0))


def test_control_FR10_reject_unregistered_cubit(default_registry) -> None:
    """FR-10: validator rejects unregistered cubit."""
    # Given
    validator = InputValidator(default_registry)
    # When / Then
    with pytest.raises(UnknownUnitError):
        validator.validate(Quantity(unit="cubit", value=1.0))
