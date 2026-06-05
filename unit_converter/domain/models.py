"""Domain models (FR-01, FR-02, FR-04)."""

from __future__ import annotations

from dataclasses import dataclass, field


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


@dataclass
class ConversionResult:
    """FR-02: Full conversion output for a single input quantity."""

    source: Quantity
    values: list[ConvertedValue] = field(default_factory=list)

    DEFAULT_DECIMAL_PLACES: int = 1

    def rounded_value(self, value: float, places: int | None = None) -> float:
        """FR-11: Round for display (README example uses one decimal place)."""
        places = self.DEFAULT_DECIMAL_PLACES if places is None else places
        return round(value, places)
