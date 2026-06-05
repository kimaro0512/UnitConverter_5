"""Entity conversion result tests (FR-11)."""

from __future__ import annotations

import pytest


def test_entity_FR11_rounding_policy_one_decimal(sample_conversion_result) -> None:
    """FR-11: rounded_value(8.2021) displays as 8.2."""
    # Given
    raw_value = 8.2021
    # When
    try:
        if sample_conversion_result is not None:
            sample_conversion_result.rounded_value(raw_value)
    except (ModuleNotFoundError, NotImplementedError):
        pass
    # Then
    pytest.fail("Red skeleton: rounded_value(8.2021) == 8.2")
