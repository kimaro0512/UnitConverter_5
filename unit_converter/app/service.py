"""Conversion service — use-case orchestration (FR-02, FR-06, FR-07, NFR-05)."""

from __future__ import annotations

from unit_converter.conversion.engine import ConversionEngine
from unit_converter.conversion.protocols import UnitRegistryPort
from unit_converter.domain.models import ConversionResult
from unit_converter.input.parser import parse_unit_value
from unit_converter.input.unit_registration_parser import parse_unit_registration
from unit_converter.input.validator import InputValidator
from unit_converter.output.protocols import OutputFormatter


class ConversionService:
    """Orchestrates parse → validate → convert → format without I/O."""

    def __init__(
        self,
        registry: UnitRegistryPort,
        engine: ConversionEngine,
        validator: InputValidator | None = None,
    ) -> None:
        self._registry = registry
        self._engine = engine
        self._validator = validator or InputValidator(registry)

    def convert_input(self, raw: str) -> ConversionResult:
        """FR-02, FR-09: Parse, validate, and convert a unit:value string."""
        quantity = parse_unit_value(raw)
        self._validator.validate(quantity)
        return self._engine.convert(quantity)

    def register_unit(self, registration: str) -> None:
        """FR-06: Register a new unit from a registration string."""
        definition = parse_unit_registration(registration)
        self._registry.register(definition)

    def format_result(
        self,
        result: ConversionResult,
        formatter: OutputFormatter,
    ) -> str:
        """FR-07: Delegate formatting to the selected formatter."""
        return formatter.format(result)
