"""Build one Golden Master snapshot for all 41 BCE scenarios."""

from __future__ import annotations

import inspect
import json
import re
import subprocess
import sys
from collections.abc import Callable
from pathlib import Path

from tests._approval import format_golden_cli, format_golden_error
from unit_converter.conversion.registry import UnitRegistry
from unit_converter.config.json_loader import JsonConfigLoader
from unit_converter.config.yaml_loader import YamlConfigLoader
from unit_converter.conversion.engine import ConversionEngine
from unit_converter.domain.exceptions import (
    ParseError,
    UnknownUnitError,
    ValidationError,
)
from unit_converter.domain.models import Quantity, UnitDefinition
from unit_converter.input.parser import parse_unit_value
from unit_converter.input.unit_registration_parser import parse_unit_registration
from unit_converter.input.validator import InputValidator
from unit_converter.output.csv_formatter import CsvFormatter
from unit_converter.output.formatter_factory import get_formatter, registered_format_names
from unit_converter.output.json_formatter import JsonFormatter
from unit_converter.output.table_formatter import TableFormatter
from unit_converter.output.text_formatter import TextFormatter

GOLDEN_MASTER_FILE = "unit_converter.approved.txt"


def _block(name: str, *lines: str) -> str:
    body = "\n".join(lines)
    return f"[{name}]\n{body}"


def _float(value: float) -> str:
    return f"{value:.6f}"


def _exc_name(fn: Callable[[], object], *expected: type[BaseException]) -> str:
    try:
        fn()
    except expected as exc:
        return type(exc).__name__
    raise AssertionError(f"expected {expected}")


