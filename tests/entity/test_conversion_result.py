"""Entity conversion result tests (FR-11)."""

from __future__ import annotations


def test_entity_FR11_rounding_policy_one_decimal(sample_conversion_result) -> None:
    """FR-11: rounded_value(8.2021) displays as 8.2."""
    # Given
    raw_value = 8.2021
    # When
    rounded = sample_conversion_result.rounded_value(raw_value)
    # Then
    assert rounded == 8.2
