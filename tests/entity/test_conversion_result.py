"""Entity conversion result / display rounding tests (FR-11)."""

from __future__ import annotations

from unit_converter.output.rounding import round_for_display


def test_entity_FR11_rounding_policy_one_decimal() -> None:
    """FR-11: round_for_display(8.2021) displays as 8.2."""
    # Given
    raw_value = 8.2021
    # When
    rounded = round_for_display(raw_value)
    # Then
    assert rounded == 8.2
