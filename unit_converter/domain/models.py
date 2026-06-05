"""Domain models (FR-01, FR-02, FR-04)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Quantity:
    """Parsed input: unit name and numeric value."""

    unit: str
    value: float


@dataclass(frozen=True)
class UnitDefinition:
    """Single unit expressed as ratio to the registry base unit."""

    name: str
    ratio_to_base: float


@dataclass(frozen=True)
class ConvertedValue:
    """One target unit and its converted numeric value."""

    unit: str
    value: float


@dataclass(frozen=True)
class ConversionResult:
    """FR-02: Full conversion output for a single input quantity."""

    source: Quantity
    values: tuple[ConvertedValue, ...] = ()
