"""Domain exceptions (FR-08, FR-09, FR-10)."""


class UnitConverterError(Exception):
    """Base exception for unit converter domain."""


class RegistryKeyError(UnitConverterError):
    """Storage lookup failed — not a user validation error (FR-10 via Validator)."""


class ParseError(UnitConverterError):
    """FR-09: Input string could not be parsed."""


class ValidationError(UnitConverterError):
    """FR-08, FR-09, FR-10: Input failed validation."""


class UnknownUnitError(ValidationError):
    """FR-10: Unit is not registered."""
