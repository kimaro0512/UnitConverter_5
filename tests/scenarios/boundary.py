"""Boundary scenario capture (shared by Golden Master)."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

from tests._approval import format_golden_cli, format_golden_error_code
from unit_converter.domain.error_codes import ErrorCode
from tests.scenarios.helpers import block, exc_name, float_text
from unit_converter.config.json_loader import JsonConfigLoader
from unit_converter.config.loader_factory import resolve_config_loader
from unit_converter.config.yaml_loader import YamlConfigLoader
from unit_converter.domain.exceptions import ParseError
from unit_converter.input.parser import parse_unit_value
from unit_converter.input.unit_registration_parser import parse_unit_registration
from unit_converter.output.csv_formatter import CsvFormatter
from unit_converter.output.formatter_factory import get_formatter, registered_format_names
from unit_converter.output.json_formatter import JsonFormatter
from unit_converter.output.table_formatter import TableFormatter
from unit_converter.output.text_formatter import TextFormatter


def collect_boundary_blocks(
    project_root: Path,
    sample_conversion_result,
    units_json_path: Path,
    units_yaml_path: Path,
) -> list[str]:
    blocks: list[str] = []

    cmd = [sys.executable, "-m", "unit_converter", "meter:2.5"]
    completed = subprocess.run(
        cmd, cwd=project_root, capture_output=True, text=True, timeout=10
    )
    blocks.append(
        block(
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
        block(
            "test_boundary_FR02_legacy_parity",
            f"exit={completed.returncode}",
            f"feet={float_text(feet)}",
        )
    )

    for cli_args, test_name, error_code in (
        (["meter:-1"], "test_boundary_FR08_cli_negative_exit_nonzero", ErrorCode.NEGATIVE_VALUE),
        (["mile:1"], "test_boundary_FR10_cli_unknown_unit", ErrorCode.UNKNOWN_UNIT),
    ):
        completed = subprocess.run(
            [sys.executable, "-m", "unit_converter", *cli_args],
            cwd=project_root,
            capture_output=True,
            text=True,
            timeout=10,
        )
        blocks.append(
            block(
                test_name,
                format_golden_cli(
                    completed.returncode,
                    completed.stdout,
                    completed.stderr,
                    error=(error_code.code, error_code.name_label),
                ),
            )
        )

    registry = JsonConfigLoader().load(units_json_path)
    blocks.append(
        block(
            "test_boundary_FR03_config_json_lists_three_units",
            f"count={len(registry.unit_names())}",
        )
    )
    blocks.append(
        block(
            "test_boundary_FR05_load_units_from_json",
            f"has_feet={registry.has_unit('feet')}",
        )
    )

    yaml_registry = YamlConfigLoader().load(units_yaml_path)
    blocks.append(
        block(
            "test_boundary_FR05_load_units_from_yaml",
            f"has_yard={yaml_registry.has_unit('yard')}",
        )
    )

    missing = project_root / "config" / "missing-units.json"
    blocks.append(
        block(
            "test_boundary_FR05_missing_file_raises",
            exc_name(
                lambda: resolve_config_loader(missing).load(missing),
                FileNotFoundError,
            ),
        )
    )

    blocks.append(
        block(
            "test_boundary_FR07_json_format",
            JsonFormatter().format(sample_conversion_result),
        )
    )
    blocks.append(
        block(
            "test_boundary_FR07_csv_format",
            CsvFormatter().format(sample_conversion_result),
        )
    )
    blocks.append(
        block(
            "test_boundary_FR07_table_format",
            TableFormatter().format(sample_conversion_result),
        )
    )

    names = registered_format_names()
    for fmt in ("text", "json", "csv", "table"):
        get_formatter(fmt)
    blocks.append(
        block(
            "test_boundary_FR07_factory_all_formats",
            f"names={','.join(sorted(names))}",
        )
    )
    blocks.append(
        block(
            "test_boundary_FR11_text_output_one_decimal",
            TextFormatter().format(sample_conversion_result),
        )
    )

    quantity = parse_unit_value("meter:2.5")
    blocks.append(
        block(
            "test_boundary_FR01_parse_valid_unit_value",
            f"unit={quantity.unit}",
            f"value={float_text(quantity.value)}",
        )
    )

    quantity = parse_unit_value(" meter:2.5 ")
    blocks.append(
        block(
            "test_boundary_FR01_parse_trims_whitespace",
            f"unit={quantity.unit}",
            f"value={float_text(quantity.value)}",
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
            block(
                name,
                format_golden_error_code(ErrorCode.PARSE_ERROR),
                exc_name(lambda r=raw: parse_unit_value(r), ParseError),
            )
        )

    definition = parse_unit_registration("1 cubit = 0.4572 meter")
    blocks.append(
        block(
            "test_boundary_FR06_parse_register_cubit",
            f"name={definition.name}",
            f"ratio={float_text(definition.ratio_to_base)}",
        )
    )

    return blocks
