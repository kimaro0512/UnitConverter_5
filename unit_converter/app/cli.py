"""CLI entry point (FR-02, FR-07, FR-08, FR-10)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from unit_converter.app.service import ConversionService
from unit_converter.config.loader_factory import resolve_config_loader
from unit_converter.config.protocols import ConfigLoader
from unit_converter.conversion.engine import ConversionEngine
from unit_converter.domain.exceptions import (
    ParseError,
    UnitConverterError,
    UnknownUnitError,
    ValidationError,
)
from unit_converter.input.validator import InputValidator
from unit_converter.output.formatter_factory import get_formatter


def _default_config_path() -> Path:
    return Path(__file__).resolve().parent.parent.parent / "config" / "units.json"


def _build_service(
    config_path: Path | None = None,
    loader: ConfigLoader | None = None,
) -> ConversionService:
    path = config_path or _default_config_path()
    config_loader = loader or resolve_config_loader(path)
    registry = config_loader.load(path)
    engine = ConversionEngine(registry)
    validator = InputValidator(registry)
    return ConversionService(registry=registry, engine=engine, validator=validator)


def main(argv: list[str] | None = None) -> int:
    """Run the unit converter CLI."""
    parser = argparse.ArgumentParser(description="Length unit converter")
    parser.add_argument("input", nargs="?", help="unit:value (e.g. meter:2.5)")
    parser.add_argument(
        "--format",
        default="text",
        choices=["text", "json", "csv", "table"],
        help="Output format (default: text)",
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=None,
        help="Path to units config (JSON or YAML)",
    )
    args = parser.parse_args(argv)

    if not args.input:
        print("Usage: unit-converter unit:value [--format text|json|csv|table]", file=sys.stderr)
        return 1

    try:
        service = _build_service(args.config)
        result = service.convert_input(args.input)
        formatter = get_formatter(args.format)
        print(service.format_result(result, formatter))
        return 0
    except (ParseError, ValidationError, UnknownUnitError, UnitConverterError) as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
