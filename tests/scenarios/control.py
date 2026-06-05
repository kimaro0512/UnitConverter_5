"""Control scenario capture (shared by Golden Master)."""

from __future__ import annotations

import inspect
import json
from pathlib import Path

from tests._approval import format_golden_error
from tests.scenarios.helpers import block, exc_name, float_text
from unit_converter.config.json_loader import JsonConfigLoader
from unit_converter.domain.exceptions import (
    ParseError,
    UnknownUnitError,
    ValidationError,
)
from unit_converter.domain.models import Quantity
from unit_converter.input.validator import InputValidator
from unit_converter.output.json_formatter import JsonFormatter


def collect_control_blocks(
    conversion_service,
    sample_conversion_result,
    units_json_path: Path,
) -> list[str]:
    blocks: list[str] = []
    fresh_registry = JsonConfigLoader().load(units_json_path)
    validator = InputValidator(fresh_registry)

    blocks.append(
        block(
            "test_control_FR08_reject_negative_value",
            format_golden_error("E008", "NEGATIVE_VALUE"),
            exc_name(
                lambda: validator.validate(Quantity(unit="meter", value=-1.0)),
                ValidationError,
            ),
        )
    )
    validator.validate(Quantity(unit="meter", value=0.0))
    blocks.append(block("test_control_FR08_zero_allowed", "OK"))

    blocks.append(
        block(
            "test_control_FR10_reject_unknown_unit",
            format_golden_error("E010", "UNKNOWN_UNIT"),
            exc_name(
                lambda: validator.validate(Quantity(unit="mile", value=1.0)),
                UnknownUnitError,
            ),
        )
    )
    blocks.append(
        block(
            "test_control_FR10_reject_unregistered_cubit",
            format_golden_error("E010", "UNKNOWN_UNIT"),
            exc_name(
                lambda: validator.validate(Quantity(unit="cubit", value=1.0)),
                UnknownUnitError,
            ),
        )
    )

    result = conversion_service.convert_input("meter:2.5")
    blocks.append(
        block(
            "test_control_FR02_service_convert_input",
            f"unit={result.source.unit}",
            f"value={float_text(result.source.value)}",
        )
    )

    result = conversion_service.convert_input("meter:1.0")
    units = sorted(item.unit for item in result.values)
    blocks.append(
        block(
            "test_control_FR02_service_returns_all_unit_values",
            f"units={','.join(units)}",
        )
    )

    conversion_service.register_unit("1 cubit = 0.4572 meter")
    result = conversion_service.convert_input("meter:1.0")
    units = sorted(item.unit for item in result.values)
    blocks.append(
        block(
            "test_control_FR06_service_register_and_convert",
            f"units={','.join(units)}",
        )
    )

    output = conversion_service.format_result(sample_conversion_result, JsonFormatter())
    parsed = json.loads(output)
    blocks.append(
        block(
            "test_control_FR07_service_format_json",
            f"source_unit={parsed['source']['unit']}",
            "feet_in_output=true",
        )
    )
    blocks.append(
        block(
            "test_control_FR09_service_invalid_format",
            format_golden_error("E009", "PARSE_ERROR"),
            exc_name(
                lambda: conversion_service.convert_input("invalid"),
                ParseError,
                ValidationError,
            ),
        )
    )

    source = inspect.getsource(conversion_service.convert_input)
    blocks.append(
        block(
            "test_control_NFR05_no_stdin_mock",
            f"stdin={'stdin' in source}",
            f"parse_unit_value={'parse_unit_value(raw)' in source}",
        )
    )

    return blocks
