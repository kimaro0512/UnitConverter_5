"""Golden Master — all 41 BCE scenarios vs one approved baseline."""

from __future__ import annotations

from tests._approval import assert_matches_golden
from tests.golden_master_report import (
    GOLDEN_MASTER_FILE,
    build_golden_master_report,
)


def test_golden_master_all_scenarios(
    project_root,
    default_registry,
    empty_registry,
    engine,
    conversion_service,
    sample_conversion_result,
    units_json_path,
    units_yaml_path,
    engine_source_path,
) -> None:
    """Golden Master: 41 BCE scenario snapshot vs tests/golden/unit_converter.approved.txt."""
    report = build_golden_master_report(
        project_root=project_root,
        default_registry=default_registry,
        empty_registry=empty_registry,
        engine=engine,
        conversion_service=conversion_service,
        sample_conversion_result=sample_conversion_result,
        units_json_path=units_json_path,
        units_yaml_path=units_yaml_path,
        engine_source_path=engine_source_path,
    )
    assert_matches_golden(report, GOLDEN_MASTER_FILE)
