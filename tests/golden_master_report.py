"""Build one Golden Master snapshot for all 41 BCE scenarios."""

from __future__ import annotations

from pathlib import Path

from tests.scenarios.boundary import collect_boundary_blocks
from tests.scenarios.control import collect_control_blocks
from tests.scenarios.entity import collect_entity_blocks

GOLDEN_MASTER_FILE = "unit_converter.approved.txt"


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
    _ = (default_registry, engine)
    blocks: list[str] = []
    blocks.extend(
        collect_boundary_blocks(
            project_root,
            sample_conversion_result,
            units_json_path,
            units_yaml_path,
        )
    )
    blocks.extend(
        collect_control_blocks(
            conversion_service,
            sample_conversion_result,
            units_json_path,
        )
    )
    blocks.extend(
        collect_entity_blocks(
            empty_registry,
            sample_conversion_result,
            units_json_path,
            engine_source_path,
        )
    )
    blocks.sort()
    return "\n\n".join(blocks) + "\n"