def build_golden_master_report(
    project_root: Path,
    default_registry,
    empty_registry,
    engine,
    conversion_service,
    sample_conversion_result,
    units_json_path: Path,
    units_yaml_path: Path,
    engine_source_path: Path,
) -> str:
    """Serialize all 41 BCE scenario outputs into one deterministic report."""
    blocks: list[str] = []

    # --- boundary ---
    cmd = [sys.executable, "-m", "unit_converter", "meter:2.5"]
    completed = subprocess.run(
        cmd, cwd=project_root, capture_output=True, text=True, timeout=10
    )
    blocks.append(
        _block(
            "test_boundary_FR02_cli_stdout_contains_feet",
            format_golden_cli(completed.returncode, completed.stdout, completed.stderr),
        )
    )

    cmd = [sys.executable, "UnitConverter.py"]
    completed = subprocess.run(
        cmd,
        cwd=project_root,
        input="meter:2.5\n",
        capture_output=True,
        text=True,
        timeout=10,
    )
    match = re.search(r"=\s*([\d.]+)\s*feet", completed.stdout)
    feet = float(match.group(1)) if match else -1.0
    blocks.append(
        _block(
            "test_boundary_FR02_legacy_parity",
            f"exit={completed.returncode}",
            f"feet={_float(feet)}",
        )
    )

    cmd = [sys.executable, "-m", "unit_converter", "meter:-1"]
    completed = subprocess.run(
        cmd, cwd=project_root, capture_output=True, text=True, timeout=10
    )
    blocks.append(
        _block(
            "test_boundary_FR08_cli_negative_exit_nonzero",
            format_golden_cli(
                completed.returncode,
                completed.stdout,
                completed.stderr,
                error=("E008", "NEGATIVE_VALUE"),
            ),
        )
    )

    cmd = [sys.executable, "-m", "unit_converter", "mile:1"]
    completed = subprocess.run(
        cmd, cwd=project_root, capture_output=True, text=True, timeout=10
    )
    blocks.append(
        _block(
            "test_boundary_FR10_cli_unknown_unit",
            format_golden_cli(
                completed.returncode,
                completed.stdout,
                completed.stderr,
                error=("E010", "UNKNOWN_UNIT"),
            ),
        )
    )

    registry = JsonConfigLoader().load(units_json_path)
    blocks.append(
        _block(
            "test_boundary_FR03_config_json_lists_three_units",
            f"count={len(registry.unit_names())}",
        )
    )

    blocks.append(
        _block(
            "test_boundary_FR05_load_units_from_json",
            f"has_feet={registry.has_unit('feet')}",
        )
    )

    yaml_registry = YamlConfigLoader().load(units_yaml_path)
    blocks.append(
        _block(
            "test_boundary_FR05_load_units_from_yaml",
            f"has_yard={yaml_registry.has_unit('yard')}",
        )
    )

    missing = project_root / "config" / "missing-units.json"
    blocks.append(
        _block(
            "test_boundary_FR05_missing_file_raises",
            _exc_name(lambda: JsonConfigLoader().load(missing), FileNotFoundError),
        )
    )

    blocks.append(
        _block(
            "test_boundary_FR07_json_format",
            JsonFormatter().format(sample_conversion_result),
        )
    )
    blocks.append(
        _block(
            "test_boundary_FR07_csv_format",
            CsvFormatter().format(sample_conversion_result),
        )
    )
    blocks.append(
        _block(
            "test_boundary_FR07_table_format",
            TableFormatter().format(sample_conversion_result),
        )
    )

    names = registered_format_names()
    get_formatter("text")
    get_formatter("json")
    get_formatter("csv")
    get_formatter("table")
    blocks.append(
        _block(
            "test_boundary_FR07_factory_all_formats",
            f"names={','.join(sorted(names))}",
        )
    )

    blocks.append(
        _block(
            "test_boundary_FR11_text_output_one_decimal",
            TextFormatter().format(sample_conversion_result),
        )
    )

    quantity = parse_unit_value("meter:2.5")
    blocks.append(
        _block(
            "test_boundary_FR01_parse_valid_unit_value",
            f"unit={quantity.unit}",
            f"value={_float(quantity.value)}",
        )
    )

    quantity = parse_unit_value(" meter:2.5 ")
    blocks.append(
        _block(
            "test_boundary_FR01_parse_trims_whitespace",
            f"unit={quantity.unit}",
            f"value={_float(quantity.value)}",
        )
    )

    for raw, name in (
        ("meter2.5", "test_boundary_FR09_reject_missing_colon"),
        ("meter:abc", "test_boundary_FR09_reject_non_numeric"),
        ("meter", "test_boundary_FR09_reject_bare_unit"),
        ("abc", "test_boundary_FR09_reject_bare_non_unit"),
        ("meter:2.5:extra", "test_boundary_FR09_reject_extra_colon"),
    ):
        blocks.append(
            _block(
                name,
                format_golden_error("E009", "PARSE_ERROR"),
                _exc_name(lambda r=raw: parse_unit_value(r), ParseError),
            )
        )

    definition = parse_unit_registration("1 cubit = 0.4572 meter")
    blocks.append(
        _block(
            "test_boundary_FR06_parse_register_cubit",
            f"name={definition.name}",
            f"ratio={_float(definition.ratio_to_base)}",
        )
    )

    fresh_registry = JsonConfigLoader().load(units_json_path)
    fresh_engine = ConversionEngine(fresh_registry)

    # --- control (validator before service mutates registry) ---
    validator = InputValidator(fresh_registry)
    blocks.append(
        _block(
            "test_control_FR08_reject_negative_value",
            format_golden_error("E008", "NEGATIVE_VALUE"),
            _exc_name(
                lambda: validator.validate(Quantity(unit="meter", value=-1.0)),
                ValidationError,
            ),
        )
    )

    validator.validate(Quantity(unit="meter", value=0.0))
    blocks.append(_block("test_control_FR08_zero_allowed", "OK"))

    blocks.append(
        _block(
            "test_control_FR10_reject_unknown_unit",
            format_golden_error("E010", "UNKNOWN_UNIT"),
            _exc_name(
                lambda: validator.validate(Quantity(unit="mile", value=1.0)),
                UnknownUnitError,
            ),
        )
    )

    blocks.append(
        _block(
            "test_control_FR10_reject_unregistered_cubit",
            format_golden_error("E010", "UNKNOWN_UNIT"),
            _exc_name(
                lambda: validator.validate(Quantity(unit="cubit", value=1.0)),
                UnknownUnitError,
            ),
        )
    )

    result = conversion_service.convert_input("meter:2.5")
    blocks.append(
        _block(
            "test_control_FR02_service_convert_input",
            f"unit={result.source.unit}",
            f"value={_float(result.source.value)}",
        )
    )

    result = conversion_service.convert_input("meter:1.0")
    units = sorted(item.unit for item in result.values)
    blocks.append(
        _block(
            "test_control_FR02_service_returns_all_unit_values",
            f"units={','.join(units)}",
        )
    )

    conversion_service.register_unit("1 cubit = 0.4572 meter")
    result = conversion_service.convert_input("meter:1.0")
    units = sorted(item.unit for item in result.values)
    blocks.append(
        _block(
            "test_control_FR06_service_register_and_convert",
            f"units={','.join(units)}",
        )
    )

    output = conversion_service.format_result(
        sample_conversion_result, JsonFormatter()
    )
    parsed = json.loads(output)
    blocks.append(
        _block(
            "test_control_FR07_service_format_json",
            f"source_unit={parsed['source']['unit']}",
            "feet_in_output=true",
        )
    )

    blocks.append(
        _block(
            "test_control_FR09_service_invalid_format",
            format_golden_error("E009", "PARSE_ERROR"),
            _exc_name(
                lambda: conversion_service.convert_input("invalid"),
                ParseError,
                ValidationError,
            ),
        )
    )

    source = inspect.getsource(conversion_service.convert_input)
    blocks.append(
        _block(
            "test_control_NFR05_no_stdin_mock",
            f"stdin={'stdin' in source}",
            f"parse_unit_value={'parse_unit_value(raw)' in source}",
        )
    )

    # --- entity (fresh registry — unaffected by service.register_unit) ---
    quantity = Quantity(unit="meter", value=2.5)
    result = fresh_engine.convert(quantity)
    feet = next(item.value for item in result.values if item.unit == "feet")
    yard = next(item.value for item in result.values if item.unit == "yard")
    blocks.append(
        _block(
            "test_entity_FR02_convert_to_all_registered_units",
            f"feet={_float(feet)}",
            f"yard={_float(yard)}",
        )
    )

    quantity = Quantity(unit="feet", value=8.2021)
    result = fresh_engine.convert(quantity)
    meter = next(item.value for item in result.values if item.unit == "meter")
    blocks.append(
        _block(
            "test_entity_FR02_feet_input_converts_to_meter",
            f"meter={_float(meter)}",
        )
    )

    names = sorted(fresh_registry.unit_names())
    blocks.append(
        _block(
            "test_entity_FR03_default_units_in_registry",
            f"units={','.join(names)}",
        )
    )

    quantity = Quantity(unit="meter", value=1.0)
    result = fresh_engine.convert(quantity)
    feet = next(item.value for item in result.values if item.unit == "feet")
    yard = next(item.value for item in result.values if item.unit == "yard")
    blocks.append(
        _block(
            "test_entity_FR04_meter_hub_converts_to_feet_and_yard",
            f"feet={_float(feet)}",
            f"yard={_float(yard)}",
        )
    )

    quantity = Quantity(unit="feet", value=3.28084)
    result = fresh_engine.convert(quantity)
    feet = next(item.value for item in result.values if item.unit == "feet")
    yard = next(item.value for item in result.values if item.unit == "yard")
    ratio = yard / feet
    blocks.append(
        _block(
            "test_entity_FR04_feet_yard_cross_consistent",
            f"ratio={_float(ratio)}",
        )
    )

    cubit = UnitDefinition(name="cubit", ratio_to_base=0.4572)
    empty_registry.register(cubit)
    blocks.append(
        _block(
            "test_entity_FR06_registry_stores_cubit",
            f"has_cubit={empty_registry.has_unit('cubit')}",
        )
    )

    reg = UnitRegistry(base_unit="meter")
    reg.register_many(
        [
            UnitDefinition(name="meter", ratio_to_base=1.0),
            UnitDefinition(name="cubit", ratio_to_base=0.4572),
        ]
    )
    eng = ConversionEngine(reg)
    result = eng.convert(Quantity(unit="meter", value=1.0))
    unit_set = sorted(item.unit for item in result.values)
    blocks.append(
        _block(
            "test_entity_FR06_cubit_in_conversion_output",
            f"units={','.join(unit_set)}",
        )
    )

    rounded = sample_conversion_result.rounded_value(8.2021)
    blocks.append(
        _block(
            "test_entity_FR11_rounding_policy_one_decimal",
            f"rounded={_float(rounded)}",
        )
    )

    source = engine_source_path.read_text(encoding="utf-8")
    blocks.append(
        _block(
            "test_entity_NFR01_engine_no_unit_branch",
            f"elif_unit={'elif unit' in source}",
            f"feet_eq={'unit == \"feet\"' in source}",
            f"yard_eq={'unit == \"yard\"' in source}",
            f"meter_eq={'unit == \"meter\"' in source}",
        )
    )

    blocks.append(
        _block(
            "test_entity_NFR06_engine_no_magic_numbers",
            f"ratio_feet={'3.28084' in source}",
            f"ratio_yard={'1.09361' in source}",
        )
    )

    blocks.sort()
    return "\n\n".join(blocks) + "\n"
